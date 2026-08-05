"""`mfc` — English CLI for the Money Forward Cloud Accounting API."""

from __future__ import annotations

import typer

from mfcloud.cli import auth_cmd

app = typer.Typer(
    name="mfc",
    help="English toolkit for the Money Forward Cloud Accounting API.",
    no_args_is_help=True,
)
app.add_typer(auth_cmd.app, name="auth")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
