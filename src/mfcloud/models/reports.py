"""Reports: trial balances and transition (month-over-month) tables.

Row trees nest: assets/liabilities groups contain financial-statement items, which
contain accounts, which contain sub-accounts (row `type` distinguishes levels).
"""

from __future__ import annotations

from pydantic import field_validator

from mfcloud.models.common import MFModel


class TBRow(MFModel):
    type: str
    name: str
    values: list[float | None]
    rows: list[TBRow]

    @field_validator("rows", mode="before")
    @classmethod
    def _default_empty_rows(cls, v: list | None) -> list:
        # Leaf accounts (no sub-accounts) come back as `rows: null`.
        return v if v is not None else []


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

    @field_validator("rows", mode="before")
    @classmethod
    def _default_empty_rows(cls, v: list | None) -> list:
        # Leaf accounts (no sub-accounts) come back as `rows: null`.
        return v if v is not None else []


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
