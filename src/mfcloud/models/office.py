"""Office (business entity) and accounting periods."""

from __future__ import annotations

from mfcloud.models.common import MFModel


class AccountingPeriod(MFModel):
    start_date: str
    end_date: str
    fiscal_year: int


class Office(MFModel):
    name: str
    code: str
    type: str
    employee_count: str | None = None
    is_real_estate: bool | None = None
    is_manufacturing: bool
    pl_name_value_display_option: str | None = None
    accounting_periods: list[AccountingPeriod]
