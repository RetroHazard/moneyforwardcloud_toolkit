"""Journal entry and voucher commands."""

from __future__ import annotations

from pathlib import Path

import typer

from mfcloud.cli.common import (
    PROFILE_OPTION,
    TABLE_OPTION,
    YES_OPTION,
    api_errors,
    confirm_destructive,
    emit,
    get_client,
    read_payload,
)

journals_app = typer.Typer(help="Journal entries.")
vouchers_app = typer.Typer(help="Vouchers (receipt files on journal entries).")


@journals_app.command("list")
@api_errors
def journals_list(
    start_date: str = typer.Option(None, help="YYYY-MM-DD, filters transaction_date."),
    end_date: str = typer.Option(None, help="YYYY-MM-DD."),
    account_id: str = typer.Option(None),
    is_realized: bool = typer.Option(None, "--realized/--unrealized"),
    page: int = typer.Option(None),
    per_page: int = typer.Option(None, help="1-100."),
    all_pages: bool = typer.Option(False, "--all", help="Fetch every page."),
    profile: str = PROFILE_OPTION,
    table: bool = TABLE_OPTION,
):
    """List journal entries (one page unless --all)."""
    client = get_client(profile)
    filters = dict(
        start_date=start_date, end_date=end_date, account_id=account_id,
        is_realized=is_realized,
    )
    if all_pages:
        entries = list(client.journals.iter_all(**filters))
        emit(entries, table, columns=["id", "number", "transaction_date", "journal_type"])
    else:
        response = client.journals.list(page=page, per_page=per_page, **filters)
        emit(response, table)


@journals_app.command("get")
@api_errors
def journals_get(
    journal_id: str = typer.Argument(...),
    profile: str = PROFILE_OPTION,
    table: bool = TABLE_OPTION,
):
    emit(get_client(profile).journals.get(journal_id), table)


@journals_app.command("create")
@api_errors
def journals_create(
    json_arg: str = typer.Option(None, "--json"),
    file_arg: Path = typer.Option(None, "--file"),
    profile: str = PROFILE_OPTION,
    table: bool = TABLE_OPTION,
):
    """Create a journal entry from JSON: {transaction_date, journal_type, branches: [...]}."""
    emit(get_client(profile).journals.create(read_payload(json_arg, file_arg)), table)


@journals_app.command("update")
@api_errors
def journals_update(
    journal_id: str = typer.Argument(...),
    json_arg: str = typer.Option(None, "--json"),
    file_arg: Path = typer.Option(None, "--file"),
    yes: bool = YES_OPTION,
    profile: str = PROFILE_OPTION,
    table: bool = TABLE_OPTION,
):
    """Replace a journal entry (full update — send every line)."""
    payload = read_payload(json_arg, file_arg)
    confirm_destructive(f"Overwrite journal {journal_id}", yes)
    emit(get_client(profile).journals.update(journal_id, payload), table)


@journals_app.command("delete")
@api_errors
def journals_delete(
    journal_id: str = typer.Argument(...),
    yes: bool = YES_OPTION,
    profile: str = PROFILE_OPTION,
):
    """Permanently delete a journal entry."""
    confirm_destructive(f"Permanently delete journal {journal_id}", yes)
    get_client(profile).journals.delete(journal_id)
    typer.echo(f"Deleted journal {journal_id}.")


@vouchers_app.command("upload")
@api_errors
def vouchers_upload(
    path: Path = typer.Argument(..., exists=True, readable=True, help="Local file to upload."),
    journal_id: str = typer.Option(None, "--journal-id", help="Attach to this journal entry."),
    profile: str = PROFILE_OPTION,
    table: bool = TABLE_OPTION,
):
    """Upload a local file as a voucher (base64 handled for you)."""
    emit(get_client(profile).vouchers.upload_path(path, journal_id), table)


@vouchers_app.command("delete")
@api_errors
def vouchers_delete(
    journal_id: str = typer.Option(..., "--journal-id"),
    voucher_file_id: str = typer.Option(..., "--voucher-file-id"),
    yes: bool = YES_OPTION,
    profile: str = PROFILE_OPTION,
):
    """Delete a voucher file from a journal entry."""
    confirm_destructive(
        f"Delete voucher {voucher_file_id} from journal {journal_id}", yes
    )
    get_client(profile).vouchers.delete(journal_id, voucher_file_id)
    typer.echo(f"Deleted voucher {voucher_file_id}.")
