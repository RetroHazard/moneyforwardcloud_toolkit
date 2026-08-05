"""Imported bank/card transactions (明細)."""

from __future__ import annotations

from mfcloud.models.common import Metadata, MFModel


class Transaction(MFModel):
    id: str
    date: str
    value: int
    side: str
    content: str | None = None
    memo: str | None = None
    journalizing_status: str
    connected_account_id: str
    connected_sub_account_id: str
    voucher_file_ids: list[str]


class GetTransactionsResponse(MFModel):
    transactions: list[Transaction]
    metadata: Metadata
