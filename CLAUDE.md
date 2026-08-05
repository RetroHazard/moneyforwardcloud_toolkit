# CLAUDE.md

English toolkit for the Money Forward Cloud Accounting API (v3). The platform is
Japanese-only; everything here (spec, docs, CLI, MCP tools) is English-first.

## Using the toolkit to manage accounting data

- **Preferred interface: the `mf-accounting` MCP server** (`.mcp.json` starts it via
  `uv run mfc-mcp`). ~20 tools; destructive ones (update/delete journal, delete
  voucher) return a preview first — show it to the user and only pass `confirm=true`
  after they agree. The English endpoint reference is available as MCP resources:
  `spec://reference` (index) and `spec://reference/{page}`.
- **Fallback: the `mfc` CLI** — `uv run mfc --help`. JSON output by default;
  destructive commands need `--yes`.
- Workflow recipes and the ja↔en accounting glossary live in
  `.claude/skills/mf-accounting/SKILL.md` and `docs/glossary.md`.
- Amounts are tax-inclusive yen integers; dates are `YYYY-MM-DD`; IDs are opaque
  strings from the list tools/commands. Data values (account names, partners) may be
  Japanese — translate them in conversation, never in stored data.
- Auth is OAuth-only; profiles map 1:1 to offices (`MFC_PROFILE` env). If calls fail
  with not_logged_in, the user must run `uv run mfc auth login` (see docs/oauth-setup.md).

## Working on the codebase

- `uv run pytest` (all mocked, no network) and `uv run ruff check` must pass.
- `spec/openapi.en.yaml` is the source of truth. The chain upstream → ja → en → code
  is enforced by tests: `tools/fetch_spec.py` (upstream drift),
  `tools/check_spec_sync.py` + spec-lock tests (ja↔en structure, 23/23 operation
  coverage, model↔schema field parity). If you change models/resources, spec-lock
  will tell you exactly what drifted.
- Translations live in `spec/translations.json`; after editing, re-inject with
  `tools/translate_spec.py inject` and regenerate docs with `tools/gen_reference.py`.
- Rate limit (3 req/s) is enforced in `src/mfcloud/http.py`; writes are never
  auto-retried — do not weaken either.
- Conventional commits (feat/fix/docs/...), no attribution lines. Feature branches,
  squash merges, branches kept.
- Live tests: `MFC_LIVE_TEST=1 uv run pytest tests/live` (needs a logged-in profile;
  read-only).
