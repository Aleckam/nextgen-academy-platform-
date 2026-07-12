from flask import Blueprint, jsonify

from app.models import User, Role, School, Subscription, Certificate, LessonProgress
from app.utils.rbac import roles_required

bp = Blueprint("admin", __name__)


@bp.get("/overview")
@roles_required(Role.SUPER_ADMIN)
def overview():
    """Admin dashboard overview + basic analytics dashboard (§3.2, Should Have)."""
    return jsonify(
        {
            "total_users": User.query.count(),
            "total_students": User.query.filter_by(role=Role.STUDENT).count(),
            "total_schools": School.query.count(),
            "active_subscriptions": Subscription.query.filter_by(status="active").count(),
            "certificates_issued": Certificate.query.count(),
            "lessons_completed": LessonProgress.query.filter_by(status="completed").count(),
        }
    )


@bp.get("/users")
@roles_required(Role.SUPER_ADMIN)
def list_users():
    """User account management (§3.2)."""
    from flask import request

    query = User.query
    role = request.args.get("role")
    if role:
        query = query.filter_by(role=Role(role))
    page = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 25)), 100)
    users = query.order_by(User.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
    return jsonify([u.to_dict(include_private=True) for u in users])


@bp.get("/schools")
@roles_required(Role.SUPER_ADMIN)
def list_schools():
    """School account management (§3.2)."""
    return jsonify([s.to_dict() for s in School.query.order_by(School.created_at.desc()).all()])
