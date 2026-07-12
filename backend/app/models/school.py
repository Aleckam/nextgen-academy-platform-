from datetime import datetime

from app.extensions import db


class School(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    admin_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    term_label = db.Column(db.String(50), default="Term 1")
    academic_year = db.Column(db.Integer, default=lambda: datetime.utcnow().year)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    classes = db.relationship("SchoolClass", backref="school", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "term_label": self.term_label,
            "academic_year": self.academic_year,
        }


class SchoolClass(db.Model):
    """A single class/cohort within a school, e.g. 'Form 2B — Young Investors'."""

    __tablename__ = "school_classes"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    programme_id = db.Column(db.Integer, db.ForeignKey("programmes.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    students = db.relationship(
        "User", backref="school_class", lazy="dynamic", foreign_keys="User.class_id"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "school_id": self.school_id,
            "name": self.name,
            "teacher_id": self.teacher_id,
            "programme_id": self.programme_id,
            "student_count": self.students.count(),
        }
