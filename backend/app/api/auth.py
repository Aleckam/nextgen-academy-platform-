from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)

from app.extensions import db
from app.models import User, Role, AccountType, AgeGroup, PasswordResetToken

bp = Blueprint("auth", __name__)


def _claims_for(user: User) -> dict:
    return {"role": user.role.value, "school_id": user.school_id}


def _issue_tokens(user: User):
    identity = str(user.id)
    claims = _claims_for(user)
    return {
        "access_token": create_access_token(identity=identity, additional_claims=claims),
        "refresh_token": create_refresh_token(identity=identity, additional_claims=claims),
        "user": user.to_dict(include_private=True),
    }


@bp.post("/register")
def register():
    """Email/password registration for parents and professionals (§3.1).
    School and student accounts are provisioned separately (see /schools
    and the CSV upload flow) rather than through public self-registration.
    """
    data = request.get_json(force=True) or {}
    required = ["email", "password", "name", "account_type"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if User.query.filter_by(email=data["email"].lower()).first():
        return jsonify({"error": "An account with this email already exists"}), 409

    try:
        account_type = AccountType(data["account_type"])
    except ValueError:
        return jsonify({"error": "Invalid account_type"}), 400

    role = Role.PARENT if account_type in (AccountType.INDIVIDUAL, AccountType.FAMILY) else Role.PARENT
    if account_type == AccountType.PROFESSIONAL:
        role = Role.STUDENT  # professionals consume content directly, so they hold the learner role

    user = User(
        email=data["email"].lower(),
        name=data["name"],
        role=role,
        account_type=account_type,
        age_group=AgeGroup.PROFESSIONAL if account_type == AccountType.PROFESSIONAL else AgeGroup.NA,
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify(_issue_tokens(user)), 201


@bp.post("/login")
def login():
    """Email/password login for parents, professionals, teachers, school
    admins and super admins."""
    data = request.get_json(force=True) or {}
    user = User.query.filter_by(email=(data.get("email") or "").lower()).first()
    if not user or not user.check_password(data.get("password", "")):
        return jsonify({"error": "Invalid email or password"}), 401
    if not user.is_active:
        return jsonify({"error": "Account is disabled"}), 403

    user.last_active_at = datetime.utcnow()
    db.session.commit()
    return jsonify(_issue_tokens(user))


@bp.post("/student-login")
def student_login():
    """PIN-based login for school students — no email required, works on any
    shared device (§3.1, WF03)."""
    data = request.get_json(force=True) or {}
    school_id = data.get("school_id")
    username = (data.get("username") or "").strip()
    pin = (data.get("pin") or "").strip()

    if not (school_id and username and pin):
        return jsonify({"error": "school_id, username and pin are required"}), 400

    user = User.query.filter_by(
        school_id=school_id, username=username, role=Role.STUDENT
    ).first()
    if not user or not user.check_pin(pin):
        return jsonify({"error": "Invalid username or PIN"}), 401

    user.last_active_at = datetime.utcnow()
    db.session.commit()
    return jsonify(_issue_tokens(user))


@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user = User.query.get_or_404(int(identity))
    access_token = create_access_token(identity=identity, additional_claims=_claims_for(user))
    return jsonify({"access_token": access_token})


@bp.get("/me")
@jwt_required()
def me():
    user = User.query.get_or_404(int(get_jwt_identity()))
    return jsonify(user.to_dict(include_private=True))


@bp.post("/password-reset/request")
def password_reset_request():
    """Kicks off the email-link password reset flow (§3.1). Token creation
    only — actual email delivery is a SendGrid/Mailgun integration (§6)."""
    data = request.get_json(force=True) or {}
    user = User.query.filter_by(email=(data.get("email") or "").lower()).first()
    if user:
        token = PasswordResetToken(
            user_id=user.id, expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        db.session.add(token)
        db.session.commit()
        current_app.logger.info("Password reset token for %s: %s", user.email, token.token)
    # Always 200 — do not leak whether an email exists.
    return jsonify({"message": "If that email exists, a reset link has been sent."})


@bp.post("/password-reset/confirm")
def password_reset_confirm():
    data = request.get_json(force=True) or {}
    token = PasswordResetToken.query.filter_by(token=data.get("token")).first()
    if not token or token.used or token.expires_at < datetime.utcnow():
        return jsonify({"error": "Invalid or expired token"}), 400

    user = User.query.get_or_404(token.user_id)
    user.set_password(data.get("password", ""))
    token.used = True
    db.session.commit()
    return jsonify({"message": "Password updated"})
