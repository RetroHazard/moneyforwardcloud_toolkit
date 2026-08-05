"""MFClient — the single entry point to the Money Forward Cloud Accounting API.

Wires together auth (bearer token with auto-refresh), the rate-limited retrying
transport, error mapping, and one resource object per API area:

    client = MFClient.from_profile()          # uses stored OAuth tokens
    client.accounts.list(available=True)
    client.journals.iter_all(start_date="2026-04-01")
"""

from __future__ import annotations

import httpx

from mfcloud.auth.oauth import BearerAuth, TokenManager
from mfcloud.auth.store import TokenStore
from mfcloud.config import Config
from mfcloud.errors import raise_for_status
from mfcloud.http import BASE_URL, RateLimitedRetryTransport
from mfcloud.resources.accounts import AccountsResource, SubAccountsResource
from mfcloud.resources.journals import JournalsResource
from mfcloud.resources.masters import (
    ConnectedAccountsResource,
    DepartmentsResource,
    TaxesResource,
    TermSettingsResource,
)
from mfcloud.resources.offices import OfficesResource
from mfcloud.resources.reports import ReportsResource
from mfcloud.resources.trade_partners import TradePartnersResource
from mfcloud.resources.transactions import TransactionsResource
from mfcloud.resources.vouchers import VouchersResource


class MFClient:
    def __init__(
        self,
        auth: httpx.Auth | None = None,
        transport: httpx.BaseTransport | None = None,
        base_url: str = BASE_URL,
    ) -> None:
        self._http = httpx.Client(
            base_url=base_url,
            auth=auth,
            transport=RateLimitedRetryTransport(inner=transport),
            timeout=30.0,
        )
        self.offices = OfficesResource(self)
        self.accounts = AccountsResource(self)
        self.sub_accounts = SubAccountsResource(self)
        self.departments = DepartmentsResource(self)
        self.taxes = TaxesResource(self)
        self.term_settings = TermSettingsResource(self)
        self.connected_accounts = ConnectedAccountsResource(self)
        self.trade_partners = TradePartnersResource(self)
        self.journals = JournalsResource(self)
        self.transactions = TransactionsResource(self)
        self.reports = ReportsResource(self)
        self.vouchers = VouchersResource(self)

    @classmethod
    def from_profile(cls, profile: str | None = None) -> MFClient:
        """Build a client using stored OAuth tokens for a profile (= one office)."""
        config = Config.load()
        store = TokenStore()
        manager = TokenManager(
            store=store,
            profile=config.resolve_profile(profile),
            client_id=config.client_id,
            client_secret=store.load_client_secret() or "",
        )
        return cls(auth=BearerAuth(manager))

    # -- low-level ---------------------------------------------------------------

    def request(self, method: str, path: str, params: dict | None = None, json=None):
        clean = {k: v for k, v in (params or {}).items() if v is not None}
        response = self._http.request(method, path, params=clean, json=json)
        raise_for_status(response)
        return response.json() if response.content else None

    def get(self, path: str, params: dict | None = None):
        return self.request("GET", path, params=params)

    def post(self, path: str, json=None):
        return self.request("POST", path, json=json)

    def put(self, path: str, json=None):
        return self.request("PUT", path, json=json)

    def delete(self, path: str, json=None):
        return self.request("DELETE", path, json=json)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> MFClient:
        return self

    def __exit__(self, *exc) -> None:
        self.close()
