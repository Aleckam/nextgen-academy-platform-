from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify, send_file
from io import BytesIO

from app.extensions import db
from app.models import User, Role, AccountType, AgeGroup, School, SchoolClass, LessonProgress, Certificate
from app.utils.rbac import roles_required
from app.utils.csv_import import parse_student_csv
from app.utils.pins import generate_unique_pin, generate_username
from app.utils.pdf import render_pin_cards_pdf, render_term_report_pdf

bp = Blueprint("schools", __name__)


@bp.get("/<int:school_id>/dashboard")
@roles_required(Role.SCHOOL_ADMIN, Role.SUPER_ADMIN)
def dashboard(school_id):
    """Backs WF01 — School Admin Dashboard: enrolled students, completion
    rates, active users, certificates, classes & progress, inactive alerts."""
    school = School.query.get_or_404(school_id)
    classes = school.classes.all()

    class_rows = []
    total_students = 0
    total_completion = 0
    for cls in classes:
        students = cls.students.filter_by(role=Role.STUDENT).all()
        count = len(students)
        total_students += count
        completion = _average_completion([s.id for s in students])
        total_completion += completion * count
        class_rows.append(
            {
                **cls.to_dict(),
                "teacher_name": cls.teacher_id and User.query.get(cls.teacher_id).name,
                "completion_pct": completion,
                "status": "needs_attention" if completion < 60 else "on_track",
            }
        )

    week_ago = datetime.utcnow() - timedelta(days=7)
    active_this_week = User.query.filter(
        User.school_id == school_id,
        User.role == Role.STUDENT,
        User.last_active_at >= week_ago,
    ).count()

    certificates_earned = (
        db.session.query(Certificate)
        .join(User, Certificate.student_id == User.id)
        .filter(User.school_id == school_id)
        .count()
    )

    inactive_cutoff = datetime.utcnow() - timedelta(days=7)
    inactive_students = (
        User.query.filter(
            User.school_id == school_id,
            User.role == Role.STUDENT,
            db.or_(User.last_active_at.is_(None), User.last_active_at < inactive_cutoff),
        )
        .limit(20)
        .all()
    )

    avg_completion = round(total_completion / total_students) if total_students else 0

    return jsonify(
        {
            "school": school.to_dict(),
            "stats": {
                "students_enrolled": total_students,
                "classes_count": len(classes),
                "average_completion_pct": avg_completion,
                "certificates_earned": certificates_earned,
                "active_this_week": active_this_week,
            },
            "classes": class_rows,
            "inactive_students": [
                {
                    "id": s.id,
                    "name": s.name,
                    "class_id": s.class_id,
                    "last_active_at": s.last_active_at.isoformat() if s.last_active_at else None,
                }
                for s in inactive_students
            ],
        }
    )


def _average_completion(student_ids: list) -> int:
    if not student_ids:
        return 0
    rows = LessonProgress.query.filter(LessonProgress.student_id.in_(student_ids)).all()
    if not rows:
        return 0
    completed = sum(1 for r in rows if r.status == "completed")
    return round((completed / len(rows)) * 100)


@bp.post("/<int:school_id>/students/upload")
@roles_required(Role.SCHOOL_ADMIN, Role.SUPER_ADMIN)
def upload_students_csv(school_id):
    """Step 1 of WF03 — parses and validates the CSV, returns a preview
    (valid rows / rows needing attention) without writing to the DB yet."""
    School.query.get_or_404(school_id)
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    result = parse_student_csv(request.files["file"].stream)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)


