"""Read-only master-data commands: office, accounts, departments, taxes, etc."""

from __future__ import annotations

from pathlib import Path

import typer

from mfcloud.cli.common import (
    PROFILE_OPTION,
    TABLE_OPTION,
    api_errors,
    emit,
    get_client,
    read_payload,
)

office_app = typer.Typer(help="Office (business entity) info.")
accounts_app = typer.Typer(help="Chart of accounts.")
sub_accounts_app = typer.Typer(help="Sub-accounts.")
departments_app = typer.Typer(help="Departments.")
taxes_app = typer.Typer(help="Tax categories.")
term_settings_app = typer.Typer(help="Accounting-period settings.")
connected_accounts_app = typer.Typer(help="Connected services (bank/card feeds).")
trade_partners_app = typer.Typer(help="Trade partners (customers/vendors).")


@office_app.command("get")
@api_errors
def office_get(profile: str = PROFILE_OPTION, table: bool = TABLE_OPTION):
    """Show the office this profile's token is authorized for."""
    emit(get_client(profile).offices.current(), table)


@accounts_app.command("list")
@api_errors
def accounts_list(
    available: bool = typer.Option(None, "--available/--unavailable", help="Filter by in-use."),
    profile: str = PROFILE_OPTION,
    table: bool = TABLE_OPTION,
):
    """List accounts (with nested sub-accounts)."""
    emit(get_client(profile).accounts.list(available=available), table,
         columns=["id", "name", "account_group", "category", "available"])


@sub_accounts_app.command("list")
@api_errors
def sub_accounts_list(
    account_id: str = typer.Option(None, "--account-id"),
    profile: str = PROFILE_OPTION,
    table: bool = TABLE_OPTION,
):
    emit(get_client(profile).sub_accounts.list(account_id=account_id), table)


@departments_app.command("list")
@api_errors
def departments_list(profile: str = PROFILE_OPTION, table: bool = TABLE_OPTION):
    emit(get_client(profile).departments.list(), table)


@taxes_app.command("list")
@api_errors
def taxes_list(
    available: bool = typer.Option(None, "--available/--unavailable"),
    profile: str = PROFILE_OPTION,
    table: bool = TABLE_OPTION,
):
    emit(get_client(profile).taxes.list(available=available), table)


@term_settings_app.command("list")
@api_errors
def term_settings_list(profile: str = PROFILE_OPTION, table: bool = TABLE_OPTION):
    emit(get_client(profile).term_settings.list(), table)


@connected_accounts_app.command("list")
@api_errors
def connected_accounts_list(profile: str = PROFILE_OPTION, table: bool = TABLE_OPTION):
    emit(get_client(profile).connected_accounts.list(), table,
         columns=["id", "name", "is_manual", "account_id"])


@trade_partners_app.command("list")
@api_errors
def trade_partners_list(
    available: bool = typer.Option(None, "--available/--unavailable"),
    profile: str = PROFILE_OPTION,
    table: bool = TABLE_OPTION,
):
    emit(get_client(profile).trade_partners.list(available=available), table)


@trade_partners_app.command("create")
@api_errors
def trade_partners_create(
    json_arg: str = typer.Option(None, "--json", help='e.g. \'[{"name": "..."}]\''),
    file_arg: Path = typer.Option(None, "--file", help="JSON file with a list of partners."),
    profile: str = PROFILE_OPTION,
    table: bool = TABLE_OPTION,
):
    """Create trade partners from a JSON list of {name, search_key?, ...}."""
    payload = read_payload(json_arg, file_arg)
    if isinstance(payload, dict):
        payload = [payload]
    emit(get_client(profile).trade_partners.create(payload), table)
