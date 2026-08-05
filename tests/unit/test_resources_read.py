"""All 15 GET operations: correct request shape, response parsed into typed models."""

import pytest

from tests.unit import fixtures
from tests.unit.helpers import RecordingAPI, make_client


@pytest.fixture
def api():
    return RecordingAPI()


@pytest.fixture
def client(api):
    return make_client(api)


def test_current_office(api, client):
    api.route("GET", "/api/v3/offices", fixtures.OFFICE)
    office = client.offices.current()
    assert office.name == "テスト株式会社"
    assert office.accounting_periods[0].fiscal_year == 2026


def test_list_accounts(api, client):
    api.route("GET", "/api/v3/accounts", {"accounts": [fixtures.ACCOUNT]})
    accounts = client.accounts.list(available=True)
    assert api.last.url.params["available"] == "true"
    assert accounts[0].name == "現金"
    assert accounts[0].sub_accounts[0].id == "sub1"


def test_list_accounts_omits_none_params(api, client):
    api.route("GET", "/api/v3/accounts", {"accounts": []})
    client.accounts.list()
    assert "available" not in api.last.url.params


def test_list_sub_accounts(api, client):
    api.route("GET", "/api/v3/sub_accounts", {"sub_accounts": [fixtures.SUB_ACCOUNT]})
    subs = client.sub_accounts.list(account_id="acc1")
    assert api.last.url.params["account_id"] == "acc1"
    assert subs[0].name == "本店"


def test_list_departments(api, client):
    api.route("GET", "/api/v3/departments", {"departments": [fixtures.DEPARTMENT]})
    assert client.departments.list()[0].name == "営業部"


def test_list_taxes(api, client):
    api.route("GET", "/api/v3/taxes", {"taxes": [fixtures.TAX]})
    taxes = client.taxes.list()
    assert taxes[0].tax_rate == 0.1


def test_list_term_settings(api, client):
    api.route("GET", "/api/v3/term_settings", {"term_settings": [fixtures.TERM_SETTING]})
    assert client.term_settings.list()[0].fiscal_year == 2026


def test_list_connected_accounts(api, client):
    api.route(
        "GET", "/api/v3/connected_accounts", {"connected_accounts": [fixtures.CONNECTED_ACCOUNT]}
    )
    connected = client.connected_accounts.list()
    assert connected[0].connected_sub_accounts[0].id == "csa1"


def test_list_trade_partners(api, client):
    api.route("GET", "/api/v3/trade_partners", {"trade_partners": [fixtures.TRADE_PARTNER]})
    assert client.trade_partners.list()[0].code == "TP1"


def test_list_journals_with_filters(api, client):
    api.route("GET", "/api/v3/journals", {
        "metadata": {"total_pages": 1, "total_count": 1}, "journals": [fixtures.JOURNAL],
    })
    response = client.journals.list(start_date="2026-04-01", end_date="2026-06-30", page=1)
    params = api.last.url.params
    assert params["start_date"] == "2026-04-01"
    assert params["page"] == "1"
    entry = response.journals[0]
    assert entry.branches[0].debitor.value == 1000
    assert response.metadata.total_count == 1


def test_get_journal_by_id(api, client):
    api.route("GET", "/api/v3/journals/j1", {"journal": fixtures.JOURNAL})
    entry = client.journals.get("j1")
    assert entry.id == "j1"


def test_journals_iter_all_walks_pages(api, client):
    pages = {
        1: {"metadata": {"total_pages": 2, "total_count": 2},
            "journals": [{**fixtures.JOURNAL, "id": "j1"}]},
        2: {"metadata": {"total_pages": 2, "total_count": 2},
            "journals": [{**fixtures.JOURNAL, "id": "j2"}]},
    }

    def handler(request):
        api.requests.append(request)
        import httpx

        page = int(request.url.params.get("page", 1))
        return httpx.Response(200, json=pages[page])

    import httpx

    from mfcloud.client import MFClient

    client = MFClient(transport=httpx.MockTransport(handler))
    ids = [j.id for j in client.journals.iter_all(per_page=1)]
    assert ids == ["j1", "j2"]


def test_list_transactions(api, client):
    api.route("GET", "/api/v3/transactions", {
        "transactions": [fixtures.TRANSACTION],
        "metadata": {"total_pages": 1, "total_count": 1},
    })
    response = client.transactions.list("2026-05-01", "2026-05-31", side="expense")
    params = api.last.url.params
    assert params["side"] == "expense"
    assert response.transactions[0].value == 5400


def test_trial_balance_reports(api, client):
    api.route("GET", "/api/v3/reports/trial_balance_bs", fixtures.TB_RESPONSE)
    api.route("GET", "/api/v3/reports/trial_balance_pl", fixtures.TB_RESPONSE)
    bs = client.reports.trial_balance_bs(fiscal_year=2026, with_sub_accounts=True)
    assert api.last.url.params["with_sub_accounts"] == "true"
    assert bs.rows[0].rows[0].name == "現金"
    assert bs.rows[0].values[-1] is None
    client.reports.trial_balance_pl(start_date="2026-04-01", end_date="2026-06-30")
    assert api.last.url.params["start_date"] == "2026-04-01"


def test_transition_reports(api, client):
    api.route("GET", "/api/v3/reports/transition_bs", fixtures.TRANSITION_RESPONSE)
    api.route("GET", "/api/v3/reports/transition_pl", fixtures.TRANSITION_RESPONSE)
    report = client.reports.transition_pl(type="transition_pl", fiscal_year=2026)
    assert api.last.url.params["type"] == "transition_pl"
    assert report.rows[0].values == [100, 200, None, 300]
    client.reports.transition_bs(type="transition_bs")


def test_error_response_raises_typed_error(api, client):
    from mfcloud.errors import MFCNotFoundError

    with pytest.raises(MFCNotFoundError):
        client.journals.get("missing")
