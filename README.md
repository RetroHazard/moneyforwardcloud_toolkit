# Money Forward Cloud Accounting Toolkit

English-first Python toolkit for the [Money Forward Cloud Accounting API v3](https://developers.api-accounting.moneyforward.com/) — a Japanese-only platform. All **23 API operations** are covered by a typed client library, a CLI (`mfc`), and an MCP server so Claude (or any MCP client) can manage accounting data through natural language, in English.

## What's inside

| Layer | Purpose |
|---|---|
| [`spec/openapi.en.yaml`](spec/openapi.en.yaml) | Fully translated English OpenAPI spec — the project's source of truth (pinned Japanese original alongside) |
| [`docs/api/`](docs/api/README.md) | Generated English API reference (all 23 operations + schemas) |
| [`docs/glossary.md`](docs/glossary.md) | Canonical ja↔en accounting terminology |
| `src/mfcloud/` | Core library: OAuth 2.0, rate-limited client, typed Pydantic models, every endpoint |
| `mfc` | CLI — JSON-first output, `--table` for humans, `--yes` gating on deletes |
| `mfc-mcp` | MCP server (FastMCP, stdio) — the primary Claude interface |
| `.claude/skills/mf-accounting/` | Claude skill with bookkeeping workflow recipes |

## Quick start

```sh
uv sync
uv run pytest          # 100% mocked — no network, no credentials needed
```

**1. Register an OAuth app** (one-time, requires full-admin rights on the office) —
follow the English walkthrough in [docs/oauth-setup.md](docs/oauth-setup.md). The API
supports *only* OAuth 2.0 authorization-code flow; App Portal API keys do not work.

**2. Log in** (tokens go to the Windows Credential Manager, one profile per office):

```sh
uv run mfc auth login --client-id <ID> --client-secret <SECRET>
```

**3. Use it:**

```sh
uv run mfc office get
uv run mfc accounts list --available --table
uv run mfc journals list --start-date 2026-04-01 --all
uv run mfc reports trial-balance-pl --fiscal-year 2026
```

**4. Claude:** the repo's [`.mcp.json`](.mcp.json) auto-starts the `mf-accounting` MCP
server in Claude Code. For Claude Desktop, add the same command (`uv run mfc-mcp`,
working directory = this repo). Then just ask — *"book a ¥5,400 taxi expense for
May 2nd"*, *"which bank transactions from April are still unbooked?"*.

Verify against the real API once logged in: `MFC_LIVE_TEST=1 uv run pytest tests/live`.

## API constraints honored

- **Rate limit:** 3 requests/second per (Client ID, office) — enforced client-side by
  pacing, with 429 backoff honoring `Retry-After`.
- **Writes are never auto-retried** (an ambiguous timeout must not double-book a
  journal entry); GETs retry on 5xx/network errors.
- **Destructive operations** (journal update/delete, voucher delete) require `--yes`
  in the CLI and a preview→`confirm=true` round-trip in MCP.
- Tokens are office-scoped → profiles map 1:1 to offices.

## Staying in sync with upstream

The spec chain **upstream → ja → en → code** is machine-checked:

```sh
uv run python tools/fetch_spec.py       # structural diff vs pinned Japanese spec
uv run python tools/check_spec_sync.py  # ja/en structural identity
uv run pytest tests/spec_lock           # 23/23 op coverage + model field parity
```

On upstream drift: `fetch_spec.py --update`, translate the changed strings in
`spec/translations.json`, re-inject (`tools/translate_spec.py inject`), regenerate
docs (`tools/gen_reference.py`) — the tests confirm nothing was missed.

## Note: Money Forward's official remote MCP server

MF ships a hosted MCP server (beta) that also covers Cloud Accounting — zero install,
but Japanese-only, unversioned tool surface, and no local safety gating. This toolkit
exists for the English-first experience, verifiable 23/23 coverage, and deterministic
destructive-op confirmation; the official server can be a complementary fallback.
