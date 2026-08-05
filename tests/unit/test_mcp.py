"""MCP server tests over FastMCP's in-memory client — no process, no network."""

import asyncio
import json

import pytest
from fastmcp import Client

import mfcloud.mcp.server as server
from tests.unit import fixtures
from tests.unit.helpers import RecordingAPI, make_client

EXPECTED_TOOLS = {
    "get_office", "list_accounts", "list_sub_accounts", "list_departments",
    "list_taxes", "list_term_settings", "list_connected_accounts",
    "list_trade_partners", "list_journals", "get_journal", "list_transactions",
    "get_report",
    "create_journal", "update_journal", "delete_journal",
    "upload_voucher", "delete_voucher",
    "create_trade_partners", "create_transactions", "journalize_transaction",
}

DESTRUCTIVE_TOOLS = {"update_journal", "delete_journal", "delete_voucher"}


def run(coro):
    return asyncio.run(coro)


@pytest.fixture
def api(monkeypatch):
    recording = RecordingAPI()
    monkeypatch.setattr(server, "_client", make_client(recording))
    return recording


def call(tool: str, **arguments):
    async def _go():
        async with Client(server.mcp) as client:
            result = await client.call_tool(tool, arguments)
            return result.data

    return run(_go())


def test_tool_surface_and_annotations():
    async def _go():
        async with Client(server.mcp) as client:
            return await client.list_tools()

    tools = {t.name: t for t in run(_go())}
    assert set(tools) == EXPECTED_TOOLS
    for name, tool in tools.items():
        annotations = tool.annotations
        assert annotations is not None, f"{name} missing annotations"
        if name in DESTRUCTIVE_TOOLS:
            assert annotations.destructiveHint is True
        elif name.startswith(("get_", "list_")):
            assert annotations.readOnlyHint is True


def test_read_tool_roundtrip(api):
    api.route("GET", "/api/v3/accounts", {"accounts": [fixtures.ACCOUNT]})
    data = call("list_accounts", available=True)
    assert data[0]["name"] == "現金"
    assert api.last.url.params["available"] == "true"


def test_get_report_collapses_four_endpoints(api):
    api.route("GET", "/api/v3/reports/trial_balance_pl", fixtures.TB_RESPONSE)
    api.route("GET", "/api/v3/reports/transition_bs", fixtures.TRANSITION_RESPONSE)
    tb = call("get_report", report_type="trial_balance_pl", fiscal_year=2026)
    assert tb["report_type"] == "trial_balance_bs"  # fixture value; endpoint was pl
    assert api.last.url.path.endswith("trial_balance_pl")
    tr = call("get_report", report_type="transition_bs", fiscal_year=2026)
    assert api.last.url.path.endswith("transition_bs")
    assert tr["fiscal_year"] == 2026


def test_create_journal(api):
    api.route("POST", "/api/v3/journals", {"journal": fixtures.JOURNAL})
    result = call("create_journal", journal={
        "transaction_date": "2026-05-01", "journal_type": "NORMAL",
        "branches": [{"debitor": {"value": 1000, "account_id": "a"},
                      "creditor": {"value": 1000, "account_id": "b"}}],
    })
    assert result["id"] == "j1"
    assert json.loads(api.last.content)["journal"]["journal_type"] == "NORMAL"


def test_delete_journal_previews_without_confirm(api):
    api.route("GET", "/api/v3/journals/j1", {"journal": fixtures.JOURNAL})
    result = call("delete_journal", journal_id="j1")
    assert result["status"] == "confirmation_required"
    assert result["target"]["id"] == "j1"
    # Only a GET happened — nothing was deleted.
    assert all(r.method == "GET" for r in api.requests)


def test_delete_journal_with_confirm_deletes(api):
    api.route("DELETE", "/api/v3/journals/j1", None, status=204)
    result = call("delete_journal", journal_id="j1", confirm=True)
    assert result["status"] == "deleted"
    assert api.last.method == "DELETE"


def test_update_journal_previews_then_updates(api):
    api.route("GET", "/api/v3/journals/j1", {"journal": fixtures.JOURNAL})
    api.route("PUT", "/api/v3/journals/j1", {"journal": fixtures.JOURNAL})
    new_journal = {
        "transaction_date": "2026-05-02", "journal_type": "NORMAL",
        "branches": [{"debitor": {"value": 2000, "account_id": "a"},
                      "creditor": {"value": 2000, "account_id": "b"}}],
    }
    previewed = call("update_journal", journal_id="j1", journal=new_journal)
    assert previewed["status"] == "confirmation_required"
    assert all(r.method == "GET" for r in api.requests)
    updated = call("update_journal", journal_id="j1", journal=new_journal, confirm=True)
    assert updated["id"] == "j1"
    assert api.last.method == "PUT"


def test_delete_voucher_gated(api):
    api.route("GET", "/api/v3/journals/j1", {"journal": fixtures.JOURNAL})
    result = call("delete_voucher", journal_id="j1", voucher_file_id="vf1")
    assert result["status"] == "confirmation_required"


def test_upload_voucher_base64(api):
    api.route("POST", "/api/v3/vouchers", {
        "voucher_file_ids": [{"file_name": "r.pdf", "file_id": "vf1"}]
    })
    result = call("upload_voucher", file_name="r.pdf",
                  file_data_base64="aGVsbG8=", journal_id="j1")
    assert result[0]["file_id"] == "vf1"


def test_journalize_transaction(api):
    api.route("POST", "/api/v3/transactions/journalize", {"journal": fixtures.JOURNAL})
    result = call("journalize_transaction",
                  request={"transaction_id": "tx1", "account_id": "a1"})
    assert result["id"] == "j1"


def test_reference_resources():
    async def _go():
        async with Client(server.mcp) as client:
            index = await client.read_resource("spec://reference")
            page = await client.read_resource("spec://reference/journals")
            return index, page

    index, page = run(_go())
    assert "English Reference" in index[0].text
    assert "getJournals" in page[0].text
