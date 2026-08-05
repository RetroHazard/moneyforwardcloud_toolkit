"""Accounts (chart of accounts) and sub-accounts."""

from __future__ import annotations

from mfcloud.models.accounts import Account, SubAccount
from mfcloud.resources.base import Resource, operation


class AccountsResource(Resource):
    @operation("getAccounts")
    def list(self, available: bool | None = None) -> list[Account]:
        """All accounts, each with its nested sub-accounts.

        available=True limits to accounts currently in use.
        """
        data = self._client.get("/api/v3/accounts", params={"available": available})
        return [Account.model_validate(a) for a in data["accounts"]]


class SubAccountsResource(Resource):
    @operation("getSubAccounts")
    def list(self, account_id: str | None = None) -> list[SubAccount]:
        """Sub-accounts, optionally only those under one account."""
        data = self._client.get("/api/v3/sub_accounts", params={"account_id": account_id})
        return [SubAccount.model_validate(s) for s in data["sub_accounts"]]
