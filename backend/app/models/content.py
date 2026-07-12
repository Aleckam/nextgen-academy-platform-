from datetime import datetime

from app.extensions import db


class Programme(db.Model):
    """Top of the content hierarchy: Programme -> Module -> Lesson -> Resource/Quiz."""

    __tablename__ = "programmes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    age_group = db.Column(db.String(20), nullable=False)  # "7-12", "13-18", "professional"
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)

    modules = db.relationship(
        "Module", backref="programme", order_by="Module.order", lazy="dynamic"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "age_group": self.age_group,
            "description": self.description,
        }


class Module(db.Model):
    __tablename__ = "modules"

    id = db.Column(db.Integer, primary_key=True)
    programme_id = db.Column(db.Integer, db.ForeignKey("programmes.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    order = db.Column(db.Integer, default=0)

    lessons = db.relationship("Lesson", backref="module", order_by="Lesson.order", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "programme_id": self.programme_id,
            "title": self.title,
            "order": self.order,
            "lesson_count": self.lessons.count(),
        }


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    order = db.Column(db.Integer, default=0)

    youtube_video_id = db.Column(db.String(50))  # unlisted YouTube embed, no self-hosting (§3.3)
    duration_seconds = db.Column(db.Integer, default=0)
    workbook_url = db.Column(db.String(500))  # downloadable PDF resource
    key_terms = db.Column(db.JSON, default=list)  # [{term, definition}], e.g. WF04 side panel
    required_tier = db.Column(db.String(30), default="free")  # locked/unlocked by subscription tier

    quiz = db.relationship("Quiz", backref="lesson", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "module_id": self.module_id,
            "title": self.title,
            "order": self.order,
            "youtube_video_id": self.youtube_video_id,
            "duration_seconds": self.duration_seconds,
            "workbook_url": self.workbook_url,
            "key_terms": self.key_terms or [],
            "required_tier": self.required_tier,
        }


class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False, unique=True)
    passing_score_pct = db.Column(db.Integer, default=60)  # 5 questions minimum (§3.3)
    coin_reward = db.Column(db.Integer, default=100)

    questions = db.relationship("QuizQuestion", backref="quiz", lazy="dynamic")


class QuizQuestion(db.Model):
    __tablename__ = "quiz_questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)

    choices = db.relationship("QuizChoice", backref="question", lazy="dynamic")


class QuizChoice(db.Model):
    __tablename__ = "quiz_choices"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("quiz_questions.id"), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)


class LessonProgress(db.Model):
    """Per-student resume/completion state — powers the Resume functionality
    and school-side per-student progress tables (WF02)."""

    __tablename__ = "lesson_progress"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)
    status = db.Column(db.String(20), default="locked")  # locked | in_progress | completed
    watched_seconds = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("student_id", "lesson_id", name="uq_progress_per_student_lesson"),
    )


class QuizAttempt(db.Model):
    __tablename__ = "quiz_attempts"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    score_pct = db.Column(db.Integer, nullable=False)
    passed = db.Column(db.Boolean, nullable=False)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
