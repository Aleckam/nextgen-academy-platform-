"""QR generation for certificate verification (§3.7, §6)."""
from io import BytesIO

import qrcode

from flask import current_app


def certificate_verify_url(verification_code: str) -> str:
    base = current_app.config["CERT_VERIFY_BASE_URL"].rstrip("/")
    return f"{base}/{verification_code}"


def generate_qr_png(data: str) -> bytes:
    img = qrcode.make(data)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
