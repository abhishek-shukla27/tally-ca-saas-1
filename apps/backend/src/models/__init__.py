"""
models/__init__.py
~~~~~~~~~~~~~~~~~~
Re-export all ORM models so that:
  - `from models import CA, Client, Voucher` works anywhere.
  - Alembic's env.py can do `from models import Base` and discover
    all tables automatically for autogenerate migrations.
"""

from core.database import Base  # noqa: F401 — re-exported for Alembic
from models.ca import CA  # noqa: F401
from models.client import Client  # noqa: F401
from models.voucher import Voucher  # noqa: F401

__all__ = ["Base", "CA", "Client", "Voucher"]
