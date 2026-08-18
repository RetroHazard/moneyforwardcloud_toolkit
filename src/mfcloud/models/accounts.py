"""Accounts (chart of accounts) and sub-accounts."""

from __future__ import annotations

from pydantic import field_validator

from mfcloud.models.common import MFModel

# Spec enum AccountGroups: NONE, ASSET, LIABILITY, CAPITAL, REVENUE, EXPENSE.
# Kept as str for forward compatibility; values documented in docs/api/schemas.md.


class SubAccount(MFModel):
    account_id: str
    id: str
    name: str
    search_key: str
    tax_id: str

    @field_validator("search_key", mode="before")
    @classmethod
    def _default_empty_search_key(cls, v: str | None) -> str:
        # API sends null instead of "" for unset search keys, despite the spec
        # marking this field required.
        return v if v is not None else ""


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

    @field_validator("search_key", mode="before")
    @classmethod
    def _default_empty_search_key(cls, v: str | None) -> str:
        # API sends null instead of "" for unset search keys, despite the spec
        # marking this field required.
        return v if v is not None else ""
