"""Extract translatable text from the Japanese OpenAPI spec / inject translations back.

The English spec (spec/openapi.en.yaml) is produced by replacing only human-language
text nodes (description, summary, title, and example strings containing Japanese) in
spec/openapi.ja.yaml. Structure, keys, and all other values are preserved byte-for-byte
at the data level, which is what tools/check_spec_sync.py verifies.

Usage:
    uv run python tools/translate_spec.py extract spec/openapi.ja.yaml strings.json
    uv run python tools/translate_spec.py inject \
        spec/openapi.ja.yaml strings.json spec/openapi.en.yaml

The strings file maps JSON-pointer paths to {"ja": ..., "en": ...}. Inject fails if any
entry is missing an "en" value.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

# Keys whose string values are human language and should be translated.
TEXT_KEYS = {"description", "summary", "title"}

JAPANESE_RE = re.compile(r"[぀-ヿ㐀-鿿！-｠]")


def contains_japanese(text: str) -> bool:
    return bool(JAPANESE_RE.search(text))


def strip_text(node):
    """Return a copy of the spec with all human-language text nodes normalized.

    Two specs that differ only in description/summary/title strings (the translated
    parts) compare equal after strip_text. Used by check_spec_sync and fetch_spec.
    """
    if isinstance(node, dict):
        return {
            key: None if key in TEXT_KEYS and isinstance(value, str) else strip_text(value)
            for key, value in node.items()
        }
    if isinstance(node, list):
        return [strip_text(value) for value in node]
    return node


def walk(node, path, out):
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}/{escape(key)}"
            if key in TEXT_KEYS and isinstance(value, str) and contains_japanese(value):
                out[child] = value
            else:
                walk(value, child, out)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            walk(value, f"{path}/{i}", out)


def escape(key) -> str:
    return str(key).replace("~", "~0").replace("/", "~1")


def unescape(token: str) -> str:
    return token.replace("~1", "/").replace("~0", "~")


def set_by_pointer(root, pointer: str, value) -> None:
    tokens = [unescape(t) for t in pointer.lstrip("/").split("/")]
    node = root
    for token in tokens[:-1]:
        node = node[int(token)] if isinstance(node, list) else node[token]
    last = tokens[-1]
    if isinstance(node, list):
        node[int(last)] = value
    else:
        node[last] = value


def cmd_extract(ja_path: str, strings_path: str) -> None:
    spec = yaml.safe_load(Path(ja_path).read_text(encoding="utf-8"))
    found: dict[str, str] = {}
    walk(spec, "", found)
    existing = {}
    if Path(strings_path).exists():
        existing = json.loads(Path(strings_path).read_text(encoding="utf-8"))
    merged = {
        pointer: {"ja": ja, "en": existing.get(pointer, {}).get("en", "")}
        for pointer, ja in found.items()
    }
    Path(strings_path).write_text(
        json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    untranslated = sum(1 for v in merged.values() if not v["en"])
    print(f"{len(merged)} translatable strings ({untranslated} untranslated)")


def cmd_inject(ja_path: str, strings_path: str, en_path: str) -> None:
    spec = yaml.safe_load(Path(ja_path).read_text(encoding="utf-8"))
    strings = json.loads(Path(strings_path).read_text(encoding="utf-8"))
    missing = [p for p, v in strings.items() if not v.get("en")]
    if missing:
        sys.exit(f"error: {len(missing)} strings missing translations, e.g. {missing[:3]}")
    for pointer, value in strings.items():
        set_by_pointer(spec, pointer, value["en"])
    Path(en_path).write_text(
        yaml.safe_dump(spec, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
    )
    print(f"wrote {en_path} ({len(strings)} strings translated)")


def main() -> None:
    match sys.argv[1:]:
        case ["extract", ja, strings]:
            cmd_extract(ja, strings)
        case ["inject", ja, strings, en]:
            cmd_inject(ja, strings, en)
        case _:
            sys.exit(__doc__)


if __name__ == "__main__":
    main()
