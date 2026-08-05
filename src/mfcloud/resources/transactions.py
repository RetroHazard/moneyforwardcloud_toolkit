"""Imported bank/card transactions (明細)."""

from __future__ import annotations

from collections.abc import Iterator

from mfcloud.models.transactions import GetTransactionsResponse, Transaction
from mfcloud.resources.base import Resource, operation


class TransactionsResource(Resource):
    @operation("getTransactions")
    def list(
        self,
        start_date: str,
        end_date: str,
        connected_account_id: str | None = None,
        connected_sub_account_id: str | None = None,
        value_min: int | None = None,
        value_max: int | None = None,
        side: str | None = None,
        content: str | None = None,
        content_match_type: str | None = None,
        journalizing_statuses: list[str] | None = None,
        order: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> GetTransactionsResponse:
        """One page of transactions in [start_date, end_date] (both required)."""
        data = self._client.get(
            "/api/v3/transactions",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "connected_account_id": connected_account_id,
                "connected_sub_account_id": connected_sub_account_id,
                "value_min": value_min,
                "value_max": value_max,
                "side": side,
                "content": content,
                "content_match_type": content_match_type,
                "journalizing_statuses": journalizing_statuses,
                "order": order,
                "page": page,
                "per_page": per_page,
            },
        )
        return GetTransactionsResponse.model_validate(data)

    def iter_all(
        self, start_date: str, end_date: str, per_page: int = 100, **filters
    ) -> Iterator[Transaction]:
        """Every transaction in the window, walking all pages."""
        page = 1
        while True:
            response = self.list(start_date, end_date, page=page, per_page=per_page, **filters)
            yield from response.transactions
            if page >= response.metadata.total_pages:
                return
            page += 1
