# Project Plan: Tally Data Extraction & CA Dashboard SaaS

## Objective
Build a multi-tenant B2B SaaS platform that automatically extracts financial data from clients' local TallyPrime instances, pushes it securely to the cloud, and exposes a comprehensive compliance and audit dashboard for Chartered Accountant (CA) firms.

---

## 1. System Architecture Matrix

### Component A: Tally-Sync Desktop Client (`/apps/desktop-client`)
*   **Tech Stack:** Python 3.11+, PySide6 (for tray UI), `requests`, `apscheduler`, `PyInstaller`.
*   **Responsibility:** 
    *   Runs as a lightweight system tray application on the client's Windows system.
    *   Pings `http://localhost:9000` via XML queries at scheduled intervals (e.g., every 1 hour).
    *   Transforms raw Tally XML payloads directly into compressed JSON.
    *   Pushes JSON payloads via outbound HTTPS `POST` to the Cloud Backend API along with an `X-Client-Token`.

### Component B: Backend API Engine (`/apps/backend`)
*   **Tech Stack:** FastAPI, Pydantic v2, SQLAlchemy, PostgreSQL, Alembic.
*   **Responsibility:**
    *   Exposes ingestion endpoints for the desktop sync client (`/api/v1/sync/upload`).
    *   Validates device tokens and maps incoming data to the respective CA's workspace client ID.
    *   Parses incoming financial structures (Ledgers, Vouchers, Stock Items).
    *   Runs rule-based automated audit compliance checks (e.g., flagging transactions violating Income Tax Section 40A(3) for cash payments > ₹10,000, checking invalid GSTIN formats).

### Component C: CA Web Portal (`/apps/web-dashboard`)
*   **Tech Stack:** Next.js (App Router), TailwindCSS, Shadcn/ui, Tremor Charts, Lucide Icons.
*   **Responsibility:**
    *   Multi-tenant portal for CA firms to log in and manage all onboarded clients.
    *   Displays real-time financial health KPIs (P&L tracking, Balance Sheets, Debtors Aging).
    *   Provides dedicated compliance screens filtering all anomalous vouchers flagged by the backend engine.

---

## 2. Directory Layout
```text
tally-ca-saas/
├── apps/
│   ├── desktop-client/      # Python Desktop Utility
│   │   ├── src/
│   │   │   ├── core/        # Tally XML queries & XML-to-JSON parsers
│   │   │   ├── gui/         # System tray application layout
│   │   │   └── scheduler.py # Background task orchestration
│   │   └── requirements.txt
│   ├── backend/             # FastAPI Engine
│   │   ├── src/
│   │   │   ├── api/         # Routes (sync ingestion, dashboard data, auth)
│   │   │   ├── core/        # Audit logic & engine rules
│   │   │   ├── models/      # Postgres schemas via SQLAlchemy
│   │   │   └── main.py
│   │   └── Dockerfile
│   └── web-dashboard/       # Next.js Application
│       ├── src/
│       │   ├── app/         # Dashboard pages (Overview, Clients, Compliance)
│       │   └── components/  # Reusable UI elements (Shadcn)
```

---

## 3. Database Schema Blueprint (PostgreSQL)
*   **`users / cas`**: Stores CA firm credentials, subscription profiles, and global settings.
*   **`clients`**: Maps specific commercial clients to their respective governing CA firm. Generates unique secure `api_sync_token` values.
*   **`ledgers`**: Stores parent ledger details sync targets (`guid`, `name`, `parent_group`, `opening_balance`, `current_balance`).
*   **`vouchers`**: Detailed line-item logging (`guid`, `date`, `voucher_type`, `voucher_number`, `amount`, `is_cancelled`).
*   **`voucher_ledger_entries`**: Breakdowns of split accounting allocations per transaction (Dr/Cr tags).
*   **`audit_flags`**: Tracks rule-engine alerts linked to specific `voucher_id` entries with severity ratings (Info, Warning, Critical).

---

## 4. Phased Implementation Prompts for AI Integration

### Phase 1: Core Tally Request Envelopes & Ingestion Tests
> **Prompt for AI:** Generate a Python script (`tally_client.py`) that constructs an XML HTTP POST envelope to request a full list of Company Ledgers from `http://localhost:9000`. Include functions to safely convert the resulting Tally XML into standard flat JSON format using `xml.etree.ElementTree`. Provide mock Tally XML data to verify functionality without a live Tally instance.

### Phase 2: High-Performance FastAPI Backend Engine
> **Prompt for AI:** Setup a FastAPI project skeleton with a multi-tenant PostgreSQL schema configuration using SQLAlchemy. Define structural database models for `CA`, `Client`, `Ledger`, `Voucher`, and `AuditFlag`. Generate a `/api/v1/sync/vouchers` ingestion route equipped with a custom security dependency that validates an inbound `X-Client-Token`.

### Phase 3: Regulatory Audit Compliance Rules
> **Prompt for AI:** Build a data validation engine module in Python for our backend. Write automated audit scanning functions that evaluate incoming JSON arrays of Vouchers. The function must flag: (1) Cash ledger payments exceeding ₹10,000 in a single voucher, (2) Transactions where the recorded GSTIN fails regex validation, and (3) Vouchers creating a negative cash ledger threshold balance. Write entries into the `AuditFlag` schema table.

### Phase 4: Next.js + Shadcn Audit Desk Portal
> **Prompt for AI:** Build a modern Next.js client management dashboard layout using Tailwind CSS. It must include a sidebar with: "Overview", "Clients", "Audit & Compliance Flags", and "Settings". Use mock state matrices to display an operational overview of onboarded companies, showing their last sync timestamps and total active critical audit alerts.
