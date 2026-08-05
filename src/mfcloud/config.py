"""Configuration and profiles.

Non-secret settings live in <config_dir>/config.toml (client secret and tokens go to
the OS keyring — see auth.store). A *profile* names one authorized office; tokens are
office-scoped, so switching offices means switching profiles.

Resolution order: explicit argument > MFC_* environment variable > config.toml > default.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_REDIRECT_PORT = 8730


def config_dir() -> Path:
    if override := os.environ.get("MFC_CONFIG_DIR"):
        return Path(override)
    base = os.environ.get("APPDATA") or str(Path.home() / ".config")
    return Path(base) / "mfcloud"


@dataclass
class Config:
    client_id: str = ""
    redirect_port: int = DEFAULT_REDIRECT_PORT
    default_profile: str = "default"
    path: Path = field(default_factory=lambda: config_dir() / "config.toml")

    @classmethod
    def load(cls, path: Path | None = None) -> Config:
        path = path or config_dir() / "config.toml"
        data: dict = {}
        if path.exists():
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        return cls(
            client_id=os.environ.get("MFC_CLIENT_ID", data.get("client_id", "")),
            redirect_port=int(
                os.environ.get("MFC_REDIRECT_PORT")
                or data.get("redirect_port", DEFAULT_REDIRECT_PORT)
            ),
            default_profile=data.get("default_profile", "default"),
            path=path,
        )

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            f'client_id = "{self.client_id}"',
            f"redirect_port = {self.redirect_port}",
            f'default_profile = "{self.default_profile}"',
        ]
        self.path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def resolve_profile(self, explicit: str | None = None) -> str:
        return explicit or os.environ.get("MFC_PROFILE") or self.default_profile
