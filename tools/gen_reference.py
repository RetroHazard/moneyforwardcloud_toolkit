"""Generate the English Markdown API reference from spec/openapi.en.yaml.

Produces docs/api/README.md (overview + index), one file per tag with its operations,
and docs/api/schemas.md with all component schemas. Output is committed so the
reference is readable with zero tooling (and servable as MCP resources).

Usage: uv run python tools/gen_reference.py
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec" / "openapi.en.yaml"
OUT = ROOT / "docs" / "api"

METHOD_ORDER = {"get": 0, "post": 1, "put": 2, "delete": 3}


def tag_filename(tag: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", tag).lower() + ".md"


def anchor(name: str) -> str:
    return name.lower().replace(" ", "-")


def schema_ref_name(ref: str) -> str:
    return ref.rsplit("/", 1)[-1]


def type_str(schema: dict, from_schemas_file: bool = False) -> str:
    """Human-readable type for a schema node, linking $refs to schemas.md."""
    if not isinstance(schema, dict):
        return "?"
    if "$ref" in schema:
        name = schema_ref_name(schema["$ref"])
        target = f"#{anchor(name)}" if from_schemas_file else f"schemas.md#{anchor(name)}"
        return f"[{name}]({target})"
    stype = schema.get("type", "object")
    if stype == "array":
        return f"array of {type_str(schema.get('items', {}), from_schemas_file)}"
    if "enum" in schema:
        values = ", ".join(f"`{v}`" for v in schema["enum"])
        return f"{stype} (enum: {values})"
    if schema.get("format"):
        return f"{stype} ({schema['format']})"
    return stype


def clean(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(str(text).replace("<br />", " ").replace("<br/>", " ").split())


def properties_table(schema: dict, from_schemas_file: bool = False) -> list[str]:
    """Render an object schema's properties as a Markdown table."""
    lines = []
    required = set(schema.get("required", []))
    props = schema.get("properties", {})
    if not props:
        return lines
    lines.append("| Field | Type | Required | Description |")
    lines.append("|---|---|---|---|")
    for name, prop in props.items():
        req = "yes" if name in required else ""
        desc = clean(prop.get("description")) if isinstance(prop, dict) else ""
        example = prop.get("example") if isinstance(prop, dict) else None
        if example is not None and not isinstance(example, (dict, list)):
            desc = f"{desc} Example: `{example}`".strip()
        lines.append(f"| `{name}` | {type_str(prop, from_schemas_file)} | {req} | {desc} |")
    return lines


def render_operation(path: str, method: str, op: dict, components: dict) -> list[str]:
    lines = [f"## {method.upper()} `{path}`", ""]
    if op.get("summary"):
        lines += [f"**{clean(op['summary'])}** (`{op['operationId']}`)", ""]
    if op.get("description"):
        lines += [clean(op["description"]), ""]
    scopes = [s for sec in op.get("security", []) for v in sec.values() for s in v]
    if scopes:
        lines += ["**Scopes:** " + ", ".join(f"`{s}`" for s in scopes), ""]

    params = []
    for p in op.get("parameters", []):
        if "$ref" in p:
            p = components["parameters"][p["$ref"].rsplit("/", 1)[-1]]
        params.append(p)
    if params:
        lines += ["### Parameters", "", "| Name | In | Type | Required | Description |",
                  "|---|---|---|---|---|"]
        for p in params:
            desc = clean(p.get("description"))
            if desc == "nil":
                desc = ""
            required = "yes" if p.get("required") else ""
            lines.append(
                f"| `{p['name']}` | {p['in']} | {type_str(p.get('schema', {}))} "
                f"| {required} | {desc} |"
            )
        lines.append("")

    body = op.get("requestBody")
    if body:
        schema = body["content"]["application/json"]["schema"]
        lines += ["### Request body", "", f"Type: {type_str(schema)}", ""]

    lines += ["### Responses", "", "| Status | Body |", "|---|---|"]
    for status, resp in op.get("responses", {}).items():
        content = resp.get("content", {})
        if content:
            schema = next(iter(content.values())).get("schema", {})
            body_type = type_str(schema)
        else:
            body_type = "—"
        lines.append(f"| {status} | {body_type} |")
    lines.append("")
    return lines


def main() -> None:
    spec = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    components = spec["components"]
    tag_descriptions = {t["name"]: t.get("description", "") for t in spec.get("tags", [])}

    # Group operations by tag.
    by_tag: dict[str, list[tuple[str, str, dict]]] = {}
    op_count = 0
    for path, methods in spec["paths"].items():
        for method, op in methods.items():
            if method not in METHOD_ORDER:
                continue
            op_count += 1
            for tag in op.get("tags", ["Untagged"]):
                by_tag.setdefault(tag, []).append((path, method, op))

    # Per-tag pages.
    for tag, ops in by_tag.items():
        ops.sort(key=lambda x: (x[0], METHOD_ORDER[x[1]]))
        lines = [f"# {tag}", ""]
        if tag_descriptions.get(tag):
            lines += [clean(tag_descriptions[tag]), ""]
        for path, method, op in ops:
            lines += render_operation(path, method, op, components)
        (OUT / tag_filename(tag)).write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Schemas page.
    lines = ["# Schemas", "", "Component schemas referenced across the API.", ""]
    for name, schema in components["schemas"].items():
        lines += [f"## {name}", ""]
        if schema.get("description"):
            lines += [clean(schema["description"]), ""]
        if schema.get("enum"):
            lines += [f"Type: {type_str(schema, from_schemas_file=True)}", ""]
        table = properties_table(schema, from_schemas_file=True)
        if table:
            lines += table + [""]
        elif schema.get("type") == "array":
            lines += [f"Type: {type_str(schema, from_schemas_file=True)}", ""]
    (OUT / "schemas.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Index / overview.
    info = spec["info"]
    lines = [f"# {clean(info.get('title'))} — English Reference", ""]
    lines += [
        f"Translated from the official Japanese OpenAPI spec (version {info.get('version')}).",
        f"Base URL: `{spec['servers'][0]['url']}`. All paths below are relative to it.",
        "",
        "Authentication: OAuth 2.0 authorization-code flow; pass the access token as a",
        "`Authorization: Bearer <token>` header. Rate limit: 3 requests/second per",
        "(Client ID, office) pair; 429 on excess.",
        "",
        "## Resources",
        "",
        "| Page | Operations |",
        "|---|---|",
    ]
    for tag in sorted(by_tag):
        ops = ", ".join(f"`{m.upper()} {p}`" for p, m, _ in by_tag[tag])
        lines.append(f"| [{tag}]({tag_filename(tag)}) | {ops} |")
    lines += ["| [Schemas](schemas.md) | All component schemas |", ""]
    (OUT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"generated {len(by_tag)} tag pages + schemas.md + README.md ({op_count} operations)")


if __name__ == "__main__":
    main()
