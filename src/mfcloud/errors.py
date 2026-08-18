"""Typed exceptions for Money Forward Cloud Accounting API failures.

The API returns 4xx/5xx bodies shaped {"errors": [{"code": ..., "message": ...}]}.
Messages are already English upstream; exceptions preserve them verbatim.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import httpx


@dataclass
class APIErrorDetail:
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


@dataclass
class MFCloudError(Exception):
    """Base for all API errors. Carries HTTP status and the API's error details."""

    status: int
    details: list[APIErrorDetail] = field(default_factory=list)

    def __str__(self) -> str:
        summary = "; ".join(str(d) for d in self.details) or "no error details in response"
        return f"HTTP {self.status} from MF Cloud Accounting API — {summary}"


class MFCValidationError(MFCloudError):
    """400/409/422: the request was malformed or violates a business rule."""


class MFCAuthError(MFCloudError):
    """401: access token missing, expired, or revoked."""


class MFCPermissionError(MFCloudError):
    """403: the granted OAuth scopes don't permit this operation."""


class MFCNotFoundError(MFCloudError):
    """404: the resource does not exist (or belongs to another office)."""


class MFCRateLimitError(MFCloudError):
    """429: exceeded 3 requests/second per (client, office) — after client-side retries."""


class MFCServerError(MFCloudError):
    """5xx: Money Forward server-side failure."""


_STATUS_MAP: dict[int, type[MFCloudError]] = {
    400: MFCValidationError,
    401: MFCAuthError,
    403: MFCPermissionError,
    404: MFCNotFoundError,
    409: MFCValidationError,
    422: MFCValidationError,
    429: MFCRateLimitError,
}


def parse_error_details(response: httpx.Response) -> list[APIErrorDetail]:
    try:
        body = response.json()
        return [
            APIErrorDetail(code=str(e.get("code", "unknown")), message=str(e.get("message", "")))
            for e in body.get("errors", [])
        ]
    except Exception:
        return []


def parse_oauth_error_details(response: httpx.Response) -> list[APIErrorDetail]:
    """Parse an RFC 6749 token-endpoint error body: {"error", "error_description"}."""
    try:
        body = response.json()
        if not isinstance(body, dict) or "error" not in body:
            return []
        return [
            APIErrorDetail(
                code=str(body["error"]),
                message=str(body.get("error_description", "")),
            )
        ]
    except Exception:
        return []


def raise_for_status(response: httpx.Response) -> None:
    """Map an error response to a typed exception; no-op for 2xx/3xx."""
    if response.status_code < 400:
        return
    cls = _STATUS_MAP.get(response.status_code)
    if cls is None:
        cls = MFCServerError if response.status_code >= 500 else MFCValidationError
    raise cls(status=response.status_code, details=parse_error_details(response))
