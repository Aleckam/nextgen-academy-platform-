# Architecture

Scaffold for the NextGen Academy of Finance & AI MVP, built against
`NextGen_MVP_Scope_Summary_v1.0` and the four `wireframes_pkg` wireframes
(see `docs/wireframes/`). Section references below (`§3.1` etc.) point at
the scope document.

## Stack

| Layer | Choice |
|---|---|
| Frontend | React 19 + Vite + React Router |
| Backend | Flask 3 + SQLAlchemy + Flask-JWT-Extended |
| Database | PostgreSQL (SQLite for local dev, see `backend/app/config.py`) |
| PDF generation | WeasyPrint (PIN cards, term reports) |
| QR codes | `qrcode` (certificate verification) |

Matches the scope doc's preferred stack (§5), Flask chosen over Node per
the co-founder's stated Flask learning goal.

## Repo layout

```
backend/
  app/
    models/       identity, school, content, certificate, commerce, blog
    api/          one blueprint per domain (auth, schools, classes, content, ...)
    utils/        rbac, pin generation, csv import, pdf, qr
  seed.py         demo data matching the wireframes (Redeemed Group of Schools)
  run.py
frontend/
  src/
    pages/public/    Homepage, pricing, sign-up, login, blog, cert verify
    pages/learner/   age-tiered dashboards, lesson player, quiz, certificates
    pages/school/    admin dashboard, CSV upload+PIN cards, class view, roster
    pages/admin/     NextGen team CMS/admin screens
    components/      shared UI (Sidebar, StatCard, ProgressBar, Badge)
docs/
  wireframes/    original WF01-04 assets (PNG + interactive HTML)
```

## Data model

One database serves all three product faces, per the scope doc's "single
codebase, single database" requirement (§2). Key entities:

- **User** — every human on the platform. `role` (parent/student/teacher/
  school_admin/super_admin) drives RBAC; `account_type` (individual/family/
  professional/school) drives billing and dashboard variant. School-enrolled
  students authenticate via `username` + `pin_hash` (no email); everyone
  else via `email` + `password_hash`.
- **School / SchoolClass** — institution and class-cohort records.
- **Programme → Module → Lesson → Quiz** — the content hierarchy from §3.3,
  with `LessonProgress` and `QuizAttempt` tracking per-student state.
- **Certificate** — issued on module completion, carries a UUID
  `verification_code` for the public QR-verify page.
- **Subscription / Payment** — provider-agnostic; Paynow and Stripe both
  write through the same `POST /subscriptions/:id/payments` webhook shape.
- **BlogPost / NewsletterSignup** — content marketing (§3.6).

RBAC is enforced at the API layer (`app/utils/rbac.py`) on every route,
per the requirement that RBAC exist from day one (§2).

## Phase 2 accommodations

Per the scope doc's explicit ask (§4), nothing here blocks Phase 2 without
a rebuild:

- **ZSE/VFEX simulator** — `Subscription`/portfolio data isn't modeled yet;
  add a `PortfolioHolding` table keyed on `student_id` when that ships. The
  lesson player's "virtual portfolio" widget is illustrative-only for now.
- **React Native** — the frontend is a thin API client with no
  web-only assumptions baked into business logic; screens under
  `pages/learner/` are the ones a mobile app would need to reimplement.
  first.
- **Shona/Ndebele** — no strings are externalised into an i18n layer yet.
  This should happen before the frontend grows much further — retrofitting
  i18n across dozens of components is the expensive path.

## What's real vs. stubbed

The four wireframed screens (WF01-04) are fully wired end-to-end: real
backend endpoints, real database queries, real frontend components — see
`docs/SCREENS.md` for verification notes and how to reproduce the
end-to-end tests that were run against this scaffold.

Every other screen from the §7 list has a route and a page component so
navigation/RBAC is complete, but most have a `PlaceholderPage` or a
thin single-endpoint view rather than the full designed feature — see
inline comments in each `frontend/src/pages/**` file for what's real vs.
what's left, and `docs/SCREENS.md` for the master checklist.

## Running locally

```bash
# Backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # defaults to local SQLite if DATABASE_URL is unset
python seed.py          # creates demo data matching the wireframes
python run.py            # http://localhost:5000

# Frontend (new terminal)
cd frontend
npm install
cp .env.example .env
npm run dev               # http://localhost:5173
```

Demo logins after `python seed.py`:
- School admin: `peace@redeemedschools.co.zw` / `changeme`
- Super admin: `alec@nextgenacademy.co.zw` / `changeme`

Or with Docker: `docker compose up --build` (Postgres + backend + frontend).
