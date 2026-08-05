"""CLI behavior: output modes, payload input, destructive gating, error mapping."""

import json

import pytest
from typer.testing import CliRunner

from mfcloud.cli import journals_cmd, masters_cmd, reports_cmd, transactions_cmd
from mfcloud.cli.app import app
from tests.unit import fixtures
from tests.unit.helpers import RecordingAPI, make_client

runner = CliRunner()


@pytest.fixture
def api(monkeypatch):
    recording = RecordingAPI()
    for module in (journals_cmd, masters_cmd, reports_cmd, transactions_cmd):
        monkeypatch.setattr(module, "get_client", lambda profile: make_client(recording))
    return recording


def test_office_get_outputs_json(api):
    api.route("GET", "/api/v3/offices", fixtures.OFFICE)
    result = runner.invoke(app, ["office", "get"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["name"] == "テスト株式会社"


def test_accounts_list_table_mode(api):
    api.route("GET", "/api/v3/accounts", {"accounts": [fixtures.ACCOUNT]})
    result = runner.invoke(app, ["accounts", "list", "--table"])
    assert result.exit_code == 0
    assert "現金" in result.stdout
    assert "{" not in result.stdout  # not JSON


def test_journals_list_passes_filters(api):
    api.route("GET", "/api/v3/journals", {
        "metadata": {"total_pages": 1, "total_count": 0}, "journals": [],
    })
    result = runner.invoke(
        app, ["journals", "list", "--start-date", "2026-04-01", "--per-page", "50"]
    )
    assert result.exit_code == 0
    params = api.last.url.params
    assert params["start_date"] == "2026-04-01"
    assert params["per_page"] == "50"


def test_journals_create_from_inline_json(api):
    api.route("POST", "/api/v3/journals", {"journal": fixtures.JOURNAL})
    payload = {
        "transaction_date": "2026-05-01", "journal_type": "NORMAL",
        "branches": [{"debitor": {"value": 1000, "account_id": "a"},
                      "creditor": {"value": 1000, "account_id": "b"}}],
    }
    result = runner.invoke(app, ["journals", "create", "--json", json.dumps(payload)])
    assert result.exit_code == 0
    assert json.loads(result.stdout)["id"] == "j1"


def test_journals_delete_refused_without_yes(api):
    result = runner.invoke(app, ["journals", "delete", "j1"], input="n\n")
    assert result.exit_code == 1
    assert not api.requests  # nothing sent


def test_journals_delete_with_yes(api):
    api.route("DELETE", "/api/v3/journals/j1", None, status=204)
    result = runner.invoke(app, ["journals", "delete", "j1", "--yes"])
    assert result.exit_code == 0
    assert api.last.method == "DELETE"


def test_vouchers_delete_gated(api):
    result = runner.invoke(
        app,
        ["vouchers", "delete", "--journal-id", "j1", "--voucher-file-id", "v1"],
        input="n\n",
    )
    assert result.exit_code == 1
    assert not api.requests


def test_vouchers_upload_file(api, tmp_path):
    api.route("POST", "/api/v3/vouchers", {"voucher_file_ids": [
        {"file_name": "r.pdf", "file_id": "vf1"}]})
    f = tmp_path / "r.pdf"
    f.write_bytes(b"pdf")
    result = runner.invoke(app, ["vouchers", "upload", str(f), "--journal-id", "j1"])
    assert result.exit_code == 0
    assert json.loads(result.stdout)[0]["file_id"] == "vf1"


def test_transactions_journalize(api):
    api.route("POST", "/api/v3/transactions/journalize", {"journal": fixtures.JOURNAL})
    result = runner.invoke(app, [
        "transactions", "journalize", "--json",
        json.dumps({"transaction_id": "tx1", "account_id": "a1"}),
    ])
    assert result.exit_code == 0
    assert json.loads(result.stdout)["id"] == "j1"


def test_reports_trial_balance(api):
    api.route("GET", "/api/v3/reports/trial_balance_bs", fixtures.TB_RESPONSE)
    result = runner.invoke(app, ["reports", "trial-balance-bs", "--fiscal-year", "2026"])
    assert result.exit_code == 0
    assert api.last.url.params["fiscal_year"] == "2026"


def test_api_error_exits_nonzero_with_english_message(api):
    api.route("GET", "/api/v3/departments", {
        "errors": [{"code": "unauthorized", "message": "Access token expired"}]
    }, status=401)
    result = runner.invoke(app, ["departments", "list"])
    assert result.exit_code == 1
    assert "Access token expired" in result.output


def test_payload_rejects_both_json_and_file(api, tmp_path):
    f = tmp_path / "x.json"
    f.write_text("{}")
    result = runner.invoke(
        app, ["journals", "create", "--json", "{}", "--file", str(f)]
    )
    assert result.exit_code == 2
