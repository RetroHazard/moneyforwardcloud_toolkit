"""`mfc` — English CLI for the Money Forward Cloud Accounting API."""

from __future__ import annotations

import typer

from mfcloud.cli import auth_cmd, journals_cmd, masters_cmd, reports_cmd, transactions_cmd

app = typer.Typer(
    name="mfc",
    help="English toolkit for the Money Forward Cloud Accounting API.",
    no_args_is_help=True,
)
app.add_typer(auth_cmd.app, name="auth")
app.add_typer(masters_cmd.office_app, name="office")
app.add_typer(masters_cmd.accounts_app, name="accounts")
app.add_typer(masters_cmd.sub_accounts_app, name="sub-accounts")
app.add_typer(masters_cmd.departments_app, name="departments")
app.add_typer(masters_cmd.taxes_app, name="taxes")
app.add_typer(masters_cmd.term_settings_app, name="term-settings")
app.add_typer(masters_cmd.connected_accounts_app, name="connected-accounts")
app.add_typer(masters_cmd.trade_partners_app, name="trade-partners")
app.add_typer(journals_cmd.journals_app, name="journals")
app.add_typer(journals_cmd.vouchers_app, name="vouchers")
app.add_typer(transactions_cmd.transactions_app, name="transactions")
app.add_typer(reports_cmd.reports_app, name="reports")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
