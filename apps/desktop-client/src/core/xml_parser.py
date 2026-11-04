"""
xml_parser.py
~~~~~~~~~~~~~
Converts raw TallyPrime XML responses into clean, flat Python dicts / lists
that are safe to serialise straight to JSON.

Design decisions:
  - Uses stdlib `xml.etree.ElementTree` only — zero third-party deps.
  - Each parser is a pure function: xml_text -> list[dict].
  - Monetary amounts are kept as floats (Tally negates credit entries).
  - `_safe_float` silently handles empty / malformed amount strings.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _safe_float(value: str | None) -> float:
    """Parse a Tally amount string to float; return 0.0 on failure."""
    if not value:
        return 0.0
    try:
        return float(value.strip().replace(",", ""))
    except ValueError:
        return 0.0


def _safe_text(element: ET.Element | None, tag: str, default: str = "") -> str:
    """Extract inner text from a child tag, with a safe default."""
    if element is None:
        return default
    child = element.find(tag)
    return (child.text or default).strip() if child is not None else default


def _parse_collection(xml_text: str, item_tag: str) -> list[ET.Element]:
    """
    Parse the top-level Tally XML envelope and return all matching item elements.

    Tally response root is typically <ENVELOPE><BODY><DATA><COLLECTION>...
    """
    try:
        root = ET.fromstring(xml_text.strip())
    except ET.ParseError as exc:
        raise ValueError(f"Invalid XML from Tally: {exc}") from exc

    # Walk any nesting depth to find the collection items
    return root.findall(f".//{item_tag}")


# ---------------------------------------------------------------------------
# Public parsers
# ---------------------------------------------------------------------------

def parse_ledgers(xml_text: str) -> list[dict[str, Any]]:
    """
    Parse a Tally Ledger collection XML response.

    Returns:
        List of dicts with keys:
            guid, name, parent_group, opening_balance, closing_balance
    """
    items = _parse_collection(xml_text, "LEDGER")
    result: list[dict[str, Any]] = []

    for ledger in items:
        result.append(
            {
                "guid": _safe_text(ledger, "GUID"),
                "name": ledger.get("NAME") or _safe_text(ledger, "NAME"),
                "parent_group": _safe_text(ledger, "PARENT"),
                "opening_balance": _safe_float(_safe_text(ledger, "OPENINGBALANCE")),
                "closing_balance": _safe_float(_safe_text(ledger, "CLOSINGBALANCE")),
            }
        )

    return result


def parse_vouchers(xml_text: str) -> list[dict[str, Any]]:
    """
    Parse a Tally Voucher collection XML response.

    Returns:
        List of dicts with keys:
            guid, date, voucher_type, voucher_number,
            party_ledger, amount, is_cancelled, narration
    """
    items = _parse_collection(xml_text, "VOUCHER")
    result: list[dict[str, Any]] = []

    for voucher in items:
        raw_date = _safe_text(voucher, "DATE")  # Format: YYYYMMDD
        formatted_date = (
            f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
            if len(raw_date) == 8
            else raw_date
        )
        cancelled_text = _safe_text(voucher, "ISCANCELLED").upper()

        result.append(
            {
                "guid": _safe_text(voucher, "GUID"),
                "date": formatted_date,
                "voucher_type": _safe_text(voucher, "VOUCHERTYPENAME"),
                "voucher_number": _safe_text(voucher, "VOUCHERNUMBER"),
                "party_ledger": _safe_text(voucher, "PARTYLEDGERNAME"),
                "amount": _safe_float(_safe_text(voucher, "AMOUNT")),
                "is_cancelled": cancelled_text in ("YES", "TRUE", "1"),
                "narration": _safe_text(voucher, "NARRATION"),
            }
        )

    return result


def parse_stock_items(xml_text: str) -> list[dict[str, Any]]:
    """
    Parse a Tally Stock Item collection XML response.

    Returns:
        List of dicts with keys:
            guid, name, parent_group, base_units,
            opening_quantity, opening_rate, opening_value
    """
    items = _parse_collection(xml_text, "STOCKITEM")
    result: list[dict[str, Any]] = []

    for item in items:
        result.append(
            {
                "guid": _safe_text(item, "GUID"),
                "name": item.get("NAME") or _safe_text(item, "NAME"),
                "parent_group": _safe_text(item, "PARENT"),
                "base_units": _safe_text(item, "BASEUNITS"),
                "opening_quantity": _safe_float(_safe_text(item, "OPENINGBALANCE")),
                "opening_rate": _safe_float(_safe_text(item, "OPENINGRATE")),
                "opening_value": _safe_float(_safe_text(item, "OPENINGVALUE")),
            }
        )

    return result

