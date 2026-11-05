"""
database.py
~~~~~~~~~~~
SQLAlchemy engine + session factory.

Pattern: "one engine, one SessionLocal factory, yield-per-request sessions."
Import `get_db` as a FastAPI dependency to get a scoped session.
"""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from core.config import settings

# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------
engine = create_engine(
    settings.DATABASE_URL,
    # Keep a small pool — this is a low-traffic ingestion service
    pool_pre_ping=True,     # health-check connections before use
    pool_size=5,
    max_overflow=10,
    echo=settings.DEBUG,    # log SQL when DEBUG=True
)

# ---------------------------------------------------------------------------
# Session factory
# ---------------------------------------------------------------------------
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,  # keep attributes accessible after commit
)


# ---------------------------------------------------------------------------
# Declarative base (all models inherit from this)
# ---------------------------------------------------------------------------
class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# FastAPI dependency
# ---------------------------------------------------------------------------
def get_db() -> Generator[Session, None, None]:
    """
    Yield a SQLAlchemy Session for the duration of a single HTTP request.
    The session is always closed in the finally block, even on error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

