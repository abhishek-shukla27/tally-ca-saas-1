"""
models/client.py
~~~~~~~~~~~~~~~~
SQLAlchemy ORM model for a commercial Client managed by a CA firm.
Each Client has a unique `api_sync_token` used by the desktop agent
to authenticate uploads via the X-Client-Token header.
"""

from __future__ import annotations

import datetime
import secrets

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


def _generate_token() -> str:
    """Generate a 48-character URL-safe random token."""
    return secrets.token_urlsafe(36)  # 36 bytes → 48-char base64url string


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    ca_id: Mapped[int] = mapped_column(
        ForeignKey("cas.id"), nullable=False, index=True
    )
    api_sync_token: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
        default=_generate_token,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    ca: Mapped["CA"] = relationship("CA", back_populates="clients")  # noqa: F821
    vouchers: Mapped[list["Voucher"]] = relationship(  # noqa: F821
        "Voucher", back_populates="client", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Client id={self.id} company_name={self.company_name!r}>"

