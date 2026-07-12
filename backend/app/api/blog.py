from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import BlogPost, NewsletterSignup, Role
from app.utils.rbac import roles_required

bp = Blueprint("blog", __name__)


@bp.get("")
def list_posts():
    """Blog listing page — public, filterable by category (§3.6)."""
    query = BlogPost.query.filter_by(status="published")
    category = request.args.get("category")
    if category:
        query = query.filter_by(category=category)
    posts = query.order_by(BlogPost.published_at.desc()).all()
    return jsonify([p.to_dict() for p in posts])


@bp.get("/categories")
def categories():
    return jsonify(BlogPost.CATEGORIES)


@bp.get("/<slug>")
def get_post(slug):
    """Blog article page, incl. related articles widget (§3.6)."""
    post = BlogPost.query.filter_by(slug=slug, status="published").first_or_404()
    related = (
        BlogPost.query.filter(
            BlogPost.category == post.category, BlogPost.id != post.id, BlogPost.status == "published"
        )
        .limit(3)
        .all()
    )
    return jsonify({"post": post.to_dict(), "body": post.body, "related": [r.to_dict() for r in related]})


@bp.post("")
@roles_required(Role.SUPER_ADMIN)
def create_post():
    """Blog CMS — create, edit, publish articles (§3.6)."""
    data = request.get_json(force=True) or {}
    required = ["title", "slug", "category", "body"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    post = BlogPost(
        title=data["title"],
        slug=data["slug"],
        category=data["category"],
        author_id=int(get_jwt_identity()),
        excerpt=data.get("excerpt"),
        body=data["body"],
        status=data.get("status", "draft"),
        published_at=datetime.utcnow() if data.get("status") == "published" else None,
    )
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201


@bp.patch("/<int:post_id>")
@roles_required(Role.SUPER_ADMIN)
def update_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    data = request.get_json(force=True) or {}
    for field in ("title", "category", "excerpt", "body", "status"):
        if field in data:
            setattr(post, field, data[field])
    if data.get("status") == "published" and not post.published_at:
        post.published_at = datetime.utcnow()
    db.session.commit()
    return jsonify(post.to_dict())


@bp.post("/newsletter-signup")
def newsletter_signup():
    """Embedded in articles and homepage (§3.6)."""
    data = request.get_json(force=True) or {}
    email = (data.get("email") or "").strip().lower()
    if not email:
        return jsonify({"error": "email is required"}), 400
    if not NewsletterSignup.query.filter_by(email=email).first():
        db.session.add(NewsletterSignup(email=email))
        db.session.commit()
    return jsonify({"message": "Subscribed"}), 201
