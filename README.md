# Tally-CA SaaS

> A multi-tenant B2B SaaS platform that automatically extracts financial data from clients' local TallyPrime instances, pushes it securely to the cloud, and exposes a comprehensive compliance and audit dashboard for Chartered Accountant (CA) firms.

---

## Project Structure

```
tally-ca-saas/
├── apps/
│   ├── desktop-client/        # Phase 1 – Python Tally sync agent
│   │   ├── src/
│   │   │   ├── tally_client.py    # Core sync script + mock harness
│   │   │   ├── scheduler.py       # APScheduler background runner
│   │   │   └── core/
│   │   │       ├── tally_queries.py   # XML envelope builders
│   │   │       └── xml_parser.py      # XML → JSON converters
│   │   └── requirements.txt
│   ├── backend/               # Phase 2 – FastAPI ingestion engine  ← LIVE
│   │   ├── src/
│   │   │   ├── main.py            # FastAPI app entry-point
│   │   │   ├── core/
│   │   │   │   ├── config.py      # Pydantic settings (.env loader)
│   │   │   │   ├── database.py    # SQLAlchemy engine + get_db
│   │   │   │   └── security.py    # X-Client-Token auth dependency
│   │   │   ├── models/
│   │   │   │   ├── ca.py          # CA firm ORM model
│   │   │   │   ├── client.py      # Client + api_sync_token model
│   │   │   │   └── voucher.py     # Voucher transaction model
│   │   │   └── api/
│   │   │       ├── schemas.py     # Pydantic v2 request/response shapes
│   │   │       └── sync.py        # POST /api/v1/sync/upload router
│   │   ├── .env                   # Local environment config (gitignored)
│   │   ├── .env.example
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── web-dashboard/         # Phase 4 – Next.js CA portal
│       └── src/
│           ├── app/
│           └── components/
├── PROJECT_STATUS.md          # Live build log + future goals
└── plan.md                    # Original project blueprint
```

---

## Build Status

| Phase | Component | Status |
|-------|-----------|--------|
| 1 | Desktop Client — Tally XML extraction & upload | ✅ Complete |
| 2 | Backend — FastAPI + PostgreSQL ingestion API | ✅ Complete |
| 3 | Audit Compliance Rules Engine | 🔲 Up Next |
| 4 | Next.js CA Dashboard | 🔲 Planned |

---

## Quick Start

### Phase 1 — Desktop Sync Client

```bash
cd apps/desktop-client
pip install -r requirements.txt
python src/tally_client.py --mock       # offline self-test (no Tally needed)
python src/tally_client.py --sync all   # live sync against TallyPrime
python src/scheduler.py                 # run on a schedule (every 60 min)
```

### Phase 2 — Backend API

```bash
cd apps/backend
pip install -r requirements.txt
# Edit .env → set DATABASE_URL with your Postgres credentials
cd src
python -m uvicorn main:app --reload --port 8000
```

**Interactive docs →** http://localhost:8000/docs

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Desktop Agent | Python 3.11+, `requests`, `apscheduler`, `xml.etree` |
| Backend API | FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic |
| Database | PostgreSQL 14+ |
| Web Dashboard *(planned)* | Next.js 14, TailwindCSS, Shadcn/ui, Tremor Charts |
| Packaging | PyInstaller (desktop), Docker (backend) |

---

## Documentation

- [`plan.md`](./plan.md) — Original architecture blueprint
- [`PROJECT_STATUS.md`](./PROJECT_STATUS.md) — Live build log, what's working, and future goals
- [`apps/backend/README.md`](./apps/backend/README.md) — Backend setup & API usage guide
- [`apps/desktop-client/README.md`](./apps/desktop-client/README.md) — Desktop client setup & CLI reference
