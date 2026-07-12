from datetime import datetime

from app.extensions import db


class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    owner_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=True)
    account_type = db.Column(db.String(20), nullable=False)  # individual|family|professional|school
    tier = db.Column(db.String(30), nullable=False, default="basic")
    status = db.Column(db.String(20), nullable=False, default="active")  # active|past_due|cancelled
    seats = db.Column(db.Integer, default=1)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    renewal_date = db.Column(db.DateTime, nullable=True)
    payment_provider = db.Column(db.String(20))  # paynow | stripe

    payments = db.relationship("Payment", backref="subscription", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "account_type": self.account_type,
            "tier": self.tier,
            "status": self.status,
            "seats": self.seats,
            "renewal_date": self.renewal_date.isoformat() if self.renewal_date else None,
            "payment_provider": self.payment_provider,
        }


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey("subscriptions.id"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(10), default="USD")  # USD via Stripe, ZiG/EcoCash via Paynow
    provider = db.Column(db.String(20), nullable=False)
    provider_reference = db.Column(db.String(120))
    status = db.Column(db.String(20), default="pending")  # pending|success|failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
