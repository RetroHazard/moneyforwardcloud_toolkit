"""Fetch the upstream Japanese OpenAPI spec and detect structural drift.

Downloads the latest spec and compares its *structure* (paths, operations, parameters,
schemas — everything except description/summary/title text) against the pinned
spec/openapi.ja.yaml. Exits 0 when unchanged, 1 on drift (listing changed pointers),
2 on download failure.

Usage:
    uv run python tools/fetch_spec.py            # check only
    uv run python tools/fetch_spec.py --update   # also overwrite spec/openapi.ja.yaml
"""

from __future__ import annotations

import sys
from pathlib import Path

import httpx
import yaml

from translate_spec import strip_text

UPSTREAM_URL = "https://developers.api-accounting.moneyforward.com/v3/openapi.yaml"
PINNED = Path(__file__).resolve().parent.parent / "spec" / "openapi.ja.yaml"


def diff_pointers(old, new, path="", out=None) -> list[str]:
    if out is None:
        out = []
    if type(old) is not type(new):
        out.append(path or "/")
    elif isinstance(old, dict):
        for key in old.keys() | new.keys():
            if key not in old or key not in new:
                out.append(f"{path}/{key}")
            else:
                diff_pointers(old[key], new[key], f"{path}/{key}", out)
    elif isinstance(old, list):
        if len(old) != len(new):
            out.append(f"{path} (length {len(old)} -> {len(new)})")
        else:
            for i, (a, b) in enumerate(zip(old, new, strict=True)):
                diff_pointers(a, b, f"{path}/{i}", out)
    elif old != new:
        out.append(path or "/")
    return out


def main() -> None:
    try:
        response = httpx.get(UPSTREAM_URL, timeout=30, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        sys.exit(f"download failed: {exc}")
    upstream_text = response.text
    pinned = strip_text(yaml.safe_load(PINNED.read_text(encoding="utf-8")))
    upstream = strip_text(yaml.safe_load(upstream_text))
    drift = diff_pointers(pinned, upstream)
    if "--update" in sys.argv:
        PINNED.write_text(upstream_text, encoding="utf-8")
        print(f"updated {PINNED}")
    if drift:
        print(f"STRUCTURAL DRIFT ({len(drift)} pointers):")
        for pointer in drift[:50]:
            print(f"  {pointer}")
        if len(drift) > 50:
            print(f"  ... and {len(drift) - 50} more")
        print("Re-run translation for changed nodes, then regenerate docs.")
        sys.exit(1)
    print("no structural drift")


if __name__ == "__main__":
    main()
