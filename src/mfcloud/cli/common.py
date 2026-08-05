"""Shared CLI plumbing: client construction, JSON/table output, payload input,
destructive-action gating, error handling."""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from functools import wraps
from pathlib import Path

import typer
from pydantic import BaseModel

from mfcloud.client import MFClient
from mfcloud.errors import MFCloudError

PROFILE_OPTION = typer.Option(None, "--profile", help="Profile (one per office).")
TABLE_OPTION = typer.Option(
    False, "--table", help="Human-readable table instead of JSON."
)
YES_OPTION = typer.Option(False, "--yes", help="Skip the confirmation prompt.")


def get_client(profile: str | None) -> MFClient:
    return MFClient.from_profile(profile)


def to_jsonable(data):
    if isinstance(data, BaseModel):
        return data.model_dump()
    if isinstance(data, list):
        return [to_jsonable(x) for x in data]
    return data


def emit(data, table: bool = False, columns: list[str] | None = None) -> None:
    """Print JSON (default, machine-first) or a simple table for humans."""
    payload = to_jsonable(data)
    if not table:
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    rows = payload if isinstance(payload, list) else [payload]
    if not rows:
        typer.echo("(empty)")
        return
    columns = columns or [k for k in rows[0] if not isinstance(rows[0][k], (dict, list))]
    widths = {
        c: max(len(c), *(len(str(r.get(c, ""))) for r in rows)) for c in columns
    }
    typer.echo("  ".join(c.ljust(widths[c]) for c in columns))
    for r in rows:
        typer.echo("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in columns))


def read_payload(json_arg: str | None, file_arg: Path | None) -> dict:
    """Request body from --json, --file, or piped stdin (exactly one source)."""
    sources = [s for s in (json_arg, file_arg) if s is not None]
    if len(sources) > 1:
        typer.echo("Give the payload via --json OR --file, not both.", err=True)
        raise typer.Exit(2)
    if json_arg is not None:
        return json.loads(json_arg)
    if file_arg is not None:
        return json.loads(file_arg.read_text(encoding="utf-8"))
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    typer.echo("Provide a payload: --json '<...>', --file <path>, or pipe JSON in.", err=True)
    raise typer.Exit(2)


def confirm_destructive(description: str, yes: bool) -> None:
    if yes:
        return
    if not typer.confirm(f"{description} — continue?"):
        typer.echo("Aborted.")
        raise typer.Exit(1)


def api_errors(func: Callable) -> Callable:
    """Map API exceptions to a one-line English stderr message and exit 1."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MFCloudError as exc:
            typer.echo(f"error: {exc}", err=True)
            raise typer.Exit(1) from exc

    return wrapper
