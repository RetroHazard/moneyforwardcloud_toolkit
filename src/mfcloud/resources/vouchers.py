"""Vouchers — receipt/document files attached to journal entries."""

from __future__ import annotations

import base64
from pathlib import Path

from mfcloud.models.requests import VoucherFile
from mfcloud.resources.base import Resource, operation


class VouchersResource(Resource):
    @operation("postVouchers")
    def upload(
        self, files: list[VoucherFile | dict], journal_id: str | None = None
    ) -> list[dict]:
        """Upload voucher files (optionally attaching to a journal entry).

        Returns [{"file_name": ..., "file_id": ...}] for later reference/deletion.
        """
        body = {
            "voucher_files": [
                VoucherFile.model_validate(f).model_dump(exclude_none=True) for f in files
            ],
        }
        if journal_id is not None:
            body["journal_id"] = journal_id
        data = self._client.post("/api/v3/vouchers", json=body)
        return data["voucher_file_ids"]

    def upload_path(self, path: str | Path, journal_id: str | None = None) -> list[dict]:
        """Convenience: upload a local file, base64-encoding it for the API."""
        p = Path(path)
        encoded = base64.b64encode(p.read_bytes()).decode("ascii")
        return self.upload([VoucherFile(file_name=p.name, file_data=encoded)], journal_id)

    @operation("deleteVouchers")
    def delete(self, journal_id: str, voucher_file_id: str) -> None:
        """Detach/delete a voucher file from a journal entry."""
        self._client.delete(
            "/api/v3/vouchers",
            json={"journal_id": journal_id, "voucher_file_id": voucher_file_id},
        )
