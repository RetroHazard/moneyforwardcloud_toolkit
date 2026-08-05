"""Master-data endpoints: departments, taxes, term settings, connected services."""

from __future__ import annotations

from mfcloud.models.masters import ConnectedAccount, Department, Tax, TermSetting
from mfcloud.resources.base import Resource, operation


class DepartmentsResource(Resource):
    @operation("getDepartments")
    def list(self) -> list[Department]:
        data = self._client.get("/api/v3/departments")
        return [Department.model_validate(d) for d in data["departments"]]


class TaxesResource(Resource):
    @operation("getTaxes")
    def list(self, available: bool | None = None) -> list[Tax]:
        """Tax categories. available=True limits to those currently in use."""
        data = self._client.get("/api/v3/taxes", params={"available": available})
        return [Tax.model_validate(t) for t in data["taxes"]]


class TermSettingsResource(Resource):
    @operation("getTermSettings")
    def list(self) -> list[TermSetting]:
        """Accounting-period settings for every fiscal year."""
        data = self._client.get("/api/v3/term_settings")
        return [TermSetting.model_validate(t) for t in data["term_settings"]]


class ConnectedAccountsResource(Resource):
    @operation("getConnectedAccounts")
    def list(self) -> list[ConnectedAccount]:
        """Connected services (bank/card feeds), including manual accounts."""
        data = self._client.get("/api/v3/connected_accounts")
        return [ConnectedAccount.model_validate(c) for c in data["connected_accounts"]]
