import csv
import io

REQUIRED_COLUMNS = ["first_name", "last_name", "class_name"]
OPTIONAL_COLUMNS = ["student_id", "age_group"]

# Accept the human-friendly header labels shown in WF03 as well as snake_case.
HEADER_ALIASES = {
    "first name": "first_name",
    "last name": "last_name",
    "class name": "class_name",
    "student id": "student_id",
    "age group": "age_group",
}


def _normalise_header(h: str) -> str:
    h = h.strip().lower()
    return HEADER_ALIASES.get(h, h.replace(" ", "_"))


def parse_student_csv(file_stream) -> dict:
    """Parses the school CSV upload (WF03), returning valid rows plus
    per-row errors so the admin can review before confirming.
    """
    text = file_stream.read()
    if isinstance(text, bytes):
        text = text.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    reader.fieldnames = [_normalise_header(h) for h in (reader.fieldnames or [])]

    missing_columns = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
    if missing_columns:
        return {"error": f"Missing required columns: {', '.join(missing_columns)}"}

    valid_rows, error_rows = [], []
    seen = set()
    for i, row in enumerate(reader, start=2):  # row 1 is the header
        first = (row.get("first_name") or "").strip()
        last = (row.get("last_name") or "").strip()
        class_name = (row.get("class_name") or "").strip()

        errors = []
        if not first:
            errors.append("First name missing")
        if not last:
            errors.append("Last name missing")
        if not class_name:
            errors.append("Class name missing")

        key = (first.lower(), last.lower(), class_name.lower())
        if key in seen and not errors:
            errors.append("Duplicate row")
        seen.add(key)

        record = {
            "row": i,
            "first_name": first,
            "last_name": last,
            "class_name": class_name,
            "student_id": (row.get("student_id") or "").strip() or None,
            "age_group": (row.get("age_group") or "").strip() or None,
        }
        if errors:
            record["errors"] = errors
            error_rows.append(record)
        else:
            valid_rows.append(record)

    return {
        "valid_rows": valid_rows,
        "error_rows": error_rows,
        "total": len(valid_rows) + len(error_rows),
    }
