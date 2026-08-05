"""Report commands: trial balances and transition tables."""

from __future__ import annotations

import typer

from mfcloud.cli.common import PROFILE_OPTION, TABLE_OPTION, api_errors, emit, get_client

reports_app = typer.Typer(help="Reports (trial balance, transitions).")

FY = typer.Option(None, help="Fiscal year, e.g. 2026.")
SM = typer.Option(None, help="Start month 1-12.")
EM = typer.Option(None, help="End month 1-12.")
SD = typer.Option(None, help="Start date YYYY-MM-DD (alternative to fiscal year+months).")
ED = typer.Option(None, help="End date YYYY-MM-DD.")
WSA = typer.Option(None, "--with-sub-accounts/--without-sub-accounts")
IT = typer.Option(None, "--include-tax/--exclude-tax")


@reports_app.command("trial-balance-bs")
@api_errors
def trial_balance_bs(
    fiscal_year: int = FY, start_month: int = SM, end_month: int = EM,
    start_date: str = SD, end_date: str = ED,
    with_sub_accounts: bool = WSA, include_tax: bool = IT,
    profile: str = PROFILE_OPTION, table: bool = TABLE_OPTION,
):
    """Balance-sheet trial balance."""
    emit(get_client(profile).reports.trial_balance_bs(
        fiscal_year=fiscal_year, start_month=start_month, end_month=end_month,
        start_date=start_date, end_date=end_date,
        with_sub_accounts=with_sub_accounts, include_tax=include_tax), table)


@reports_app.command("trial-balance-pl")
@api_errors
def trial_balance_pl(
    fiscal_year: int = FY, start_month: int = SM, end_month: int = EM,
    start_date: str = SD, end_date: str = ED,
    with_sub_accounts: bool = WSA, include_tax: bool = IT,
    profile: str = PROFILE_OPTION, table: bool = TABLE_OPTION,
):
    """Profit-and-loss trial balance."""
    emit(get_client(profile).reports.trial_balance_pl(
        fiscal_year=fiscal_year, start_month=start_month, end_month=end_month,
        start_date=start_date, end_date=end_date,
        with_sub_accounts=with_sub_accounts, include_tax=include_tax), table)


@reports_app.command("transition-bs")
@api_errors
def transition_bs(
    type: str = typer.Option("transition_bs", help="Report variant."),
    fiscal_year: int = FY, start_month: int = SM, end_month: int = EM,
    with_sub_accounts: bool = WSA, include_tax: bool = IT,
    profile: str = PROFILE_OPTION, table: bool = TABLE_OPTION,
):
    """Month-over-month balance-sheet movement."""
    emit(get_client(profile).reports.transition_bs(
        type=type, fiscal_year=fiscal_year, start_month=start_month,
        end_month=end_month, with_sub_accounts=with_sub_accounts,
        include_tax=include_tax), table)


@reports_app.command("transition-pl")
@api_errors
def transition_pl(
    type: str = typer.Option("transition_pl", help="Report variant."),
    fiscal_year: int = FY, start_month: int = SM, end_month: int = EM,
    with_sub_accounts: bool = WSA, include_tax: bool = IT,
    profile: str = PROFILE_OPTION, table: bool = TABLE_OPTION,
):
    """Month-over-month profit-and-loss movement."""
    emit(get_client(profile).reports.transition_pl(
        type=type, fiscal_year=fiscal_year, start_month=start_month,
        end_month=end_month, with_sub_accounts=with_sub_accounts,
        include_tax=include_tax), table)
