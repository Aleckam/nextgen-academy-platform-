# NextGen Academy of Finance & AI — Platform

A subscription-based financial literacy platform for Zimbabwe, serving
three audiences from one codebase and one database: individual learners
(kids, teens, professionals), schools (bulk enrolment via CSV + PIN login),
and the NextGen team (content and user administration).

This repo is a full-stack scaffold built against `NextGen_MVP_Scope_Summary
_v1.0` and the four `WF01-04` wireframes. It is **not** the full 18-week
Phase 1 build — it's a working skeleton (real data model, real RBAC, real
auth, and the four wireframed screens fully wired end-to-end) meant to give
a developer team a running start. See `docs/SCREENS.md` for exactly what's
real vs. still a placeholder, and `docs/ARCHITECTURE.md` for the full
technical writeup.

## Quick start

```bash
# Backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python seed.py     # demo data: Redeemed Group of Schools, Form 2B
python run.py        # http://localhost:5000

# Frontend
cd frontend
npm install
npm run dev            # http://localhost:5173
```

Demo logins (after `python seed.py`):
- School admin — `peace@redeemedschools.co.zw` / `changeme`
- Super admin — `alec@nextgenacademy.co.zw` / `changeme`
- Students — created via the CSV upload flow at `/school/upload` (log in
  at `/login` → "Student Login (PIN)" with school code `1`)

Or: `docker compose up --build` for Postgres + backend + frontend together.

## What's built

- **Data model** covering every Phase 1 entity: users/RBAC, schools/classes,
  the Programme → Module → Lesson → Quiz content hierarchy, certificates,
  subscriptions/payments, blog.
- **Auth**: email/password for parents & professionals, PIN-only login for
  school students (no email required), JWT + role-based access control
  enforced at the API layer.
- **The four wireframed screens**, built as real React components against
  real Flask endpoints, verified end-to-end with a headless browser:
  - School Admin Dashboard (`WF01`)
  - Individual Class View (`WF02`)
  - CSV Student Upload + PIN Card flow (`WF03`)
  - Young Investors Lesson Player (`WF04`)
- **PDF generation** (WeasyPrint) for PIN cards and term reports, **QR
  codes** for certificate verification.
- **Routing + RBAC guards** for all ~32 Phase 1 screens across Public,
  Learner App, School Portal and Admin Panel — see `docs/SCREENS.md` for
  which are fully wired vs. still placeholders.

## What's not built yet

Paynow/Stripe checkout integration, the Content CMS admin UI (backend CRUD
exists), certificate template management, and the coin/streak/portfolio
gamification widgets (illustrative-only in this scaffold). Full list in
`docs/SCREENS.md`.

## Source material

- `docs/MVP scope summary` — see the original `NextGen_MVP_Scope_Summary`
  doc for the full Phase 1 spec this was built against.
- `docs/wireframes/` — the four original WF01-04 wireframes (PNG +
  interactive HTML) this build implements.
