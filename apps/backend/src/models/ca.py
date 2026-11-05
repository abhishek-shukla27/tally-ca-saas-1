"""
models/ca.py
~~~~~~~~~~~~
SQLAlchemy ORM model for a Chartered Accountant (CA) firm.
One CA firm can manage many Clients.
"""

from __future__ import annotations

import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class CA(Base):
    __tablename__ = "cas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    firm_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    clients: Mapped[list["Client"]] = relationship(  # noqa: F821
        "Client", back_populates="ca", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<CA id={self.id} firm_name={self.firm_name!r}>"

