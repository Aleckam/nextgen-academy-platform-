import uuid
from datetime import datetime

from app.extensions import db


class Certificate(db.Model):
    """Auto-generated on module completion. QR code links to the public
    certificate verification page (§3.7)."""

    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id"), nullable=False)
    verification_code = db.Column(
        db.String(36), unique=True, default=lambda: str(uuid.uuid4()), nullable=False
    )
    pdf_url = db.Column(db.String(500))
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "module_id": self.module_id,
            "verification_code": self.verification_code,
            "pdf_url": self.pdf_url,
            "issued_at": self.issued_at.isoformat() if self.issued_at else None,
        }
