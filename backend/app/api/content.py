from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import (
    Role,
    Programme,
    Module,
    Lesson,
    Quiz,
    QuizQuestion,
    QuizChoice,
    LessonProgress,
    QuizAttempt,
    Certificate,
)
from app.utils.rbac import roles_required

bp = Blueprint("content", __name__)


# ---- Public/learner read endpoints -----------------------------------------

@bp.get("/programmes")
def list_programmes():
    """Module / course listing (§3.4). Public age_group filter e.g. ?age_group=13-18."""
    query = Programme.query.order_by(Programme.order)
    age_group = request.args.get("age_group")
    if age_group:
        query = query.filter_by(age_group=age_group)
    return jsonify([p.to_dict() for p in query.all()])


@bp.get("/programmes/<int:programme_id>/modules")
def list_modules(programme_id):
    modules = Module.query.filter_by(programme_id=programme_id).order_by(Module.order).all()
    return jsonify([m.to_dict() for m in modules])


@bp.get("/lessons/<int:lesson_id>")
@jwt_required()
def get_lesson(lesson_id):
    """Backs WF04 — Young Investors Lesson Player: video, key terms, quiz
    unlock state, and this student's resume position."""
    lesson = Lesson.query.get_or_404(lesson_id)
    student_id = int(get_jwt_identity())
    progress = LessonProgress.query.filter_by(student_id=student_id, lesson_id=lesson_id).first()

    module = Module.query.get(lesson.module_id)
    siblings = Module.query.get(lesson.module_id).lessons.order_by(Lesson.order).all()

    return jsonify(
        {
            "lesson": lesson.to_dict(),
            "module": module.to_dict(),
            "sibling_lessons": [
                {
                    **l.to_dict(),
                    "progress": _progress_summary(student_id, l.id),
                }
                for l in siblings
            ],
            "my_progress": {
                "status": progress.status if progress else "locked",
                "watched_seconds": progress.watched_seconds if progress else 0,
            },
            "quiz_id": lesson.quiz.id if lesson.quiz else None,
        }
    )


def _progress_summary(student_id, lesson_id):
    p = LessonProgress.query.filter_by(student_id=student_id, lesson_id=lesson_id).first()
    return {"status": p.status if p else "locked"}


@bp.put("/lessons/<int:lesson_id>/progress")
@jwt_required()
def update_progress(lesson_id):
    """Video lesson player auto-saves progress; powers 'Resume where you left
    off' (§3.3, §3.4)."""
    Lesson.query.get_or_404(lesson_id)
    student_id = int(get_jwt_identity())
    data = request.get_json(force=True) or {}

    progress = LessonProgress.query.filter_by(student_id=student_id, lesson_id=lesson_id).first()
    if not progress:
        progress = LessonProgress(student_id=student_id, lesson_id=lesson_id, status="in_progress")
        db.session.add(progress)

    progress.watched_seconds = max(progress.watched_seconds, data.get("watched_seconds", 0))
    if data.get("completed"):
        progress.status = "completed"
        progress.completed_at = datetime.utcnow()
    elif progress.status == "locked":
        progress.status = "in_progress"

    db.session.commit()
    return jsonify({"status": progress.status, "watched_seconds": progress.watched_seconds})


@bp.get("/quizzes/<int:quiz_id>")
@jwt_required()
def get_quiz(quiz_id):
    """Post-video quiz — 5 questions minimum, required before progression (§3.3)."""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions.all()
    return jsonify(
        {
            "id": quiz.id,
            "lesson_id": quiz.lesson_id,
            "passing_score_pct": quiz.passing_score_pct,
            "coin_reward": quiz.coin_reward,
            "questions": [
                {
                    "id": q.id,
                    "question_text": q.question_text,
                    "choices": [{"id": c.id, "text": c.text} for c in q.choices],
                }
                for q in questions
            ],
        }
    )


