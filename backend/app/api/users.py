from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import User

bp = Blueprint("users", __name__)


@bp.get("/me")
@jwt_required()
def get_profile():
    user = User.query.get_or_404(int(get_jwt_identity()))
    return jsonify(user.to_dict(include_private=True))


@bp.patch("/me")
@jwt_required()
def update_profile():
    """Profile management — name, age group, profile photo (§3.1)."""
    user = User.query.get_or_404(int(get_jwt_identity()))
    data = request.get_json(force=True) or {}
    for field in ("name", "profile_photo_url"):
        if field in data:
            setattr(user, field, data[field])
    db.session.commit()
    return jsonify(user.to_dict(include_private=True))
