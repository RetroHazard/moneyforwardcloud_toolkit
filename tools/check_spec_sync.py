"""Verify spec/openapi.en.yaml is structurally identical to spec/openapi.ja.yaml.

The English spec must differ from the Japanese one ONLY in description/summary/title
text. Any other difference means the translation pipeline corrupted the spec.

Usage: uv run python tools/check_spec_sync.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from fetch_spec import diff_pointers
from translate_spec import strip_text

SPEC_DIR = Path(__file__).resolve().parent.parent / "spec"


def main() -> None:
    ja = strip_text(yaml.safe_load((SPEC_DIR / "openapi.ja.yaml").read_text(encoding="utf-8")))
    en = strip_text(yaml.safe_load((SPEC_DIR / "openapi.en.yaml").read_text(encoding="utf-8")))
    drift = diff_pointers(ja, en)
    if drift:
        print(f"ja/en STRUCTURAL MISMATCH ({len(drift)} pointers):")
        for pointer in drift[:50]:
            print(f"  {pointer}")
        sys.exit(1)
    print("ja/en specs structurally identical")


if __name__ == "__main__":
    main()
