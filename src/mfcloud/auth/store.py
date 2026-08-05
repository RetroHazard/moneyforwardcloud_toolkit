"""Token and client-secret storage in the OS keyring (Windows Credential Manager).

One JSON blob per profile under service "mfcloud-toolkit". Nothing secret ever touches
a plain file. The keyring backend is injectable so tests use an in-memory fake.
"""

from __future__ import annotations

import contextlib
import json
from dataclasses import asdict, dataclass, field

import keyring

SERVICE = "mfcloud-toolkit"
CLIENT_SECRET_KEY = "__client_secret__"


@dataclass
class TokenSet:
    access_token: str
    refresh_token: str
    expires_at: float
    scopes: list[str] = field(default_factory=list)

    @classmethod
    def from_token_response(cls, data: dict, now: float) -> TokenSet:
        return cls(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token", ""),
            expires_at=now + float(data.get("expires_in", 3600)),
            scopes=str(data.get("scope", "")).split(),
        )

    def expiring(self, now: float, margin: float = 60.0) -> bool:
        return now >= self.expires_at - margin


class TokenStore:
    def __init__(self, backend=None) -> None:
        self._kr = backend or keyring

    def save_tokens(self, profile: str, tokens: TokenSet) -> None:
        self._kr.set_password(SERVICE, profile, json.dumps(asdict(tokens)))

    def load_tokens(self, profile: str) -> TokenSet | None:
        raw = self._kr.get_password(SERVICE, profile)
        return TokenSet(**json.loads(raw)) if raw else None

    def delete_tokens(self, profile: str) -> None:
        with contextlib.suppress(Exception):
            self._kr.delete_password(SERVICE, profile)

    def save_client_secret(self, secret: str) -> None:
        self._kr.set_password(SERVICE, CLIENT_SECRET_KEY, secret)

    def load_client_secret(self) -> str | None:
        return self._kr.get_password(SERVICE, CLIENT_SECRET_KEY)
