"""Trade partners (customers/vendors)."""

from __future__ import annotations

from mfcloud.models.masters import TradePartner
from mfcloud.resources.base import Resource, operation


class TradePartnersResource(Resource):
    @operation("getTradePartners")
    def list(self, available: bool | None = None) -> list[TradePartner]:
        data = self._client.get("/api/v3/trade_partners", params={"available": available})
        return [TradePartner.model_validate(t) for t in data["trade_partners"]]
