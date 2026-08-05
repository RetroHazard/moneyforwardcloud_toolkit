"""Request-body models for write operations.

Field names mirror the spec exactly. Amounts are tax-inclusive yen integers; dates are
YYYY-MM-DD strings. IDs come from the corresponding read endpoints (accounts, taxes,
departments, trade partners).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class RequestModel(BaseModel):
    """Requests forbid unknown fields — a typo'd field must fail loudly, locally."""

    model_config = ConfigDict(extra="forbid")


class NewJournalLineDetails(RequestModel):
    """One side (debit or credit) of a new journal line."""

    value: int
    account_id: str
    tax_id: str | None = None
    sub_account_id: str | None = None
    department_id: str | None = None
    trade_partner_code: str | None = None
    invoice_kind: str | None = None


class NewJournalLine(RequestModel):
    remark: str | None = None
    creditor: NewJournalLineDetails | None = None
    debitor: NewJournalLineDetails | None = None


class NewJournal(RequestModel):
    """Body of journal create/update (spec: CRUDJournalRequest_journal)."""

    transaction_date: str
    journal_type: str
    branches: list[NewJournalLine]
    memo: str | None = None
    tags: list[str] | None = None


class VoucherFile(RequestModel):
    """A file to upload as a voucher; file_data is base64-encoded content."""

    file_name: str
    file_data: str


class NewTradePartner(RequestModel):
    name: str
    search_key: str | None = None
    invoice_registration_number: str | None = None
    corporate_number: str | None = None
    available: bool | None = None


class NewTransaction(RequestModel):
    date: str
    value: int
    side: str
    content: str
    memo: str | None = None


class JournalizeRequest(RequestModel):
    """Create a journal entry from an imported transaction
    (spec: PostTransactionJournalizeRequest)."""

    transaction_id: str
    account_id: str
    transaction_date: str | None = None
    tags: list[str] | None = None
    memo: str | None = None
    sub_account_id: str | None = None
    department_id: str | None = None
    trade_partner_code: str | None = None
    tax_id: str | None = None
    invoice_kind: str | None = None
    remark: str | None = None


REQUEST_MODEL_FOR_SCHEMA: dict[str, type[RequestModel]] = {
    "CRUDJournalRequest_journal": NewJournal,
    "CRUDJournalLine": NewJournalLine,
    "CRUDJournalLineDetails": NewJournalLineDetails,
    "PostVouchersRequest_voucher_files_inner": VoucherFile,
    "PostTradePartnersRequest_trade_partners_inner": NewTradePartner,
    "PostTransactionsRequest_transactions_inner": NewTransaction,
    "PostTransactionJournalizeRequest": JournalizeRequest,
}
