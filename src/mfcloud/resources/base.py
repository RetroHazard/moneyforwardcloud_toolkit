"""Resource base class and the operation registry backing spec-lock tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mfcloud.client import MFClient


def operation(operation_id: str):
    """Tag a resource method with the OpenAPI operationId it implements."""

    def decorate(func):
        func.__operation_id__ = operation_id
        return func

    return decorate


class Resource:
    def __init__(self, client: MFClient) -> None:
        self._client = client
