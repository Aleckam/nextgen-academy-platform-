from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

from app.models import Role


def roles_required(*allowed_roles: Role):
    """Restrict a route to one or more roles. Must be used under a JWT-protected
    route (calls verify_jwt_in_request itself, so @jwt_required() is optional
    but harmless above it).

    RBAC is enforced at the API layer for every school/admin/learner route,
    per the MVP requirement that RBAC be implemented from day one (§2).
    """

    allowed = {r.value if isinstance(r, Role) else r for r in allowed_roles}

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") not in allowed:
                return jsonify({"error": "forbidden", "message": "Insufficient role"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def same_school_or_super_admin(get_school_id):
    """Decorator factory ensuring a school_admin/teacher only touches their
    own school's data, unless they're a super_admin. `get_school_id(*args,
    **kwargs)` extracts the target school id from the route args."""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") == Role.SUPER_ADMIN.value:
                return fn(*args, **kwargs)
            target_school_id = get_school_id(*args, **kwargs)
            if claims.get("school_id") != target_school_id:
                return jsonify({"error": "forbidden", "message": "Wrong school"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
