"""PDF generation for the two Phase 1 documents (§6): PIN cards and term
reports. Uses WeasyPrint to render HTML/CSS to PDF, per the preferred stack.

Kept as pure functions returning bytes so routes can either stream the PDF
or upload it to S3/R2 and store the resulting URL.
"""
from io import BytesIO

from weasyprint import HTML

PIN_CARD_TEMPLATE = """
<html><head><style>
  body {{ font-family: sans-serif; }}
  .card {{ border: 2px solid #0a2540; border-radius: 8px; padding: 16px; margin-bottom: 12px; }}
  .header {{ color: #0a2540; font-weight: bold; font-size: 14px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
  th, td {{ text-align: left; padding: 6px; border-bottom: 1px solid #ddd; font-size: 12px; }}
</style></head><body>
  <div class="card">
    <div class="header">NextGen Academy of Finance &amp; AI — Student Login Cards</div>
    <div>{school_name} &middot; {class_name} &middot; {term_label}</div>
    <div style="font-size:11px;color:#555;margin-top:4px;">
      To log in: go to nextgen-academy.co.zw, click "Student Login", enter username and 4-digit PIN.
    </div>
    <table>
      <tr><th>Student name</th><th>Username</th><th>PIN</th></tr>
      {rows}
    </table>
  </div>
</body></html>
"""


def render_pin_cards_pdf(school_name: str, class_name: str, term_label: str, students: list) -> bytes:
    rows = "".join(
        f"<tr><td>{s['name']}</td><td>{s['username']}</td><td>{s['pin']}</td></tr>"
        for s in students
    )
    html = PIN_CARD_TEMPLATE.format(
        school_name=school_name, class_name=class_name, term_label=term_label, rows=rows
    )
    buf = BytesIO()
    HTML(string=html).write_pdf(buf)
    return buf.getvalue()


TERM_REPORT_TEMPLATE = """
<html><head><style>
  body {{ font-family: sans-serif; color: #0a2540; }}
  h1 {{ font-size: 18px; }}
  .stats {{ display: flex; gap: 16px; margin: 12px 0; }}
  .stat {{ border: 1px solid #ddd; padding: 10px; border-radius: 6px; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ text-align: left; padding: 6px; border-bottom: 1px solid #ddd; font-size: 12px; }}
</style></head><body>
  <h1>{school_name} — {term_label} Report</h1>
  <div class="stats">
    <div class="stat"><strong>{students_covered}</strong><div>Students covered</div></div>
    <div class="stat"><strong>{classes_included}</strong><div>Classes included</div></div>
    <div class="stat"><strong>{certificates_issued}</strong><div>Certificates issued</div></div>
    <div class="stat"><strong>{overall_completion}%</strong><div>Overall completion</div></div>
  </div>
  <table>
    <tr><th>Class</th><th>Students</th><th>Completion</th><th>Certificates</th></tr>
    {rows}
  </table>
</body></html>
"""


def render_term_report_pdf(school_name: str, term_label: str, summary: dict, class_rows: list) -> bytes:
    rows = "".join(
        f"<tr><td>{c['name']}</td><td>{c['student_count']}</td>"
        f"<td>{c['completion_pct']}%</td><td>{c['certificates']}</td></tr>"
        for c in class_rows
    )
    html = TERM_REPORT_TEMPLATE.format(
        school_name=school_name,
        term_label=term_label,
        rows=rows,
        **summary,
    )
    buf = BytesIO()
    HTML(string=html).write_pdf(buf)
    return buf.getvalue()
