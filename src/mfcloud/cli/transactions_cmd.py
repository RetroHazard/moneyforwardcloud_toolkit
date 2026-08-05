"""Transaction (明細) commands."""

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

transactions_app = typer.Typer(help="Imported bank/card transactions.")


@transactions_app.command("list")
@api_errors
def transactions_list(
    start_date: str = typer.Option(..., help="YYYY-MM-DD (required)."),
    end_date: str = typer.Option(..., help="YYYY-MM-DD (required)."),
    connected_account_id: str = typer.Option(None),
    side: str = typer.Option(None, help="income or expense."),
    content: str = typer.Option(None, help="Filter by description text."),
    journalizing_status: list[str] = typer.Option(
        None, "--journalizing-status", help="Repeatable, e.g. not_journalized."
    ),
    page: int = typer.Option(None),
    per_page: int = typer.Option(None, help="1-100."),
    all_pages: bool = typer.Option(False, "--all", help="Fetch every page."),
    profile: str = PROFILE_OPTION,
    table: bool = TABLE_OPTION,
):
    """List transactions in a date window (one page unless --all)."""
    client = get_client(profile)
    filters = dict(
        connected_account_id=connected_account_id, side=side, content=content,
        journalizing_statuses=journalizing_status or None,
    )
    if all_pages:
        rows = list(client.transactions.iter_all(start_date, end_date, **filters))
        emit(rows, table, columns=["id", "date", "value", "side", "content",
                                   "journalizing_status"])
    else:
        emit(client.transactions.list(start_date, end_date, page=page,
                                      per_page=per_page, **filters), table)


@transactions_app.command("create")
@api_errors
def transactions_create(
    connected_account_id: str = typer.Option(..., "--connected-account-id"),
    json_arg: str = typer.Option(None, "--json", help='List of {date, value, side, content}.'),
    file_arg: Path = typer.Option(None, "--file"),
    profile: str = PROFILE_OPTION,
    table: bool = TABLE_OPTION,
):
    """Register manual transactions under a manual connected account."""
    payload = read_payload(json_arg, file_arg)
    if isinstance(payload, dict):
        payload = [payload]
    emit(get_client(profile).transactions.create(connected_account_id, payload), table)


@transactions_app.command("journalize")
@api_errors
def transactions_journalize(
    json_arg: str = typer.Option(None, "--json", help='{transaction_id, account_id, ...}.'),
    file_arg: Path = typer.Option(None, "--file"),
    profile: str = PROFILE_OPTION,
    table: bool = TABLE_OPTION,
):
    """Create a journal entry from an imported transaction."""
    emit(get_client(profile).transactions.journalize(read_payload(json_arg, file_arg)), table)
