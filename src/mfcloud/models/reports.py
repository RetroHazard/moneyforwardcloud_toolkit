"""Reports: trial balances and transition (month-over-month) tables.

Row trees nest: assets/liabilities groups contain financial-statement items, which
contain accounts, which contain sub-accounts (row `type` distinguishes levels).
"""

from __future__ import annotations

from mfcloud.models.common import MFModel


class TBRow(MFModel):
    type: str
    name: str
    values: list[float | None]
    rows: list[TBRow]


class TBResponse(MFModel):
    report_type: str
    start_date: str
    end_date: str
    created_at: str
    columns: list[str]
    rows: list[TBRow]


class TransitionRow(MFModel):
    type: str
    name: str
    values: list[int | None]
    rows: list[TransitionRow]


class TransitionResponse(MFModel):
    report_type: str
    fiscal_year: int
    start_month: int
    end_month: int
    start_date: str
    end_date: str
    created_at: str
    columns: list[str]
    rows: list[TransitionRow]
