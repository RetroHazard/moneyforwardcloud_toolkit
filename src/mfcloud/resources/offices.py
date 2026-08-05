"""Office (business entity) endpoint."""

from __future__ import annotations

from mfcloud.models.office import Office
from mfcloud.resources.base import Resource, operation


class OfficesResource(Resource):
    @operation("currentOffice")
    def current(self) -> Office:
        """The office this token is authorized for, with its accounting periods."""
        return Office.model_validate(self._client.get("/api/v3/offices"))
