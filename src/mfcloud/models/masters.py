"""Master data: departments, tax categories, term settings, trade partners,
connected services."""

from __future__ import annotations

from mfcloud.models.common import MFModel


class Department(MFModel):
    id: str
    name: str
    parent_id: str
    search_key: str


class Tax(MFModel):
    id: str
    name: str
    abbreviation: str
    tax_rate: float
    search_key: str
    available: bool


class TermSetting(MFModel):
    start_date: str
    end_date: str
    fiscal_year: int
    prefecture: str
    business_types: list[str]
    tax_method: str
    accounting_method: str | None = None
    sales_rounding_method: str
    purchases_rounding_method: str


class TradePartner(MFModel):
    name: str
    available: bool
    code: str
    invoice_registration_number: str
    corporate_number: str
    search_key: str


class ConnectedSubAccount(MFModel):
    id: str
    name: str
    account_id: str
    sub_account_id: str


class ConnectedAccount(MFModel):
    id: str
    name: str
    is_manual: bool
    account_id: str
    sub_account_id: str
    connected_sub_accounts: list[ConnectedSubAccount]
