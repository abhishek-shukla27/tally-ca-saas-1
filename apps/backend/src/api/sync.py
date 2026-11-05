"""
api/sync.py
~~~~~~~~~~~
Router: POST /api/v1/sync/upload

This endpoint:
  1. Requires the X-Client-Token header (validated by get_current_client).
  2. Accepts the compressed JSON payload from the desktop sync agent.
  3. Prints the payload to the console (Phase 2 — persistence in Phase 3).
  4. Returns a structured success response.
"""

from __future__ import annotations

import json
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.schemas import SyncUploadPayload, UploadResponse
from core.database import get_db
from core.security import get_current_client
from models.client import Client

log = logging.getLogger("sync_router")

router = APIRouter(prefix="/api/v1/sync", tags=["Sync Ingestion"])


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_200_OK,
    summary="Receive a Tally data payload from the desktop sync agent",
    description=(
        "Authenticated via `X-Client-Token` header. "
        "Accepts ledger, voucher, or stock-item records synced from TallyPrime. "
        "Phase 2: logs the payload. Phase 3 will persist it to PostgreSQL."
    ),
)
def upload_tally_data(
    payload: SyncUploadPayload,
    current_client: Annotated[Client, Depends(get_current_client)],
    db: Annotated[Session, Depends(get_db)],
) -> UploadResponse:
    """
    Main ingestion endpoint.

    - Authenticates the request via X-Client-Token → resolves to a Client row.
    - Logs the full incoming payload to stdout (pretty-printed JSON).
    - Returns a structured acknowledgement.
    """
    # ── Pretty-print the incoming payload to the console ────────────────────
    log.info(
        "Received upload from client_id=%d  company=%r  data_type=%r  records=%d",
        current_client.id,
        current_client.company_name,
        payload.data_type,
        payload.record_count,
    )
    print("\n" + "=" * 72)
    print(f"  INCOMING PAYLOAD  |  Company: {current_client.company_name}")
    print(f"  Client ID : {current_client.id}")
    print(f"  CA ID     : {current_client.ca_id}")
    print(f"  Data Type : {payload.data_type}")
    print(f"  Records   : {payload.record_count}")
    print("-" * 72)
    print(json.dumps(payload.model_dump(), indent=2, ensure_ascii=False, default=str))
    print("=" * 72 + "\n")

    # ── Phase 3 hook: persistence will go here ───────────────────────────────
    # e.g. bulk_insert_vouchers(db, current_client.id, payload.records)

    return UploadResponse(
        status="success",
        message="Data received",
        client_id=current_client.id,
        company_name=current_client.company_name,
        data_type=payload.data_type,
        records_received=len(payload.records),
    )


@router.get(
    "/health",
    tags=["Health"],
    summary="Sync router health check",
    include_in_schema=False,
)
def sync_health() -> dict:
    return {"status": "ok", "router": "sync"}

