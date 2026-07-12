from flask import Blueprint, jsonify, send_file
from io import BytesIO
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import Certificate, User, Module
from app.utils.qrcodes import certificate_verify_url, generate_qr_png

bp = Blueprint("certificates", __name__)


@bp.get("/mine")
@jwt_required()
def my_certificates():
    """Certificate gallery in student profile (§3.7)."""
    student_id = int(get_jwt_identity())
    certs = Certificate.query.filter_by(student_id=student_id).order_by(Certificate.issued_at.desc()).all()
    return jsonify([c.to_dict() for c in certs])


@bp.get("/verify/<verification_code>")
def verify(verification_code):
    """Public certificate verification page backend — no auth required, per
    the QR code on the printed/downloaded certificate (§3.7)."""
    cert = Certificate.query.filter_by(verification_code=verification_code).first()
    if not cert:
        return jsonify({"valid": False}), 404

    student = User.query.get(cert.student_id)
    module = Module.query.get(cert.module_id)
    return jsonify(
        {
            "valid": True,
            "student_name": student.name,
            "module_title": module.title,
            "issued_at": cert.issued_at.isoformat(),
        }
    )


@bp.get("/<int:certificate_id>/qr.png")
def qr_code(certificate_id):
    cert = Certificate.query.get_or_404(certificate_id)
    url = certificate_verify_url(cert.verification_code)
    png_bytes = generate_qr_png(url)
    return send_file(BytesIO(png_bytes), mimetype="image/png")
