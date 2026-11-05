"""
core/security.py
~~~~~~~~~~~~~~~~
FastAPI dependency that validates the `X-Client-Token` header.

Usage in a route:
    @router.post("/upload")
    def upload(client: Client = Depends(get_current_client), ...):
        ...
"""

from __future__ import annotations

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from models.client import Client


def get_current_client(
    x_client_token: str = Header(
        ...,
        alias="X-Client-Token",
        description="Unique sync token issued to the desktop agent during client onboarding.",
    ),
    db: Session = Depends(get_db),
) -> Client:
    """
    Validate X-Client-Token against the `clients` table.

    Returns:
        The matching Client ORM instance.

    Raises:
        HTTP 401 — if the token is missing (FastAPI handles this automatically
                   because the header is required).
        HTTP 403 — if the token exists in the request but is not found in the DB.
    """
    client = (
        db.query(Client)
        .filter(Client.api_sync_token == x_client_token)
        .first()
    )
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or unrecognised X-Client-Token.",
        )
    return client
