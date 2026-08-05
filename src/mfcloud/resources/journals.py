"""Journal entries."""

from __future__ import annotations

from collections.abc import Iterator

from mfcloud.models.journals import GetJournalsResponse, JournalItem
from mfcloud.models.requests import NewJournal
from mfcloud.resources.base import Resource, operation


class JournalsResource(Resource):
    @operation("getJournals")
    def list(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        account_id: str | None = None,
        is_realized: bool | None = None,
        transaction_ids: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> GetJournalsResponse:
        """One page of journal entries (dates filter on transaction_date)."""
        data = self._client.get(
            "/api/v3/journals",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "account_id": account_id,
                "is_realized": is_realized,
                "transaction_ids": transaction_ids,
                "page": page,
                "per_page": per_page,
            },
        )
        return GetJournalsResponse.model_validate(data)

    def iter_all(self, per_page: int = 100, **filters) -> Iterator[JournalItem]:
        """Every journal entry matching the filters, walking all pages."""
        page = 1
        while True:
            response = self.list(page=page, per_page=per_page, **filters)
            yield from response.journals
            if page >= response.metadata.total_pages:
                return
            page += 1

    @operation("getJournalById")
    def get(self, journal_id: str) -> JournalItem:
        data = self._client.get(f"/api/v3/journals/{journal_id}")
        return JournalItem.model_validate(data["journal"])

    @operation("postJournals")
    def create(self, journal: NewJournal | dict) -> JournalItem:
        """Create a journal entry. Debits and credits must balance."""
        body = {"journal": NewJournal.model_validate(journal).model_dump(exclude_none=True)}
        data = self._client.post("/api/v3/journals", json=body)
        return JournalItem.model_validate(data["journal"])

    @operation("putJournals")
    def update(self, journal_id: str, journal: NewJournal | dict) -> JournalItem:
        """Replace a journal entry (full update — send every line, not a diff)."""
        body = {"journal": NewJournal.model_validate(journal).model_dump(exclude_none=True)}
        data = self._client.put(f"/api/v3/journals/{journal_id}", json=body)
        return JournalItem.model_validate(data["journal"])

    @operation("deleteJournals")
    def delete(self, journal_id: str) -> None:
        """Permanently delete a journal entry."""
        self._client.delete(f"/api/v3/journals/{journal_id}")
