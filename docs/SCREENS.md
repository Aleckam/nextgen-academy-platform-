# Screen checklist (Phase 1, §7 of the scope doc)

Legend: ✅ wired to real backend endpoints and verified · 🟡 route + page
exist, partial/mock data · ⬜ placeholder only

## Public

| Screen | Status | Notes |
|---|---|---|
| Homepage | 🟡 | `pages/public/HomePage.jsx` — static marketing page |
| Programme pages (×4 age groups) | 🟡 | `pages/public/ProgrammePage.jsx` — fetches real `/content/programmes` |
| Pricing page | 🟡 | Static tier cards |
| Sign-up flow (3 steps) | 🟡 | Collapsed to 1 step in `SignUpPage.jsx`; hits real `/auth/register` |
| Login page (adult + student PIN) | ✅ | `LoginPage.jsx` — both auth paths verified end-to-end |
| Blog listing page | ✅ | Real `/blog` fetch |
| Blog article page | ✅ | Real `/blog/:slug`, related articles, newsletter signup |
| Certificate verification page | ✅ | Real `/certificates/verify/:code` |

## Learner App

| Screen | Status | Notes |
|---|---|---|
| Kids dashboard (7-12) | 🟡 | Real certificate count; coin balance/streak need a wallet table |
| Teen dashboard (13-18) | 🟡 | Real programme list; portfolio widget is illustrative-only |
| Professional dashboard | 🟡 | Real programme list |
| Parent dashboard | 🟡 | Real subscription; child progress list needs a join query |
| Video lesson player | ✅ | **WF04** — verified end-to-end incl. progress auto-save |
| Post-lesson quiz | ✅ | Real quiz fetch, grading, coin reward, certificate issuance |
| Module / course listing | 🟡 | Real programme/module fetch |
| Certificate page | ✅ | Real `/certificates/mine` + QR image |
| Profile & settings | ✅ | Real `/users/me` GET/PATCH |
| Payment & subscription screen | 🟡 | Real subscription read; Paynow/Stripe checkout not implemented |

## School Portal

| Screen | Status | Notes |
|---|---|---|
| School admin dashboard | ✅ | **WF01** — verified end-to-end (stats, classes, inactive alerts, term report PDF) |
| CSV upload + PIN card flow | ✅ | **WF03** — verified end-to-end (parse, preview, confirm, PDF download) |
| Individual class view | ✅ | **WF02** — verified end-to-end (module strip, roster, activity feed) |
| Student roster management | 🟡 | Needs a dedicated `/schools/:id/students` list endpoint |
| Teacher dashboard (read-only) | 🟡 | Links into class view; needs "my class" resolution from JWT |
| Term report download | ✅ | One-click PDF, backs the dashboard's "Download Term Report" button |
| School subscription / billing | 🟡 | Real subscription read only |

## Admin Panel

| Screen | Status | Notes |
|---|---|---|
| Admin dashboard overview | ✅ | Real `/admin/overview` counters |
| Content CMS — lessons & quizzes | ⬜ | Backend CRUD is live (`/content/programmes`, `/modules`, `/lessons`, `/lessons/:id/quiz`); no admin form UI yet |
| Blog CMS | ✅ | Create/publish form wired to real `/blog` POST |
| User management | ✅ | Real `/admin/users` list |
| School account management | ✅ | Real `/admin/schools` list + create |
| Subscription & billing admin | ✅ | Real `/subscriptions/admin` list |
| Certificate template management | ⬜ | Not started — see comment in `CertificateTemplateManagement.jsx` |
| Basic analytics dashboard | ⬜ | Points at Admin Overview; needs time-series endpoints |

## What "verified end-to-end" means

The four wireframed screens (WF01-04) were smoke-tested with a headless
browser against the real Flask backend + seeded demo data (Redeemed Group
of Schools, Form 2B — Young Investors), covering:

1. School admin login → dashboard stats, classes table, inactive alerts
2. Dashboard → class view drill-down (module progress, roster, activity feed)
3. CSV upload → validation preview → confirm → PIN generation → PDF download
4. Student PIN login (username + PIN, no email) → age-tiered dashboard
5. Lesson player (WF04 lesson: "How the Zimbabwe Stock Exchange actually
   works") → key terms, progress auto-save, quiz unlock

Term report and PIN card PDF generation were also verified directly
(`WeasyPrint`, pinned to `pydyf==0.11.0` — the newer 0.12.x release breaks
WeasyPrint 62.3's PDF stream transform).
