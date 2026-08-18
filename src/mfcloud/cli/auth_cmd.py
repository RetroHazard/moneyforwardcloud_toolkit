"""`mfc auth` — login, status, logout."""

from __future__ import annotations

import time

import typer

from mfcloud.auth.oauth import login as oauth_login
from mfcloud.auth.store import TokenStore
from mfcloud.config import Config

app = typer.Typer(help="Authenticate with Money Forward (OAuth 2.0).")


@app.command()
def login(
    profile: str = typer.Option(None, "--profile", help="Profile (one per office)."),
    client_id: str = typer.Option(None, "--client-id", help="OAuth Client ID (saved to config)."),
    client_secret: str = typer.Option(
        None,
        "--client-secret",
        help=(
            "OAuth Client Secret (saved to the OS keyring). Prefer omitting this flag —"
            " you'll be prompted with hidden input, keeping the secret out of shell history."
        ),
    ),
    manual: bool = typer.Option(
        False, "--manual", help="Print the URL and paste the redirect back (no local server)."
    ),
):
    """Log in to Money Forward and store tokens for PROFILE in the OS keyring."""
    config = Config.load()
    store = TokenStore()
    if client_id:
        config.client_id = client_id
        config.save()
    if client_secret:
        store.save_client_secret(client_secret.strip())
    if not config.client_id:
        typer.echo(
            "No Client ID configured. Register an OAuth app first (see docs/oauth-setup.md),"
            " then run: mfc auth login --client-id <ID> --client-secret <SECRET>",
            err=True,
        )
        raise typer.Exit(2)
    secret = store.load_client_secret()
    if not secret:
        secret = typer.prompt("Client Secret (input hidden, saved to OS keyring)",
                              hide_input=True).strip()
        store.save_client_secret(secret)

    resolved = config.resolve_profile(profile)
    tokens = oauth_login(config.client_id, secret, config.redirect_port, manual=manual)
    store.save_tokens(resolved, tokens)
    typer.echo(f"Logged in. Tokens stored for profile '{resolved}'.")


@app.command()
def status(profile: str = typer.Option(None, "--profile")):
    """Show whether PROFILE has stored tokens and when they expire."""
    config = Config.load()
    resolved = config.resolve_profile(profile)
    tokens = TokenStore().load_tokens(resolved)
    if tokens is None:
        typer.echo(f"Profile '{resolved}': not logged in.")
        raise typer.Exit(1)
    remaining = int(tokens.expires_at - time.time())
    state = f"expires in {remaining}s" if remaining > 0 else "expired (will auto-refresh on use)"
    typer.echo(f"Profile '{resolved}': logged in, access token {state}.")
    typer.echo(f"Scopes: {' '.join(tokens.scopes) or '(unknown)'}")


@app.command()
def logout(profile: str = typer.Option(None, "--profile")):
    """Delete stored tokens for PROFILE."""
    config = Config.load()
    resolved = config.resolve_profile(profile)
    TokenStore().delete_tokens(resolved)
    typer.echo(f"Profile '{resolved}': tokens deleted.")
