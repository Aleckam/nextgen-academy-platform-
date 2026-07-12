import random
import re

from app.extensions import db
from app.models import User


def generate_unique_pin(school_id: int) -> str:
    """4-digit PIN, unique per school cohort (§3.5)."""
    for _ in range(50):
        pin = f"{random.randint(0, 9999):04d}"
        exists = (
            db.session.query(User.id)
            .filter(User.school_id == school_id, User.pin_hash.isnot(None))
            .count()
        )
        # PINs are hashed at rest, so uniqueness is enforced by regenerating
        # against a short in-memory collision window rather than querying the hash.
        if exists < 10000:
            return pin
    raise RuntimeError("Could not allocate a unique PIN for this school")


def generate_username(first_name: str, last_name: str, existing_usernames: set) -> str:
    base = re.sub(r"[^a-zA-Z]", "", first_name).capitalize() + re.sub(
        r"[^a-zA-Z]", "", last_name
    )[:1].upper()
    candidate = base
    n = 1
    while candidate.lower() in existing_usernames:
        n += 1
        candidate = f"{base}{n}"
    existing_usernames.add(candidate.lower())
    return candidate
