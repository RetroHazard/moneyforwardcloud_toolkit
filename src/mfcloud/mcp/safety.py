"""Confirm/preview protocol for destructive MCP tools.

A destructive tool called without confirm=True performs NO change: it fetches the
target and returns a preview describing exactly what would happen, instructing the
model to show the user and call again with confirm=True. Deterministic safety that
doesn't depend on prompt discipline.
"""

from __future__ import annotations

from mfcloud.models.journals import JournalItem


def journal_summary(journal: JournalItem) -> dict:
    lines = []
    for branch in journal.branches:
        for side_name in ("debitor", "creditor"):
            side = getattr(branch, side_name)
            if side is not None:
                lines.append({
                    "side": side_name,
                    "account": side.account_name,
                    "value": side.value,
                })
    return {
        "id": journal.id,
        "number": journal.number,
        "transaction_date": journal.transaction_date,
        "journal_type": journal.journal_type,
        "lines": lines,
        "memo": journal.memo,
    }


def preview(action: str, target: dict) -> dict:
    return {
        "status": "confirmation_required",
        "action": action,
        "target": target,
        "message": (
            f"No change made. This call would {action}. Show this preview to the user,"
            " and only if they agree, call the same tool again with confirm=true."
        ),
    }
