"""Test helper: an MFClient over MockTransport that records every request."""

from __future__ import annotations

import httpx

from mfcloud.client import MFClient


class RecordingAPI:
    """Routes requests to canned JSON responses and records what was sent."""

    def __init__(self):
        self.routes: dict[tuple[str, str], object] = {}
        self.requests: list[httpx.Request] = []

    def route(self, method: str, path: str, body: object, status: int = 200) -> None:
        self.routes[(method, path)] = (status, body)

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        key = (request.method, request.url.path)
        if key not in self.routes:
            return httpx.Response(404, json={"errors": [{"code": "resource_not_found",
                                                         "message": f"no route {key}"}]})
        status, body = self.routes[key]
        if body is None:
            return httpx.Response(status)
        return httpx.Response(status, json=body)

    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]


def make_client(api: RecordingAPI) -> MFClient:
    return MFClient(transport=httpx.MockTransport(api.handler))
