# Money Forward Cloud Accounting Toolkit

English-first Python toolkit for the [Money Forward Cloud Accounting API (v3)](https://developers.api-accounting.moneyforward.com/) — a Japanese-only platform. Covers all 23 API operations with a typed client library, a CLI (`mfc`), and an MCP server so Claude can manage accounting data through natural language in English.

> **Status:** under construction.

## What's inside

| Layer | Purpose |
|---|---|
| `spec/` | Pinned upstream Japanese OpenAPI spec + translated English spec (source of truth) |
| `docs/api/` | Generated English API reference |
| `src/mfcloud/` | Core library: OAuth 2.0 auth, rate-limited HTTP client, typed models, all endpoints |
| `mfc` CLI | Human/scripting interface, OAuth login |
| `mfc-mcp` | MCP server — the primary Claude interface |

## API constraints honored

- **Auth:** OAuth 2.0 authorization-code flow only (API keys are not supported by this API).
- **Rate limit:** 3 requests/second per (Client ID, office) — enforced client-side.
- Writes are never auto-retried; destructive operations require explicit confirmation.

## Development

```sh
uv sync
uv run pytest
uv run ruff check
```
