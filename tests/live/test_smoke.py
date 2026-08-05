"""Live read-only smoke tests against the real API.

Never run by default. Requires:
  1. A registered OAuth app and a logged-in profile (`mfc auth login`).
  2. MFC_LIVE_TEST=1 in the environment (and optionally MFC_PROFILE).

Run: MFC_LIVE_TEST=1 uv run pytest tests/live -v
"""

import os

import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("MFC_LIVE_TEST") != "1",
    reason="live tests disabled (set MFC_LIVE_TEST=1 and log in first)",
)


@pytest.fixture(scope="module")
def client():
    from mfcloud.client import MFClient

    with MFClient.from_profile() as c:
        yield c


def test_office(client):
    office = client.offices.current()
    assert office.name
    assert office.accounting_periods


def test_accounts(client):
    accounts = client.accounts.list(available=True)
    assert accounts
    assert all(a.id for a in accounts)


def test_taxes(client):
    assert client.taxes.list()


def test_journals_first_page(client):
    response = client.journals.list(per_page=10)
    assert response.metadata.total_count >= 0


def test_rate_limiter_paces_burst(client):
    # 4 quick calls must not trip the server-side limiter (3 req/s).
    for _ in range(4):
        client.offices.current()
