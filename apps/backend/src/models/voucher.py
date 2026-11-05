"""
models/voucher.py
~~~~~~~~~~~~~~~~~
SQLAlchemy ORM model for a financial Voucher synced from TallyPrime.
Each Voucher belongs to a Client and stores the core transaction fields.
"""

from __future__ import annotations

import datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Voucher(Base):
    __tablename__ = "vouchers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign key — which company does this voucher belong to?
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"), nullable=False, index=True
    )

    # Tally-side identity — used for idempotent upserts
    tally_guid: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )

    # Core transaction fields
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    voucher_type: Mapped[str] = mapped_column(String(100), nullable=False)
    voucher_number: Mapped[str] = mapped_column(String(100), nullable=False)
    party_ledger: Mapped[str | None] = mapped_column(String(255), nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    is_cancelled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    narration: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # Audit timestamps
    synced_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    client: Mapped["Client"] = relationship(  # noqa: F821
        "Client", back_populates="vouchers"
    )

    def __repr__(self) -> str:
        return (
            f"<Voucher id={self.id} type={self.voucher_type!r} "
            f"number={self.voucher_number!r} amount={self.amount}>"
        )
