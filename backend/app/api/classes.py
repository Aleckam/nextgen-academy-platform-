from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from app.extensions import db
from app.models import (
    User,
    Role,
    SchoolClass,
    Module,
    LessonProgress,
    Lesson,
    QuizAttempt,
    Quiz,
    Certificate,
)
from app.utils.rbac import roles_required

bp = Blueprint("classes", __name__)


@bp.get("/<int:class_id>")
@roles_required(Role.SCHOOL_ADMIN, Role.TEACHER, Role.SUPER_ADMIN)
def class_view(class_id):
    """Backs WF02 — Individual Class View: module progress strip, per-student
    progress table (module, progress %, quiz avg, last active), live
    activity feed. Teacher access is read-only (§3.5)."""
    cls = SchoolClass.query.get_or_404(class_id)
    students = cls.students.filter_by(role=Role.STUDENT).all()
    student_ids = [s.id for s in students]

    modules = Module.query.filter_by(programme_id=cls.programme_id).order_by(Module.order).all() if cls.programme_id else []
    module_progress = []
    for m in modules:
        lesson_ids = [l.id for l in m.lessons]
        pct = _class_module_completion(student_ids, lesson_ids)
        module_progress.append({"id": m.id, "title": m.title, "completion_pct": pct})

    student_rows = []
    for s in students:
        progress_rows = LessonProgress.query.filter_by(student_id=s.id).all()
        completion = _pct_completed(progress_rows)
        quiz_avg = _quiz_average(s.id)
        student_rows.append(
            {
                "id": s.id,
                "name": s.name,
                "username": s.username,
                "progress_pct": completion,
                "quiz_avg_pct": quiz_avg,
                "last_active_at": s.last_active_at.isoformat() if s.last_active_at else None,
                "status": _status_for(completion, s.last_active_at),
            }
        )

    return jsonify(
        {
            "class": cls.to_dict(),
            "module_progress": module_progress,
            "students": student_rows,
            "activity_feed": _activity_feed(student_ids),
        }
    )


def _class_module_completion(student_ids, lesson_ids):
    if not student_ids or not lesson_ids:
        return 0
    rows = LessonProgress.query.filter(
        LessonProgress.student_id.in_(student_ids), LessonProgress.lesson_id.in_(lesson_ids)
    ).all()
    total_slots = len(student_ids) * len(lesson_ids)
    if not total_slots:
        return 0
    completed = sum(1 for r in rows if r.status == "completed")
    return round((completed / total_slots) * 100)


def _pct_completed(progress_rows):
    if not progress_rows:
        return 0
    completed = sum(1 for r in progress_rows if r.status == "completed")
    return round((completed / len(progress_rows)) * 100)


def _quiz_average(student_id):
    attempts = QuizAttempt.query.filter_by(student_id=student_id).all()
    if not attempts:
        return None
    return round(sum(a.score_pct for a in attempts) / len(attempts))


def _status_for(completion_pct, last_active_at):
    import datetime as dt

    if last_active_at is None or (dt.datetime.utcnow() - last_active_at).days > 7:
        return "inactive"
    if completion_pct < 50:
        return "falling_behind"
    return "on_track"


def _activity_feed(student_ids, limit=20):
    if not student_ids:
        return []
    events = []

    for cert in (
        Certificate.query.filter(Certificate.student_id.in_(student_ids))
        .order_by(Certificate.issued_at.desc())
        .limit(limit)
        .all()
    ):
        student = User.query.get(cert.student_id)
        events.append(
            {
                "type": "certificate",
                "at": cert.issued_at.isoformat(),
                "message": f"{student.name} earned a certificate",
            }
        )

    for attempt in (
        QuizAttempt.query.filter(QuizAttempt.student_id.in_(student_ids))
        .order_by(QuizAttempt.attempted_at.desc())
        .limit(limit)
        .all()
    ):
        student = User.query.get(attempt.student_id)
        events.append(
            {
                "type": "quiz",
                "at": attempt.attempted_at.isoformat(),
                "message": f"{student.name} scored {attempt.score_pct}% on a quiz",
            }
        )

    events.sort(key=lambda e: e["at"], reverse=True)
    return events[:limit]


@bp.post("")
@roles_required(Role.SCHOOL_ADMIN, Role.SUPER_ADMIN)
def create_class():
    data = request.get_json(force=True) or {}
    required = ["school_id", "name"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    cls = SchoolClass(
        school_id=data["school_id"],
        name=data["name"],
        teacher_id=data.get("teacher_id"),
        programme_id=data.get("programme_id"),
    )
    db.session.add(cls)
    db.session.commit()
    return jsonify(cls.to_dict()), 201


@bp.patch("/<int:class_id>")
@roles_required(Role.SCHOOL_ADMIN, Role.SUPER_ADMIN)
def update_class(class_id):
    """Class management — create, edit, assign teacher (§3.5)."""
    cls = SchoolClass.query.get_or_404(class_id)
    data = request.get_json(force=True) or {}
    for field in ("name", "teacher_id", "programme_id"):
        if field in data:
            setattr(cls, field, data[field])
    db.session.commit()
    return jsonify(cls.to_dict())
