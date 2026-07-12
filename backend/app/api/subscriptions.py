from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.extensions import db
from app.models import Subscription, Payment, Role
from app.utils.rbac import roles_required

bp = Blueprint("subscriptions", __name__)


@bp.get("/mine")
@jwt_required()
def my_subscription():
    """Subscription management screen for learners/parents; billing screen
    for school admins (§3.4, §3.5)."""
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    query = Subscription.query.filter_by(owner_user_id=user_id)
    if claims.get("role") == Role.SCHOOL_ADMIN.value and claims.get("school_id"):
        query = Subscription.query.filter_by(school_id=claims["school_id"])
    sub = query.order_by(Subscription.start_date.desc()).first()
    return jsonify(sub.to_dict() if sub else None)


@bp.post("")
@jwt_required()
def create_subscription():
    """Creates a pending subscription ahead of a Paynow (local) or Stripe
    (USD/diaspora) checkout — actual payment-provider integration happens
    in the payment webhook handlers (§6), stubbed here for Phase 1 build-out."""
    data = request.get_json(force=True) or {}
    required = ["account_type", "tier", "payment_provider"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    sub = Subscription(
        owner_user_id=int(get_jwt_identity()) if data["account_type"] != "school" else None,
        school_id=data.get("school_id"),
        account_type=data["account_type"],
        tier=data["tier"],
        seats=data.get("seats", 1),
        payment_provider=data["payment_provider"],
        status="pending",
    )
    db.session.add(sub)
    db.session.commit()
    return jsonify(sub.to_dict()), 201


@bp.post("/<int:subscription_id>/payments")
def record_payment(subscription_id):
    """Payment provider webhook target (Paynow result URL / Stripe webhook).
    Marks the subscription active on a successful payment (§6)."""
    Subscription.query.get_or_404(subscription_id)
    data = request.get_json(force=True) or {}
    payment = Payment(
        subscription_id=subscription_id,
        amount=data.get("amount", 0),
        currency=data.get("currency", "USD"),
        provider=data.get("provider", "unknown"),
        provider_reference=data.get("provider_reference"),
        status=data.get("status", "pending"),
    )
    db.session.add(payment)

    if payment.status == "success":
        sub = Subscription.query.get(subscription_id)
        sub.status = "active"

    db.session.commit()
    return jsonify({"payment_id": payment.id, "status": payment.status}), 201


@bp.get("/admin")
@roles_required(Role.SUPER_ADMIN)
def list_all_subscriptions():
    """Subscription & billing admin, payment reconciliation (§3.2)."""
    subs = Subscription.query.order_by(Subscription.start_date.desc()).limit(100).all()
    return jsonify([s.to_dict() for s in subs])
