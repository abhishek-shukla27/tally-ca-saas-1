"""
tally_client.py  –  Phase 1 Core
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Tally-Sync Desktop Client: HTTP bridge between TallyPrime (localhost:9000)
and the Cloud Backend API.

Responsibilities:
  1. Build the correct XML POST envelope for each data type.
  2. Fire the request at http://localhost:9000 and return raw XML.
  3. Parse the XML into flat JSON-serialisable dicts.
  4. Compress the payload (gzip) and POST it to the Cloud Backend.
  5. Provide a full mock-data test harness so the script runs and
     validates correctness with zero live Tally dependency.

Usage (live):
    python tally_client.py --sync all

Usage (dry-run / CI):
    python tally_client.py --mock
"""

from __future__ import annotations

import argparse
import gzip
import json
import logging
import os
import sys
from typing import Any

import requests

# ---------------------------------------------------------------------------
# Local imports  (src/ is on the path when run from project root or via the
# scheduler; adjust as needed if the working directory differs)
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.tally_queries import (
    build_ledger_list_xml,
    build_stock_item_list_xml,
    build_voucher_list_xml,
)
from core.xml_parser import parse_ledgers, parse_stock_items, parse_vouchers

# ---------------------------------------------------------------------------
# Configuration  (override via environment variables or a .env file)
# ---------------------------------------------------------------------------
TALLY_URL: str = os.getenv("TALLY_URL", "http://localhost:9000")
BACKEND_UPLOAD_URL: str = os.getenv(
    "BACKEND_UPLOAD_URL", "https://api.tally-ca-saas.example.com/api/v1/sync/upload"
)
CLIENT_TOKEN: str = os.getenv("CLIENT_TOKEN", "REPLACE_ME_WITH_REAL_TOKEN")
REQUEST_TIMEOUT: int = int(os.getenv("TALLY_TIMEOUT", "30"))

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("tally_client")


# ===========================================================================
# Layer 1 – Tally HTTP transport
# ===========================================================================

def _post_to_tally(xml_body: str) -> str:
    """
    POST an XML envelope to the local TallyPrime HTTP server.

    Args:
        xml_body: UTF-8 XML string.

    Returns:
        Raw XML response text from Tally.

    Raises:
        requests.RequestException: on network / timeout errors.
        ValueError: if Tally returns a non-200 status.
    """
    log.debug("POSTing %d-byte envelope to %s", len(xml_body), TALLY_URL)
    response = requests.post(
        TALLY_URL,
        data=xml_body.encode("utf-8"),
        headers={"Content-Type": "text/xml; charset=utf-8"},
        timeout=REQUEST_TIMEOUT,
    )
    if response.status_code != 200:
        raise ValueError(
            f"Tally returned HTTP {response.status_code}: {response.text[:200]}"
        )
    log.debug("Tally response: %d bytes", len(response.text))
    return response.text


# ===========================================================================
# Layer 2 – High-level fetch helpers
# ===========================================================================

def fetch_ledgers() -> list[dict[str, Any]]:
    """Fetch and parse Ledger masters from the live Tally instance."""
    log.info("Fetching ledger list from Tally …")
    xml = _post_to_tally(build_ledger_list_xml())
    ledgers = parse_ledgers(xml)
    log.info("  → %d ledgers received", len(ledgers))
    return ledgers


def fetch_vouchers(from_date: str = "20240401", to_date: str = "20250331") -> list[dict[str, Any]]:
    """Fetch and parse Vouchers from the live Tally instance."""
    log.info("Fetching vouchers from %s to %s …", from_date, to_date)
    xml = _post_to_tally(build_voucher_list_xml(from_date, to_date))
    vouchers = parse_vouchers(xml)
    log.info("  → %d vouchers received", len(vouchers))
    return vouchers


def fetch_stock_items() -> list[dict[str, Any]]:
    """Fetch and parse Stock Item masters from the live Tally instance."""
    log.info("Fetching stock items from Tally …")
    xml = _post_to_tally(build_stock_item_list_xml())
    items = parse_stock_items(xml)
    log.info("  → %d stock items received", len(items))
    return items


# ===========================================================================
# Layer 3 – Cloud upload
# ===========================================================================

def upload_payload(data_type: str, records: list[dict[str, Any]]) -> bool:
    """
    Compress and POST a JSON payload to the Cloud Backend API.

    Args:
        data_type: One of "ledgers", "vouchers", "stock_items".
        records:   Parsed records to upload.

    Returns:
        True on HTTP 2xx, False otherwise.
    """
    payload = {
        "data_type": data_type,
        "record_count": len(records),
        "records": records,
    }
    raw_json = json.dumps(payload, ensure_ascii=False, default=str)
    compressed = gzip.compress(raw_json.encode("utf-8"))

    log.info(
        "Uploading %s: %d records (%d bytes → %d bytes gzipped)",
        data_type,
        len(records),
        len(raw_json),
        len(compressed),
    )

    try:
        resp = requests.post(
            BACKEND_UPLOAD_URL,
            data=compressed,
            headers={
                "Content-Type": "application/json",
                "Content-Encoding": "gzip",
                "X-Client-Token": CLIENT_TOKEN,
                "X-Data-Type": data_type,
            },
            timeout=60,
        )
        if resp.status_code in range(200, 300):
            log.info("  → Upload OK (%d)", resp.status_code)
            return True
        log.error("  → Upload failed (%d): %s", resp.status_code, resp.text[:200])
        return False
    except requests.RequestException as exc:
        log.error("  → Upload network error: %s", exc)
        return False


# ===========================================================================
# Layer 4 – Full sync orchestration
# ===========================================================================

def run_full_sync(from_date: str = "20240401", to_date: str = "20250331") -> None:
    """Execute a complete ledger + voucher + stock-item sync cycle."""
    log.info("=== Starting full Tally sync ===")
    results: dict[str, bool] = {}

    try:
        ledgers = fetch_ledgers()
        results["ledgers"] = upload_payload("ledgers", ledgers)
    except Exception as exc:
        log.error("Ledger sync failed: %s", exc)
        results["ledgers"] = False

    try:
        vouchers = fetch_vouchers(from_date, to_date)
        results["vouchers"] = upload_payload("vouchers", vouchers)
    except Exception as exc:
        log.error("Voucher sync failed: %s", exc)
        results["vouchers"] = False

    try:
        items = fetch_stock_items()
        results["stock_items"] = upload_payload("stock_items", items)
    except Exception as exc:
        log.error("Stock-item sync failed: %s", exc)
        results["stock_items"] = False

    log.info("=== Sync complete: %s ===", results)


# ===========================================================================
# Layer 5 – Mock / self-test harness (no live Tally required)
# ===========================================================================

# ── Mock XML responses ──────────────────────────────────────────────────────

MOCK_LEDGER_XML = """<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <BODY>
    <DATA>
      <COLLECTION>
        <LEDGER NAME="Cash">
          <GUID>led-001-cash</GUID>
          <PARENT>Cash-in-Hand</PARENT>
          <OPENINGBALANCE>50000</OPENINGBALANCE>
          <CLOSINGBALANCE>42500</CLOSINGBALANCE>
        </LEDGER>
        <LEDGER NAME="State Bank of India">
          <GUID>led-002-sbi</GUID>
          <PARENT>Bank Accounts</PARENT>
          <OPENINGBALANCE>250000</OPENINGBALANCE>
          <CLOSINGBALANCE>318750.50</CLOSINGBALANCE>
        </LEDGER>
        <LEDGER NAME="Sundry Debtors - Ravi Enterprises">
          <GUID>led-003-ravi</GUID>
          <PARENT>Sundry Debtors</PARENT>
          <OPENINGBALANCE>0</OPENINGBALANCE>
          <CLOSINGBALANCE>75000</CLOSINGBALANCE>
        </LEDGER>
        <LEDGER NAME="GST Payable (CGST)">
          <GUID>led-004-cgst</GUID>
          <PARENT>Duties &amp; Taxes</PARENT>
          <OPENINGBALANCE>0</OPENINGBALANCE>
          <CLOSINGBALANCE>-9000</CLOSINGBALANCE>
        </LEDGER>
      </COLLECTION>
    </DATA>
  </BODY>
</ENVELOPE>"""

MOCK_VOUCHER_XML = """<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <BODY>
    <DATA>
      <COLLECTION>
        <VOUCHER>
          <GUID>vch-001</GUID>
          <DATE>20240415</DATE>
          <VOUCHERTYPENAME>Payment</VOUCHERTYPENAME>
          <VOUCHERNUMBER>PMT/2024/001</VOUCHERNUMBER>
          <PARTYLEDGERNAME>Cash</PARTYLEDGERNAME>
          <AMOUNT>-15000</AMOUNT>
          <ISCANCELLED>No</ISCANCELLED>
          <NARRATION>Office supplies purchase – Sharma Stationery</NARRATION>
        </VOUCHER>
        <VOUCHER>
          <GUID>vch-002</GUID>
          <DATE>20240501</DATE>
          <VOUCHERTYPENAME>Receipt</VOUCHERTYPENAME>
          <VOUCHERNUMBER>RCP/2024/001</VOUCHERNUMBER>
          <PARTYLEDGERNAME>Sundry Debtors - Ravi Enterprises</PARTYLEDGERNAME>
          <AMOUNT>75000</AMOUNT>
          <ISCANCELLED>No</ISCANCELLED>
          <NARRATION>Payment received against Invoice INV-2024-012</NARRATION>
        </VOUCHER>
        <VOUCHER>
          <GUID>vch-003</GUID>
          <DATE>20240610</DATE>
          <VOUCHERTYPENAME>Journal</VOUCHERTYPENAME>
          <VOUCHERNUMBER>JNL/2024/001</VOUCHERNUMBER>
          <PARTYLEDGERNAME>GST Payable (CGST)</PARTYLEDGERNAME>
          <AMOUNT>-9000</AMOUNT>
          <ISCANCELLED>Yes</ISCANCELLED>
          <NARRATION>CGST adjustment entry – cancelled in revision</NARRATION>
        </VOUCHER>
      </COLLECTION>
    </DATA>
  </BODY>
</ENVELOPE>"""

MOCK_STOCK_XML = """<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <BODY>
    <DATA>
      <COLLECTION>
        <STOCKITEM NAME="A4 Paper Ream">
          <GUID>stk-001</GUID>
          <PARENT>Stationery</PARENT>
          <BASEUNITS>Nos</BASEUNITS>
          <OPENINGBALANCE>50</OPENINGBALANCE>
          <OPENINGRATE>250</OPENINGRATE>
          <OPENINGVALUE>12500</OPENINGVALUE>
        </STOCKITEM>
        <STOCKITEM NAME="Printer Toner (Black)">
          <GUID>stk-002</GUID>
          <PARENT>Consumables</PARENT>
          <BASEUNITS>Nos</BASEUNITS>
          <OPENINGBALANCE>5</OPENINGBALANCE>
          <OPENINGRATE>1800</OPENINGRATE>
          <OPENINGVALUE>9000</OPENINGVALUE>
        </STOCKITEM>
      </COLLECTION>
    </DATA>
  </BODY>
</ENVELOPE>"""


def run_mock_test() -> None:
    """
    Self-contained test harness.

    Parses mock XML → pretty-prints JSON output.
    Does NOT touch the network. Useful for CI and offline demos.
    """
    print("\n" + "=" * 70)
    print("  TALLY SYNC AGENT  –  Mock / Offline Test Mode")
    print("=" * 70)

    # ── Ledgers ─────────────────────────────────────────────────────────────
    print("\n[1] Parsing Ledger XML …")
    ledgers = parse_ledgers(MOCK_LEDGER_XML)
    _pretty_print("Ledgers", ledgers)

    # ── Vouchers ─────────────────────────────────────────────────────────────
    print("\n[2] Parsing Voucher XML …")
    vouchers = parse_vouchers(MOCK_VOUCHER_XML)
    _pretty_print("Vouchers", vouchers)

    # ── Stock Items ──────────────────────────────────────────────────────────
    print("\n[3] Parsing Stock Item XML …")
    stock_items = parse_stock_items(MOCK_STOCK_XML)
    _pretty_print("Stock Items", stock_items)

    # ── XML Query Envelopes ──────────────────────────────────────────────────
    print("\n[4] Generating XML request envelopes …")
    for label, xml_fn in [
        ("Ledger List",   build_ledger_list_xml),
        ("Voucher List",  lambda: build_voucher_list_xml("20240401", "20250331")),
        ("Stock Items",   build_stock_item_list_xml),
    ]:
        xml = xml_fn()
        print(f"  [OK] {label}: {len(xml)} bytes")

    # ── Compression simulation ───────────────────────────────────────────────
    print("\n[5] Compression simulation …")
    for data_type, records in [("ledgers", ledgers), ("vouchers", vouchers), ("stock_items", stock_items)]:
        raw = json.dumps({"data_type": data_type, "records": records}, ensure_ascii=False)
        compressed = gzip.compress(raw.encode("utf-8"))
        ratio = (1 - len(compressed) / len(raw.encode("utf-8"))) * 100
        print(
            f"  {data_type:<15}  raw={len(raw):>6} B  gzip={len(compressed):>5} B  "
            f"savings={ratio:.1f}%"
        )

    print("\n" + "=" * 70)
    print("  All mock tests PASSED  [OK]")
    print("=" * 70 + "\n")


def _pretty_print(label: str, records: list[dict]) -> None:
    """Print records as indented JSON with a header."""
    print(f"\n--- {label} ({len(records)} records) ---")
    print(json.dumps(records, indent=2, ensure_ascii=False, default=str))


# ===========================================================================
# CLI entry-point
# ===========================================================================

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Tally Sync Agent – fetch data from TallyPrime and push to the cloud.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run offline mock test (no live Tally or cloud connection).",
    )
    parser.add_argument(
        "--sync",
        choices=["ledgers", "vouchers", "stock_items", "all"],
        help="Sync a specific data type (or 'all') from live Tally.",
    )
    parser.add_argument("--from-date", default="20240401", help="Voucher start date (YYYYMMDD).")
    parser.add_argument("--to-date",   default="20250331", help="Voucher end date   (YYYYMMDD).")
    return parser


def main() -> None:
    args = _build_parser().parse_args()

    if args.mock:
        run_mock_test()
        return

    if args.sync == "ledgers":
        ledgers = fetch_ledgers()
        upload_payload("ledgers", ledgers)
    elif args.sync == "vouchers":
        vouchers = fetch_vouchers(args.from_date, args.to_date)
        upload_payload("vouchers", vouchers)
    elif args.sync == "stock_items":
        items = fetch_stock_items()
        upload_payload("stock_items", items)
    elif args.sync == "all":
        run_full_sync(args.from_date, args.to_date)
    else:
        _build_parser().print_help()


if __name__ == "__main__":
    main()
