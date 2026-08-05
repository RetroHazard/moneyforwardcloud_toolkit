"""Accounts (chart of accounts) and sub-accounts."""

from __future__ import annotations

from mfcloud.models.common import MFModel

# Spec enum AccountGroups: NONE, ASSET, LIABILITY, CAPITAL, REVENUE, EXPENSE.
# Kept as str for forward compatibility; values documented in docs/api/schemas.md.


class SubAccount(MFModel):
    account_id: str
    id: str
    name: str
    search_key: str
    tax_id: str


class Account(MFModel):
    id: str
    financial_statement_type: str
    name: str
    available: bool
    tax_id: str
    search_key: str
    sub_accounts: list[SubAccount]
    account_group: str
    category: str
