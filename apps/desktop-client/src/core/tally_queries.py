"""
tally_queries.py
~~~~~~~~~~~~~~~~
Canonical XML envelope templates for every Tally request type.
Each function returns a fully-formed XML string ready to POST to
http://localhost:9000.

Tally uses TDLXML / TDL Report envelopes. The pattern is:
  <ENVELOPE>
    <HEADER> ... </HEADER>
    <BODY>
      <EXPORTDATA>
        <REQUESTDESC>
          <REPORTNAME>...</REPORTNAME>
          <STATICVARIABLES>...</STATICVARIABLES>
        </REQUESTDESC>
      </EXPORTDATA>
    </BODY>
  </ENVELOPE>
"""

from __future__ import annotations


def build_ledger_list_xml() -> str:
    """Return the XML envelope to fetch all Ledger masters from TallyPrime."""
    return """<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER>
    <VERSION>1</VERSION>
    <TALLYREQUEST>EXPORT</TALLYREQUEST>
    <TYPE>COLLECTION</TYPE>
    <ID>Ledger List</ID>
  </HEADER>
  <BODY>
    <DESC>
      <STATICVARIABLES>
        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
      </STATICVARIABLES>
      <TDL>
        <TDLMESSAGE>
          <COLLECTION NAME="Ledger List" ISMODIFY="No">
            <TYPE>Ledger</TYPE>
            <NATIVEMETHOD>NAME</NATIVEMETHOD>
            <NATIVEMETHOD>PARENT</NATIVEMETHOD>
            <NATIVEMETHOD>OPENINGBALANCE</NATIVEMETHOD>
            <NATIVEMETHOD>CLOSINGBALANCE</NATIVEMETHOD>
            <NATIVEMETHOD>GUID</NATIVEMETHOD>
          </COLLECTION>
        </TDLMESSAGE>
      </TDL>
    </DESC>
  </BODY>
</ENVELOPE>"""


def build_voucher_list_xml(from_date: str = "20240401", to_date: str = "20250331") -> str:
    """
    Return the XML envelope to fetch all Vouchers within a date range.

    Args:
        from_date: Start date in YYYYMMDD format (default: FY 2024-25 start).
        to_date:   End date   in YYYYMMDD format (default: FY 2024-25 end).
    """
    return f"""<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER>
    <VERSION>1</VERSION>
    <TALLYREQUEST>EXPORT</TALLYREQUEST>
    <TYPE>COLLECTION</TYPE>
    <ID>Voucher List</ID>
  </HEADER>
  <BODY>
    <DESC>
      <STATICVARIABLES>
        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
        <SVFROMDATE>{from_date}</SVFROMDATE>
        <SVTODATE>{to_date}</SVTODATE>
      </STATICVARIABLES>
      <TDL>
        <TDLMESSAGE>
          <COLLECTION NAME="Voucher List" ISMODIFY="No">
            <TYPE>Voucher</TYPE>
            <NATIVEMETHOD>GUID</NATIVEMETHOD>
            <NATIVEMETHOD>DATE</NATIVEMETHOD>
            <NATIVEMETHOD>VOUCHERTYPENAME</NATIVEMETHOD>
            <NATIVEMETHOD>VOUCHERNUMBER</NATIVEMETHOD>
            <NATIVEMETHOD>PARTYLEDGERNAME</NATIVEMETHOD>
            <NATIVEMETHOD>AMOUNT</NATIVEMETHOD>
            <NATIVEMETHOD>ISCANCELLED</NATIVEMETHOD>
            <NATIVEMETHOD>NARRATION</NATIVEMETHOD>
          </COLLECTION>
        </TDLMESSAGE>
      </TDL>
    </DESC>
  </BODY>
</ENVELOPE>"""


def build_stock_item_list_xml() -> str:
    """Return the XML envelope to fetch all Stock Item masters from TallyPrime."""
    return """<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER>
    <VERSION>1</VERSION>
    <TALLYREQUEST>EXPORT</TALLYREQUEST>
    <TYPE>COLLECTION</TYPE>
    <ID>Stock Item List</ID>
  </HEADER>
  <BODY>
    <DESC>
      <STATICVARIABLES>
        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
      </STATICVARIABLES>
      <TDL>
        <TDLMESSAGE>
          <COLLECTION NAME="Stock Item List" ISMODIFY="No">
            <TYPE>Stock Item</TYPE>
            <NATIVEMETHOD>NAME</NATIVEMETHOD>
            <NATIVEMETHOD>PARENT</NATIVEMETHOD>
            <NATIVEMETHOD>BASEUNITS</NATIVEMETHOD>
            <NATIVEMETHOD>OPENINGBALANCE</NATIVEMETHOD>
            <NATIVEMETHOD>OPENINGRATE</NATIVEMETHOD>
            <NATIVEMETHOD>OPENINGVALUE</NATIVEMETHOD>
            <NATIVEMETHOD>GUID</NATIVEMETHOD>
          </COLLECTION>
        </TDLMESSAGE>
      </TDL>
    </DESC>
  </BODY>
</ENVELOPE>"""

