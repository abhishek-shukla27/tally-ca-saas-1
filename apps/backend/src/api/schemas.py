"""
api/schemas.py
~~~~~~~~~~~~~~
Pydantic v2 request/response schemas for the sync upload endpoint.
These are separate from the SQLAlchemy ORM models on purpose —
the ORM models own the DB shape; schemas own the HTTP contract.
"""

from __future__ import annotations

import datetime
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Inbound – individual records sent by the desktop agent
# ---------------------------------------------------------------------------

class VoucherIn(BaseModel):
    """A single voucher record as received from the desktop sync agent."""

    guid: str = Field(..., description="Tally GUID — globally unique across companies.")
    date: str = Field(..., description="Voucher date in YYYY-MM-DD format.")
    voucher_type: str = Field(..., examples=["Payment", "Receipt", "Journal", "Sales"])
    voucher_number: str
    party_ledger: str | None = None
    amount: float = Field(..., description="Positive for Dr, negative for Cr (Tally convention).")
    is_cancelled: bool = False
    narration: str | None = None


class LedgerIn(BaseModel):
    """A single ledger master record."""

    guid: str
    name: str
    parent_group: str | None = None
    opening_balance: float = 0.0
    closing_balance: float = 0.0


class StockItemIn(BaseModel):
    """A single stock-item master record."""

    guid: str
    name: str
    parent_group: str | None = None
    base_units: str | None = None
    opening_quantity: float = 0.0
    opening_rate: float = 0.0
    opening_value: float = 0.0


# ---------------------------------------------------------------------------
# Inbound – top-level upload payload
# ---------------------------------------------------------------------------

class SyncUploadPayload(BaseModel):
    """
    Root payload POSTed by the desktop sync agent.
    `data_type` controls which record list is populated.
    """

    data_type: str = Field(
        ...,
        description="One of: 'vouchers', 'ledgers', 'stock_items'.",
        examples=["vouchers"],
    )
    record_count: int = Field(..., ge=0)
    records: list[dict[str, Any]] = Field(
        ...,
        description="Raw records; interpreted according to data_type.",
    )


# ---------------------------------------------------------------------------
# Outbound – standard API responses
# ---------------------------------------------------------------------------

class UploadResponse(BaseModel):
    status: str
    message: str
    client_id: int
    company_name: str
    data_type: str
    records_received: int
    received_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )

