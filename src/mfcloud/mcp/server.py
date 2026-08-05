"""MCP server — the primary Claude interface to Money Forward Cloud Accounting.

~20 curated English tools over the core library (not auto-generated from the spec):
the four report endpoints collapse into one tool, destructive operations require the
confirm/preview protocol (see safety.py), and the English API reference is exposed as
MCP resources under spec://reference/{page}.

Run: `uv run mfc-mcp` (stdio). Select the office with the MFC_PROFILE env var.
"""

from __future__ import annotations

import base64 as b64
from pathlib import Path
from typing import Literal

from fastmcp import FastMCP

from mfcloud.client import MFClient
from mfcloud.mcp.safety import journal_summary, preview
from mfcloud.models.requests import (
    JournalizeRequest,
    NewJournal,
    NewTradePartner,
    NewTransaction,
    VoucherFile,
)

READ_ONLY = {"readOnlyHint": True}
DESTRUCTIVE = {"readOnlyHint": False, "destructiveHint": True}
ADDITIVE = {"readOnlyHint": False, "destructiveHint": False}

DOCS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "docs" / "api"

mcp = FastMCP(
    "mf-accounting",
    instructions=(
        "English tools for Money Forward Cloud Accounting (Japanese-only platform)."
        " Amounts are yen integers; dates are YYYY-MM-DD; IDs are opaque strings from"
        " the list_* tools. Data values (account names etc.) may be Japanese —"
        " translate them for the user in conversation. Destructive tools return a"
        " preview first; call again with confirm=true only after the user agrees."
        " Full endpoint reference: resources under spec://reference/."
    ),
)

_client: MFClient | None = None


def get_client() -> MFClient:
    global _client
    if _client is None:
        _client = MFClient.from_profile()
    return _client


# --- read tools -----------------------------------------------------------------


@mcp.tool(annotations=READ_ONLY)
def get_office() -> dict:
    """The authorized office (business entity) and its accounting periods."""
    return get_client().offices.current().model_dump()


@mcp.tool(annotations=READ_ONLY)
def list_accounts(available: bool | None = None) -> list[dict]:
    """Chart of accounts with nested sub-accounts. available=true → only in-use."""
    return [a.model_dump() for a in get_client().accounts.list(available=available)]


@mcp.tool(annotations=READ_ONLY)
def list_sub_accounts(account_id: str | None = None) -> list[dict]:
    """Sub-accounts, optionally filtered to one parent account."""
    return [s.model_dump() for s in get_client().sub_accounts.list(account_id=account_id)]


@mcp.tool(annotations=READ_ONLY)
def list_departments() -> list[dict]:
    """Departments (cost centers)."""
    return [d.model_dump() for d in get_client().departments.list()]


@mcp.tool(annotations=READ_ONLY)
def list_taxes(available: bool | None = None) -> list[dict]:
    """Tax categories (consumption-tax treatments) with rates."""
    return [t.model_dump() for t in get_client().taxes.list(available=available)]


@mcp.tool(annotations=READ_ONLY)
def list_term_settings() -> list[dict]:
    """Accounting-period settings per fiscal year (tax method, rounding, etc.)."""
    return [t.model_dump() for t in get_client().term_settings.list()]


@mcp.tool(annotations=READ_ONLY)
def list_connected_accounts() -> list[dict]:
    """Connected services (bank/card feeds) incl. manual accounts, with sub-accounts."""
    return [c.model_dump() for c in get_client().connected_accounts.list()]


@mcp.tool(annotations=READ_ONLY)
def list_trade_partners(available: bool | None = None) -> list[dict]:
    """Trade partners (customers/vendors) with invoice registration numbers."""
    return [t.model_dump() for t in get_client().trade_partners.list(available=available)]


@mcp.tool(annotations=READ_ONLY)
def list_journals(
    start_date: str | None = None,
    end_date: str | None = None,
    account_id: str | None = None,
    is_realized: bool | None = None,
    page: int | None = None,
    per_page: int | None = None,
    all_pages: bool = False,
) -> dict:
    """Journal entries (dates filter transaction_date, YYYY-MM-DD).

    One page by default (per_page max 100); all_pages=true walks every page.
    """
    client = get_client()
    filters = dict(
        start_date=start_date, end_date=end_date,
        account_id=account_id, is_realized=is_realized,
    )
    if all_pages:
        journals = [j.model_dump() for j in client.journals.iter_all(**filters)]
        return {"journals": journals, "total_count": len(journals)}
    response = client.journals.list(page=page, per_page=per_page, **filters)
    return response.model_dump()


@mcp.tool(annotations=READ_ONLY)
def get_journal(journal_id: str) -> dict:
    """One journal entry by ID, with all lines and voucher file IDs."""
    return get_client().journals.get(journal_id).model_dump()


@mcp.tool(annotations=READ_ONLY)
def list_transactions(
    start_date: str,
    end_date: str,
    connected_account_id: str | None = None,
    side: Literal["income", "expense"] | None = None,
    content: str | None = None,
    journalizing_statuses: list[str] | None = None,
    page: int | None = None,
    per_page: int | None = None,
    all_pages: bool = False,
) -> dict:
    """Imported bank/card transactions in [start_date, end_date] (both required).

    journalizing_statuses example: ["not_journalized"] to find unbooked lines.
    """
    client = get_client()
    filters = dict(
        connected_account_id=connected_account_id, side=side, content=content,
        journalizing_statuses=journalizing_statuses,
    )
    if all_pages:
        rows = [t.model_dump() for t in client.transactions.iter_all(
            start_date, end_date, **filters)]
        return {"transactions": rows, "total_count": len(rows)}
    return client.transactions.list(
        start_date, end_date, page=page, per_page=per_page, **filters
    ).model_dump()


@mcp.tool(annotations=READ_ONLY)
def get_report(
    report_type: Literal[
        "trial_balance_bs", "trial_balance_pl", "transition_bs", "transition_pl"
    ],
    fiscal_year: int | None = None,
    start_month: int | None = None,
    end_month: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    with_sub_accounts: bool | None = None,
    include_tax: bool | None = None,
) -> dict:
    """Financial reports: trial balance or month-over-month transition, BS or PL.

    Trial balances take fiscal_year+months OR a date range; transitions take
    fiscal_year+months. Rows nest: group → statement item → account → sub-account.
    """
    reports = get_client().reports
    if report_type == "trial_balance_bs":
        result = reports.trial_balance_bs(
            fiscal_year=fiscal_year, start_month=start_month, end_month=end_month,
            start_date=start_date, end_date=end_date,
            with_sub_accounts=with_sub_accounts, include_tax=include_tax)
    elif report_type == "trial_balance_pl":
        result = reports.trial_balance_pl(
            fiscal_year=fiscal_year, start_month=start_month, end_month=end_month,
            start_date=start_date, end_date=end_date,
            with_sub_accounts=with_sub_accounts, include_tax=include_tax)
    elif report_type == "transition_bs":
        result = reports.transition_bs(
            type="transition_bs", fiscal_year=fiscal_year, start_month=start_month,
            end_month=end_month, with_sub_accounts=with_sub_accounts,
            include_tax=include_tax)
    else:
        result = reports.transition_pl(
            type="transition_pl", fiscal_year=fiscal_year, start_month=start_month,
            end_month=end_month, with_sub_accounts=with_sub_accounts,
            include_tax=include_tax)
    return result.model_dump()


# --- write tools ----------------------------------------------------------------


@mcp.tool(annotations=ADDITIVE)
def create_journal(journal: NewJournal) -> dict:
    """Create a journal entry. Each branch needs balancing debitor/creditor values
    (tax-inclusive yen). Get account/tax/department IDs from the list_* tools."""
    return journal_summary(get_client().journals.create(journal))


