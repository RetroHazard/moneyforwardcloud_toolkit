"""Reports: trial balances (BS/PL) and transition tables (BS/PL)."""

from __future__ import annotations

from mfcloud.models.reports import TBResponse, TransitionResponse
from mfcloud.resources.base import Resource, operation


class ReportsResource(Resource):
    def _trial_balance(
        self,
        which: str,
        fiscal_year: int | None,
        start_month: int | None,
        end_month: int | None,
        start_date: str | None,
        end_date: str | None,
        with_sub_accounts: bool | None,
        include_tax: bool | None,
        journal_types: list[str] | None,
    ) -> TBResponse:
        data = self._client.get(
            f"/api/v3/reports/trial_balance_{which}",
            params={
                "fiscal_year": fiscal_year,
                "start_month": start_month,
                "end_month": end_month,
                "start_date": start_date,
                "end_date": end_date,
                "with_sub_accounts": with_sub_accounts,
                "include_tax": include_tax,
                "journal_types": journal_types,
            },
        )
        return TBResponse.model_validate(data)

    @operation("getReportsTrialBalanceBalanceSheet")
    def trial_balance_bs(
        self,
        fiscal_year: int | None = None,
        start_month: int | None = None,
        end_month: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        with_sub_accounts: bool | None = None,
        include_tax: bool | None = None,
        journal_types: list[str] | None = None,
    ) -> TBResponse:
        """Balance-sheet trial balance. Specify fiscal_year+months OR a date range."""
        return self._trial_balance(
            "bs", fiscal_year, start_month, end_month, start_date, end_date,
            with_sub_accounts, include_tax, journal_types,
        )

    @operation("getReportsTrialBalanceProfitLoss")
    def trial_balance_pl(
        self,
        fiscal_year: int | None = None,
        start_month: int | None = None,
        end_month: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        with_sub_accounts: bool | None = None,
        include_tax: bool | None = None,
        journal_types: list[str] | None = None,
    ) -> TBResponse:
        """Profit-and-loss trial balance. Specify fiscal_year+months OR a date range."""
        return self._trial_balance(
            "pl", fiscal_year, start_month, end_month, start_date, end_date,
            with_sub_accounts, include_tax, journal_types,
        )

    def _transition(
        self,
        which: str,
        type: str,
        fiscal_year: int | None,
        start_month: int | None,
        end_month: int | None,
        with_sub_accounts: bool | None,
        include_tax: bool | None,
    ) -> TransitionResponse:
        data = self._client.get(
            f"/api/v3/reports/transition_{which}",
            params={
                "type": type,
                "fiscal_year": fiscal_year,
                "start_month": start_month,
                "end_month": end_month,
                "with_sub_accounts": with_sub_accounts,
                "include_tax": include_tax,
            },
        )
        return TransitionResponse.model_validate(data)

    @operation("getReportsTransitionBalanceSheet")
    def transition_bs(
        self,
        type: str,
        fiscal_year: int | None = None,
        start_month: int | None = None,
        end_month: int | None = None,
        with_sub_accounts: bool | None = None,
        include_tax: bool | None = None,
    ) -> TransitionResponse:
        """Month-over-month balance-sheet movement. `type` is the report variant
        (see docs/api/transition_balance_sheet.md)."""
        return self._transition(
            "bs", type, fiscal_year, start_month, end_month, with_sub_accounts, include_tax
        )

    @operation("getReportsTransitionProfitLoss")
    def transition_pl(
        self,
        type: str,
        fiscal_year: int | None = None,
        start_month: int | None = None,
        end_month: int | None = None,
        with_sub_accounts: bool | None = None,
        include_tax: bool | None = None,
    ) -> TransitionResponse:
        """Month-over-month profit-and-loss movement."""
        return self._transition(
            "pl", type, fiscal_year, start_month, end_month, with_sub_accounts, include_tax
        )