@bp.post("/quizzes/<int:quiz_id>/attempt")
@jwt_required()
def submit_quiz_attempt(quiz_id):
    """Grades a quiz attempt, unlocks the next lesson on pass, and issues a
    certificate if this was the module's final quiz."""
    quiz = Quiz.query.get_or_404(quiz_id)
    student_id = int(get_jwt_identity())
    data = request.get_json(force=True) or {}
    answers = data.get("answers", {})  # {question_id: choice_id}

    questions = quiz.questions.all()
    correct = 0
    for q in questions:
        chosen_id = answers.get(str(q.id))
        correct_choice = next((c for c in q.choices if c.is_correct), None)
        if correct_choice and chosen_id == correct_choice.id:
            correct += 1

    score_pct = round((correct / len(questions)) * 100) if questions else 0
    passed = score_pct >= quiz.passing_score_pct

    attempt = QuizAttempt(student_id=student_id, quiz_id=quiz_id, score_pct=score_pct, passed=passed)
    db.session.add(attempt)

    certificate_issued = None
    if passed:
        lesson = Lesson.query.get(quiz.lesson_id)
        module = Module.query.get(lesson.module_id)
        module_lessons = module.lessons.all()
        all_done = all(
            LessonProgress.query.filter_by(
                student_id=student_id, lesson_id=l.id, status="completed"
            ).first()
            for l in module_lessons
            if l.id != lesson.id
        )
        if all_done and not Certificate.query.filter_by(student_id=student_id, module_id=module.id).first():
            cert = Certificate(student_id=student_id, module_id=module.id)
            db.session.add(cert)
            db.session.flush()
            certificate_issued = cert.to_dict()

    db.session.commit()
    return jsonify(
        {
            "score_pct": score_pct,
            "passed": passed,
            "coin_reward": quiz.coin_reward if passed else 0,
            "certificate_issued": certificate_issued,
        }
    )


# ---- Admin CMS endpoints (Content CMS — lessons & quizzes, §3.2) -----------

@bp.post("/programmes")
@roles_required(Role.SUPER_ADMIN)
def create_programme():
    data = request.get_json(force=True) or {}
    required = ["title", "age_group"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400
    programme = Programme(title=data["title"], age_group=data["age_group"], description=data.get("description", ""))
    db.session.add(programme)
    db.session.commit()
    return jsonify(programme.to_dict()), 201


@bp.post("/modules")
@roles_required(Role.SUPER_ADMIN)
def create_module():
    data = request.get_json(force=True) or {}
    if not data.get("programme_id") or not data.get("title"):
        return jsonify({"error": "programme_id and title are required"}), 400
    module = Module(programme_id=data["programme_id"], title=data["title"], order=data.get("order", 0))
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201


@bp.post("/lessons")
@roles_required(Role.SUPER_ADMIN)
def create_lesson():
    data = request.get_json(force=True) or {}
    if not data.get("module_id") or not data.get("title"):
        return jsonify({"error": "module_id and title are required"}), 400
    lesson = Lesson(
        module_id=data["module_id"],
        title=data["title"],
        order=data.get("order", 0),
        youtube_video_id=data.get("youtube_video_id"),
        duration_seconds=data.get("duration_seconds", 0),
        workbook_url=data.get("workbook_url"),
        key_terms=data.get("key_terms", []),
        required_tier=data.get("required_tier", "free"),
    )
    db.session.add(lesson)
    db.session.commit()
    return jsonify(lesson.to_dict()), 201


@bp.post("/lessons/<int:lesson_id>/quiz")
@roles_required(Role.SUPER_ADMIN)
def create_quiz(lesson_id):
    """Post-video quiz — 5 questions minimum, required before progression (§3.3)."""
    Lesson.query.get_or_404(lesson_id)
    data = request.get_json(force=True) or {}
    questions = data.get("questions", [])
    if len(questions) < 5:
        return jsonify({"error": "A quiz requires at least 5 questions"}), 400

    quiz = Quiz(
        lesson_id=lesson_id,
        passing_score_pct=data.get("passing_score_pct", 60),
        coin_reward=data.get("coin_reward", 100),
    )
    db.session.add(quiz)
    db.session.flush()

    for i, q in enumerate(questions):
        question = QuizQuestion(quiz_id=quiz.id, question_text=q["question_text"], order=i)
        db.session.add(question)
        db.session.flush()
        for choice in q.get("choices", []):
            db.session.add(
                QuizChoice(question_id=question.id, text=choice["text"], is_correct=choice.get("is_correct", False))
            )

    db.session.commit()
    return jsonify({"id": quiz.id, "lesson_id": lesson_id}), 201
