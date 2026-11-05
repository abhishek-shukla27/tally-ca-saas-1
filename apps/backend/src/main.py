"""
main.py – FastAPI application entry-point.
Phase 2 implementation – see plan.md § Phase 2.
"""
from fastapi import FastAPI

app = FastAPI(title="Tally-CA SaaS Backend", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