@bp.post("/<int:school_id>/students/confirm")
@roles_required(Role.SCHOOL_ADMIN, Role.SUPER_ADMIN)
def confirm_students(school_id):
    """Step 2 of WF03 — 'Confirm & create accounts'. Creates a User (role
    student, PIN login, no email) per validated row, auto-generating a
    username and a 4-digit PIN unique to the school/class."""
    school = School.query.get_or_404(school_id)
    data = request.get_json(force=True) or {}
    rows = data.get("valid_rows", [])
    if not rows:
        return jsonify({"error": "No valid rows supplied"}), 400

    existing_usernames = {
        u.username.lower()
        for u in User.query.filter_by(school_id=school_id).all()
        if u.username
    }

    created, pin_card_rows, class_ids_by_name = [], {}, {}
    for row in rows:
        class_name = row["class_name"]
        cls = SchoolClass.query.filter_by(school_id=school_id, name=class_name).first()
        if not cls:
            cls = SchoolClass(school_id=school_id, name=class_name)
            db.session.add(cls)
            db.session.flush()
        class_ids_by_name[class_name] = cls.id

        username = generate_username(row["first_name"], row["last_name"], existing_usernames)
        pin = generate_unique_pin(school_id)

        student = User(
            role=Role.STUDENT,
            account_type=AccountType.SCHOOL,
            age_group=AgeGroup.KIDS if (row.get("age_group") or "").startswith("7") else AgeGroup.TEENS,
            name=f"{row['first_name']} {row['last_name']}",
            username=username,
            school_id=school_id,
            class_id=cls.id,
        )
        student.set_pin(pin)
        db.session.add(student)
        db.session.flush()

        created.append(student.id)
        pin_card_rows.setdefault(class_name, []).append(
            {"name": student.name, "username": username, "pin": pin}
        )

    db.session.commit()

    return jsonify(
        {
            "created_count": len(created),
            "student_ids": created,
            "pin_cards_by_class": pin_card_rows,
            "class_ids_by_name": class_ids_by_name,
            "school_name": school.name,
        }
    ), 201


@bp.post("/<int:school_id>/classes/<int:class_id>/pin-cards.pdf")
@roles_required(Role.SCHOOL_ADMIN, Role.SUPER_ADMIN)
def pin_cards_pdf(school_id, class_id):
    """Step 3 of WF03 — printable PIN card PDF, one per class. Expects the
    plaintext PIN list from the confirm step (PINs are hashed at rest and
    cannot be recovered after this point, matching real password-hash
    behaviour — the admin must download cards immediately after upload)."""
    school = School.query.get_or_404(school_id)
    cls = SchoolClass.query.get_or_404(class_id)
    data = request.get_json(force=True) or {}
    students = data.get("students", [])  # [{name, username, pin}]

    pdf_bytes = render_pin_cards_pdf(school.name, cls.name, school.term_label, students)
    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"pin-cards-{cls.name.replace(' ', '-')}.pdf",
    )


@bp.get("/<int:school_id>/term-report.pdf")
@roles_required(Role.SCHOOL_ADMIN, Role.SUPER_ADMIN)
def term_report_pdf(school_id):
    """One-click term report PDF (§3.5) — completion rates, quiz scores and
    certificates for all classes."""
    school = School.query.get_or_404(school_id)
    classes = school.classes.all()

    class_rows, total_students, total_certs = [], 0, 0
    for cls in classes:
        students = cls.students.filter_by(role=Role.STUDENT).all()
        completion = _average_completion([s.id for s in students])
        certs = (
            db.session.query(Certificate)
            .join(User, Certificate.student_id == User.id)
            .filter(User.class_id == cls.id)
            .count()
        )
        total_students += len(students)
        total_certs += certs
        class_rows.append(
            {"name": cls.name, "student_count": len(students), "completion_pct": completion, "certificates": certs}
        )

    overall = round(sum(c["completion_pct"] for c in class_rows) / len(class_rows)) if class_rows else 0
    summary = {
        "students_covered": total_students,
        "classes_included": len(classes),
        "certificates_issued": total_certs,
        "overall_completion": overall,
    }
    pdf_bytes = render_term_report_pdf(school.name, school.term_label, summary, class_rows)
    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"term-report-{school.term_label.replace(' ', '-')}.pdf",
    )


@bp.post("")
@roles_required(Role.SUPER_ADMIN)
def create_school():
    """NextGen admin provisions a new school account (§3.5, §3.2 Admin Panel)."""
    data = request.get_json(force=True) or {}
    if not data.get("name"):
        return jsonify({"error": "name is required"}), 400
    school = School(name=data["name"], term_label=data.get("term_label", "Term 1"))
    db.session.add(school)
    db.session.commit()
    return jsonify(school.to_dict()), 201
