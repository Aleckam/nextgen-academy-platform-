import enum
import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class Role(str, enum.Enum):
    PARENT = "parent"
    STUDENT = "student"
    TEACHER = "teacher"
    SCHOOL_ADMIN = "school_admin"
    SUPER_ADMIN = "super_admin"


class AccountType(str, enum.Enum):
    INDIVIDUAL = "individual"
    FAMILY = "family"
    PROFESSIONAL = "professional"
    SCHOOL = "school"


class AgeGroup(str, enum.Enum):
    KIDS = "7-12"
    TEENS = "13-18"
    PROFESSIONAL = "professional"
    NA = "n/a"


class User(db.Model):
    """Covers every human on the platform: parents, professionals, students,
    teachers, school admins and NextGen super admins.

    Students onboarded via a school CSV upload authenticate with
    username + 4-digit PIN and have no email address (per MVP scope §3.1).
    Individually-subscribing learners (kids via a parent, teens, professionals)
    authenticate with email + password.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(Role), nullable=False, index=True)
    account_type = db.Column(db.Enum(AccountType), nullable=False)
    age_group = db.Column(db.Enum(AgeGroup), nullable=False, default=AgeGroup.NA)

    name = db.Column(db.String(120), nullable=False)
    profile_photo_url = db.Column(db.String(500))

    # Email + password path (parents, professionals, teachers, school admins, super admins)
    email = db.Column(db.String(255), unique=True, index=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)

    # PIN path (school-enrolled students — no email required)
    username = db.Column(db.String(80), index=True, nullable=True)
    pin_hash = db.Column(db.String(255), nullable=True)

    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey("school_classes.id"), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active_at = db.Column(db.DateTime, nullable=True)

    children = db.relationship("User", backref=db.backref("parent", remote_side=[id]))

    __table_args__ = (
        db.UniqueConstraint("school_id", "username", name="uq_username_per_school"),
    )

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return bool(self.password_hash) and check_password_hash(self.password_hash, raw_password)

    def set_pin(self, raw_pin: str) -> None:
        self.pin_hash = generate_password_hash(raw_pin)

    def check_pin(self, raw_pin: str) -> bool:
        return bool(self.pin_hash) and check_password_hash(self.pin_hash, raw_pin)

    def to_dict(self, include_private=False):
        data = {
            "id": self.id,
            "name": self.name,
            "role": self.role.value if self.role else None,
            "account_type": self.account_type.value if self.account_type else None,
            "age_group": self.age_group.value if self.age_group else None,
            "profile_photo_url": self.profile_photo_url,
            "school_id": self.school_id,
            "class_id": self.class_id,
            "is_active": self.is_active,
        }
        if include_private:
            data["email"] = self.email
            data["username"] = self.username
        return data

    def __repr__(self):
        return f"<User {self.id} {self.role}>"


class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    token = db.Column(db.String(64), unique=True, default=lambda: uuid.uuid4().hex, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
