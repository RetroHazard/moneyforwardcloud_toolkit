"""All 8 write operations: correct bodies sent, responses parsed, validation enforced."""

import json

import pytest
from pydantic import ValidationError

from mfcloud.models.requests import (
    JournalizeRequest,
    NewJournal,
    NewJournalLine,
    NewJournalLineDetails,
    NewTradePartner,
    NewTransaction,
    VoucherFile,
)
from tests.unit import fixtures
from tests.unit.helpers import RecordingAPI, make_client


@pytest.fixture
def api():
    return RecordingAPI()


@pytest.fixture
def client(api):
    return make_client(api)


def sent_body(api) -> dict:
    return json.loads(api.last.content)


NEW_JOURNAL = NewJournal(
    transaction_date="2026-05-01",
    journal_type="NORMAL",
    branches=[
        NewJournalLine(
            remark="taxi",
            debitor=NewJournalLineDetails(value=1000, account_id="acc_travel"),
            creditor=NewJournalLineDetails(value=1000, account_id="acc_cash"),
        )
    ],
)


def test_create_journal(api, client):
    api.route("POST", "/api/v3/journals", {"journal": fixtures.JOURNAL})
    created = client.journals.create(NEW_JOURNAL)
    body = sent_body(api)
    assert body["journal"]["transaction_date"] == "2026-05-01"
    assert body["journal"]["branches"][0]["debitor"]["value"] == 1000
    assert "memo" not in body["journal"]  # None fields omitted
    assert created.id == "j1"


def test_create_journal_accepts_plain_dict(api, client):
    api.route("POST", "/api/v3/journals", {"journal": fixtures.JOURNAL})
    client.journals.create(NEW_JOURNAL.model_dump(exclude_none=True))
    assert sent_body(api)["journal"]["journal_type"] == "NORMAL"


def test_create_journal_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        NewJournal.model_validate(
            {**NEW_JOURNAL.model_dump(exclude_none=True), "not_a_field": 1}
        )


def test_update_journal(api, client):
    api.route("PUT", "/api/v3/journals/j1", {"journal": fixtures.JOURNAL})
    updated = client.journals.update("j1", NEW_JOURNAL)
    assert api.last.method == "PUT"
    assert updated.number == 1


def test_delete_journal(api, client):
    api.route("DELETE", "/api/v3/journals/j1", None, status=204)
    assert client.journals.delete("j1") is None
    assert api.last.method == "DELETE"
    assert api.last.url.path == "/api/v3/journals/j1"


def test_upload_vouchers(api, client):
    api.route("POST", "/api/v3/vouchers", {
        "voucher_file_ids": [{"file_name": "receipt.pdf", "file_id": "vf1"}]
    })
    result = client.vouchers.upload(
        [VoucherFile(file_name="receipt.pdf", file_data="aGVsbG8=")], journal_id="j1"
    )
    body = sent_body(api)
    assert body["journal_id"] == "j1"
    assert body["voucher_files"][0]["file_name"] == "receipt.pdf"
    assert result[0]["file_id"] == "vf1"


def test_upload_voucher_from_path(api, client, tmp_path):
    api.route("POST", "/api/v3/vouchers", {"voucher_file_ids": []})
    f = tmp_path / "receipt.png"
    f.write_bytes(b"\x89PNG fake")
    client.vouchers.upload_path(f)
    body = sent_body(api)
    assert body["voucher_files"][0]["file_name"] == "receipt.png"
    import base64

    assert base64.b64decode(body["voucher_files"][0]["file_data"]) == b"\x89PNG fake"


def test_delete_voucher(api, client):
    api.route("DELETE", "/api/v3/vouchers", None, status=204)
    client.vouchers.delete("j1", "vf1")
    assert sent_body(api) == {"journal_id": "j1", "voucher_file_id": "vf1"}


def test_create_trade_partners(api, client):
    api.route("POST", "/api/v3/trade_partners", {"trade_partners": [fixtures.TRADE_PARTNER]})
    created = client.trade_partners.create([NewTradePartner(name="取引先A")])
    assert sent_body(api)["trade_partners"][0]["name"] == "取引先A"
    assert created[0].code == "TP1"


def test_create_transactions(api, client):
    api.route("POST", "/api/v3/transactions", {
        "connected_account_id": "ca1",
        "transactions": [{"id": "tx9", "date": "2026-05-02", "value": 5400,
                          "side": "expense", "content": "タクシー"}],
    })
    created = client.transactions.create(
        "ca1", [NewTransaction(date="2026-05-02", value=5400, side="expense", content="タクシー")]
    )
    body = sent_body(api)
    assert body["connected_account_id"] == "ca1"
    assert created[0].id == "tx9"


def test_journalize_transaction(api, client):
    api.route("POST", "/api/v3/transactions/journalize", {"journal": fixtures.JOURNAL})
    entry = client.transactions.journalize(
        JournalizeRequest(transaction_id="tx1", account_id="acc_travel", tax_id="t1")
    )
    body = sent_body(api)
    assert body["transaction_id"] == "tx1"
    assert body["account_id"] == "acc_travel"
    assert entry.id == "j1"


def test_write_error_maps_to_validation_error(api, client):
    from mfcloud.errors import MFCValidationError

    api.route("POST", "/api/v3/journals", {
        "errors": [{"code": "invalid_request_body", "message": "debits != credits"}]
    }, status=400)
    with pytest.raises(MFCValidationError, match="debits != credits"):
        client.journals.create(NEW_JOURNAL)
