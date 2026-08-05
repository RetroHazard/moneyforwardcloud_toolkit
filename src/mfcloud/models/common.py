"""Shared model base and pagination metadata."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class MFModel(BaseModel):
    """Base for all API models.

    extra="allow" keeps unknown fields the API may add later instead of failing —
    the spec-lock tests, not runtime validation, police field drift.
    """

    model_config = ConfigDict(extra="allow")


class Metadata(MFModel):
    """Pagination envelope on list endpoints."""

    total_pages: int
    total_count: int
