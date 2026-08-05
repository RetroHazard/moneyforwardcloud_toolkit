# Money Forward Cloud Accounting Toolkit — Design

**Date:** 2026-08-05
**Status:** Approved

## Goal

An English-first Python toolkit covering every endpoint of the Money Forward Cloud
Accounting API (v3), usable directly by humans and drivable by Claude via CLI for
natural-language accounting workflows. The platform and its documentation are
Japanese-only; this project provides a translated English spec and an English
developer/operator experience.

## Research Findings (verified 2026-08-05)

### API surface

- **Base URL:** `https://api-accounting.moneyforward.com` (paths under `/api/v3`)
- **Spec:** OpenAPI 3.0.3, official YAML at
  `https://developers.api-accounting.moneyforward.com/v3/openapi.yaml` (Japanese).
  MF explicitly offers this download as "input for generative AI".
- **23 operations / 17 paths / 15 resource areas:**

| Resource | Operations |
|---|---|
| Offices (事業者) | GET current office |
| Accounts (勘定科目) | GET list |
| Sub-accounts (補助科目) | GET list |
| Departments (部門) | GET list |
| Taxes (税区分) | GET list |
| Term settings (会計年度設定) | GET list |
| Journals (仕訳) | GET list, POST, GET by id, PUT, DELETE |
| Vouchers (証憑) | POST upload, DELETE |
| Trade partners (取引先) | GET list, POST |
| Connected accounts (連携サービス) | GET list |
| Transactions (明細) | GET list, POST, POST journalize |
| Reports | GET trial_balance_bs, trial_balance_pl, transition_bs, transition_pl |

### Authentication

- **OAuth 2.0 authorization-code flow only.** The MF support page explicitly
  states API-key authorization is **not** supported for the Accounting API.
- Authorize: `https://api.biz.moneyforward.com/authorize`
  Token: `https://api.biz.moneyforward.com/token`
- 13 scopes (`mfc/accounting/*.read` / `*.write`); tokens are office-scoped.
- App registration happens in MF's App Portal (requires "full admin" rights);
  yields Client ID + Client Secret and a registered redirect URI.
- **Caveat:** the user currently holds an App Portal API key (`mf_api_pro_…`).
  That scheme (JWT via `POST https://api.biz.moneyforward.com/auth/exchange`)
  works for some MF Cloud services and the official MCP server, but **not** for
  this API. An OAuth application must be registered before live use.

### Limits

- **Rate limit:** 3 requests/second per (ClientID, office ID) pair — the only
  documented limit (`/rate_limiter` doc page).
- Pagination: `page` / `per_page` query params on list endpoints.
- Errors: 4xx/5xx return a common body — an array of `{code, message}` objects.

## Architecture (Approach A: hand-written thin client)

Rationale: 23 operations is small enough to hand-write. This gives the best
English ergonomics, error messages, and Claude-facing CLI UX versus codegen
(verbose, regen churn) or a dynamic spec-driven engine (weak typing, poor
discoverability).

### Repo layout

```
moneyforwardcloud_toolkit/
├── docs/
│   ├── spec/openapi.ja.yaml       # pinned upstream Japanese spec (provenance)
│   ├── spec/openapi.en.yaml       # translated English OpenAPI — source of truth
│   ├── api/*.md                   # English reference: overview + one file per resource
│   └── setup.md                   # App Portal OAuth app registration guide
├── src/mfcloud/
│   ├── auth.py                    # OAuth code flow, token store, auto-refresh
│   ├── ratelimit.py               # 3 req/s token bucket + 429/5xx backoff
│   ├── client.py                  # httpx core: auth injection, retries, pagination
│   ├── models.py                  # Pydantic v2 models, English docstrings
│   ├── resources/                 # one module per resource area
│   └── cli/                       # Typer CLI, entry point `mfc`
├── tests/                         # pytest + respx; no live calls by default
├── CLAUDE.md                      # teaches Claude how to drive `mfc`
└── pyproject.toml                 # uv-managed, Python 3.12+
```

Dependencies: `httpx`, `pydantic` v2, `typer`, `pyyaml`. Dev: `pytest`, `respx`.

### Component responsibilities

- **auth.py** — `mfc auth login` runs a localhost callback server (redirect URI
  `http://localhost:8710/callback` by default, port configurable), opens the
  browser to MF's authorize page,
  exchanges the code, persists tokens. Client ID/Secret from env vars or config
  file. Tokens per-profile in the user config dir with restrictive permissions.
  Auto-refresh on expiry/401. `--profile` enables multiple offices; default
  profile for single-office use.
- **ratelimit.py** — client-wide token bucket at 3 req/s; exponential backoff
  with jitter on 429; retry idempotent GETs on 5xx. Always on.
- **client.py** — single httpx-based core used by all resources: base URL, auth
  header injection, rate limiting, error mapping, `page`/`per_page` pagination
  iterator (`--all-pages` support).
- **models.py / resources/** — Pydantic models and one module per resource,
  mirroring the 23 operations with English names, docstrings, and validation.
- **cli/** — `mfc <resource> <action>` covering every operation. `--json`
  output (auto-enabled when piped) for Claude; human tables otherwise.
  Destructive actions (`delete`, `update`) require `--yes`.

### English experience

- API JSON keys are already English; all toolkit docs, help, and errors are
  English.
- User data values (account names, partner names) are passed through
  untranslated — Claude reads Japanese natively and translates in conversation.
  No runtime translation table (YAGNI).
- API errors map to typed exceptions with English explanations, preserving the
  original Japanese `code`/`message`.

### Error handling

- HTTP/transport errors → retried per policy above, then raised as typed
  exceptions.
- API error bodies → `MFCloudAPIError` carrying status, code list, original
  messages, and an English summary.
- CLI exits non-zero with a one-line English explanation (plus original
  Japanese) — machine-parseable with `--json`.

### Testing

- Unit tests per resource against mocked HTTP (respx) using spec response
  examples.
- Dedicated tests for the rate limiter (timing/burst) and auth flow (fake
  authorize/token server).
- Live smoke tests exist but are gated behind an env var and never run by
  default.

## Build phases

1. **Spec** — pin Japanese YAML, produce translated `openapi.en.yaml` +
   Markdown reference docs.
2. **Core** — auth, rate limiter, client.
3. **Resources** — models + resource modules for all 23 operations.
4. **CLI** — full `mfc` surface.
5. **Polish** — CLAUDE.md, setup guide, README.

Feature branch per phase; commits at each checkpoint; squash-merge, keep
branches.

## Out of scope (for now)

- MCP server layer (can be added atop the library later; MF also offers an
  official remote MCP server which may accept the user's existing
  `mf_api_pro_…` key).
- Runtime Japanese→English translation of user data.
- Multi-office orchestration beyond named profiles.