@mcp.tool(annotations=DESTRUCTIVE)
def update_journal(journal_id: str, journal: NewJournal, confirm: bool = False) -> dict:
    """REPLACE a journal entry (full update). Without confirm=true, returns a preview
    of the entry that would be overwritten and makes no change."""
    client = get_client()
    if not confirm:
        current = client.journals.get(journal_id)
        return preview(f"overwrite journal {journal_id}", journal_summary(current))
    return journal_summary(client.journals.update(journal_id, journal))


@mcp.tool(annotations=DESTRUCTIVE)
def delete_journal(journal_id: str, confirm: bool = False) -> dict:
    """PERMANENTLY delete a journal entry. Without confirm=true, returns a preview
    of what would be deleted and makes no change."""
    client = get_client()
    if not confirm:
        current = client.journals.get(journal_id)
        return preview(f"permanently delete journal {journal_id}", journal_summary(current))
    client.journals.delete(journal_id)
    return {"status": "deleted", "journal_id": journal_id}


@mcp.tool(annotations=ADDITIVE)
def upload_voucher(
    file_name: str,
    file_data_base64: str | None = None,
    file_path: str | None = None,
    journal_id: str | None = None,
) -> list[dict]:
    """Upload a voucher (receipt) file, optionally attached to a journal entry.
    Give either base64 content or a local file_path."""
    client = get_client()
    if file_path is not None:
        data = b64.b64encode(Path(file_path).read_bytes()).decode("ascii")
    elif file_data_base64 is not None:
        data = file_data_base64
    else:
        raise ValueError("Provide file_data_base64 or file_path.")
    return client.vouchers.upload(
        [VoucherFile(file_name=file_name, file_data=data)], journal_id
    )


@mcp.tool(annotations=DESTRUCTIVE)
def delete_voucher(journal_id: str, voucher_file_id: str, confirm: bool = False) -> dict:
    """Delete a voucher file from a journal entry. Without confirm=true, returns a
    preview (the journal it belongs to) and makes no change."""
    client = get_client()
    if not confirm:
        current = client.journals.get(journal_id)
        return preview(
            f"delete voucher {voucher_file_id} from journal {journal_id}",
            journal_summary(current),
        )
    client.vouchers.delete(journal_id, voucher_file_id)
    return {"status": "deleted", "voucher_file_id": voucher_file_id}


@mcp.tool(annotations=ADDITIVE)
def create_trade_partners(partners: list[NewTradePartner]) -> list[dict]:
    """Register trade partners (customers/vendors)."""
    return [t.model_dump() for t in get_client().trade_partners.create(list(partners))]


@mcp.tool(annotations=ADDITIVE)
def create_transactions(
    connected_account_id: str, transactions: list[NewTransaction]
) -> list[dict]:
    """Register manual transactions under a manual connected account
    (side: income or expense; value: yen)."""
    return [
        t.model_dump()
        for t in get_client().transactions.create(connected_account_id, list(transactions))
    ]


@mcp.tool(annotations=ADDITIVE)
def journalize_transaction(request: JournalizeRequest) -> dict:
    """Create a journal entry from an imported transaction (books it against the
    given account/tax/department). One call per transaction."""
    return journal_summary(get_client().transactions.journalize(request))


# --- reference resources ----------------------------------------------------------


@mcp.resource("spec://reference/{page}")
def reference_page(page: str) -> str:
    """English API reference pages (generated from the translated OpenAPI spec)."""
    if not page.replace("_", "").isalnum():
        raise ValueError("invalid page name")
    target = DOCS_DIR / f"{page}.md"
    if not target.exists():
        available = ", ".join(sorted(p.stem for p in DOCS_DIR.glob("*.md")))
        raise FileNotFoundError(f"No page '{page}'. Available: {available}")
    return target.read_text(encoding="utf-8")


@mcp.resource("spec://reference")
def reference_index() -> str:
    """Index of the English API reference."""
    return (DOCS_DIR / "README.md").read_text(encoding="utf-8")


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
