"""Journal entries as returned by the API."""

from __future__ import annotations

from mfcloud.models.common import Metadata, MFModel

# entered_by (spec enum EnteredBy) tells which product created the entry, e.g.
# JOURNAL_TYPE_NORMAL (manual), JOURNAL_TYPE_STREAMED (bank feed), JOURNAL_TYPE_OPENING.
# Kept as str; the full value list lives in docs/api/schemas.md.


class JournalLineDetails(MFModel):
    """One side (debit or credit) of a journal line."""

    value: int
    tax_value: int | None = None
    account_id: str
    account_name: str
    sub_account_id: str | None = None
    sub_account_name: str | None = None
    tax_long_name: str | None = None
    tax_id: str | None = None
    tax_name: str | None = None
    department_id: str | None = None
    department_name: str | None = None
    trade_partner_name: str | None = None
    trade_partner_code: str | None = None
    invoice_kind: str | None = None


class JournalLine(MFModel):
    remark: str | None = None
    creditor: JournalLineDetails | None = None
    debitor: JournalLineDetails | None = None


class JournalItem(MFModel):
    entered_by: str
    id: str
    number: int
    term_period: int
    transaction_date: str
    is_realized: bool
    journal_type: str
    create_time: str
    update_time: str
    branches: list[JournalLine]
    tags: list[str]
    memo: str | None = None
    voucher_file_ids: list[str]
    transaction_id: str | None = None


class GetJournalsResponse(MFModel):
    metadata: Metadata
    journals: list[JournalItem]


class CRUDJournalResponse(MFModel):
    journal: JournalItem
