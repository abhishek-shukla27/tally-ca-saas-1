# Tally-CA SaaS — Backend (Phase 2)

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.11+ |
| PostgreSQL | 14+ |

---

## 1. Create the database

```sql
-- Run once in psql
CREATE DATABASE tally_ca_saas;
```

---

## 2. Install dependencies

```bash
cd apps/backend

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

---

## 3. Configure environment

```bash
copy .env.example .env     # Windows
# or:  cp .env.example .env

# Then open .env and set DATABASE_URL to match your Postgres credentials:
# DATABASE_URL=postgresql://YOUR_USER:YOUR_PASS@localhost:5432/tally_ca_saas
```

---

## 4. Run the server

```bash
# From apps/backend/src/  (so relative imports resolve correctly)
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The app will:
- Auto-create all DB tables (`cas`, `clients`, `vouchers`) on first startup.
- Serve interactive docs at **http://localhost:8000/docs**

---

## 5. Seed a test CA + Client (psql)

```sql
-- Insert a CA firm
INSERT INTO cas (firm_name, email) VALUES ('Sharma & Associates', 'ca@sharma.com');

-- Insert a client with a known token (normally auto-generated)
INSERT INTO clients (company_name, ca_id, api_sync_token)
VALUES ('Ravi Enterprises Ltd', 1, 'test-token-abc123');
```

---

## 6. Test the upload endpoint

```bash
curl -X POST http://localhost:8000/api/v1/sync/upload \
  -H "Content-Type: application/json" \
  -H "X-Client-Token: test-token-abc123" \
  -d '{
    "data_type": "vouchers",
    "record_count": 1,
    "records": [{
      "guid": "vch-001",
      "date": "2024-04-15",
      "voucher_type": "Payment",
      "voucher_number": "PMT/2024/001",
      "party_ledger": "Cash",
      "amount": -15000.0,
      "is_cancelled": false,
      "narration": "Office supplies"
    }]
  }'
```

**Expected response:**
```json
{
  "status": "success",
  "message": "Data received",
  "client_id": 1,
  "company_name": "Ravi Enterprises Ltd",
  "data_type": "vouchers",
  "records_received": 1,
  "received_at": "..."
}
```

The full payload is also **printed to the server console** for inspection.

---

## File Structure

```
src/
├── main.py                  ← FastAPI app + startup
├── core/
│   ├── config.py            ← Settings (pydantic-settings, .env)
│   ├── database.py          ← SQLAlchemy engine + get_db dependency
│   └── security.py          ← X-Client-Token validation dependency
├── models/
│   ├── __init__.py          ← Re-exports Base, CA, Client, Voucher
│   ├── ca.py                ← CA firm ORM model
│   ├── client.py            ← Client + api_sync_token ORM model
│   └── voucher.py           ← Voucher transaction ORM model
└── api/
    ├── schemas.py            ← Pydantic v2 request/response schemas
    └── sync.py               ← POST /api/v1/sync/upload router
```
