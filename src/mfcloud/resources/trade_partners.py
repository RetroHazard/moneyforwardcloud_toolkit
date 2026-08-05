"""Trade partners (customers/vendors)."""

from __future__ import annotations

from mfcloud.models.masters import TradePartner
from mfcloud.models.requests import NewTradePartner
from mfcloud.resources.base import Resource, operation


class TradePartnersResource(Resource):
    @operation("getTradePartners")
    def list(self, available: bool | None = None) -> list[TradePartner]:
        data = self._client.get("/api/v3/trade_partners", params={"available": available})
        return [TradePartner.model_validate(t) for t in data["trade_partners"]]

    @operation("postTradePartners")
    def create(self, partners: list[NewTradePartner | dict]) -> list[TradePartner]:
        """Register one or more trade partners."""
        body = {
            "trade_partners": [
                NewTradePartner.model_validate(p).model_dump(exclude_none=True)
                for p in partners
            ]
        }
        data = self._client.post("/api/v3/trade_partners", json=body)
        return [TradePartner.model_validate(t) for t in data["trade_partners"]]
