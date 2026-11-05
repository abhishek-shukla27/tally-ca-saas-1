"""
main.py
~~~~~~~
FastAPI application entry-point for the Tally-CA SaaS backend.

Startup sequence:
  1. Load settings from .env
  2. Create all DB tables (if they don't exist)
  3. Mount all API routers
  4. Expose /health and interactive docs
"""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.database import Base, engine

# Import all models so SQLAlchemy's metadata knows about them
# before create_all() is called.
import models  # noqa: F401 — registers CA, Client, Voucher with Base.metadata

from api.sync import router as sync_router

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("main")

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=(
        "Cloud ingestion backend for TallyPrime data. "
        "Receives payloads from the desktop sync agent and exposes "
        "compliance dashboards to CA firms."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS  (tighten origins in production)
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# DB table creation on startup
# ---------------------------------------------------------------------------
@app.on_event("startup")
def on_startup() -> None:
    log.info("Creating database tables (if they do not exist) …")
    Base.metadata.create_all(bind=engine)
    log.info("Database ready.")


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(sync_router)


# ---------------------------------------------------------------------------
# Root health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"], summary="Application health check")
def health() -> dict:
    return {"status": "ok", "version": settings.APP_VERSION}
