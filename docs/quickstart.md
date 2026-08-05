# Quick Start

From zero to asking Claude about your books, in four steps. Works on Windows, macOS,
and Linux (desktop).

**Prerequisites:** [uv](https://docs.astral.sh/uv/getting-started/installation/) and a
Money Forward Cloud account with full-admin rights on your office.

## 1. Install

```sh
git clone https://github.com/RetroHazard/moneyforwardcloud_toolkit
cd moneyforwardcloud_toolkit
uv sync
```

Sanity check (no credentials needed): `uv run pytest` — everything should pass.

## 2. Register an OAuth app (one time, ~5 minutes)

The API only accepts OAuth 2.0 — there are no API keys.

1. Open the [Money Forward App Portal](https://app-portal.biz.moneyforward.com/) and
   choose **アプリ新規作成** (Create new app).
2. Name it anything; set the redirect URI to exactly `http://127.0.0.1:8730/callback`.
3. Copy the **Client ID** and **Client Secret** it issues.

Stuck in the Japanese UI? [docs/oauth-setup.md](oauth-setup.md) has a label-by-label
walkthrough.

## 3. Log in

```sh
uv run mfc auth login --client-id <YOUR_CLIENT_ID>
```

You'll be prompted for the Client Secret (hidden input — this keeps it out of your
shell history). A browser opens on Money Forward's consent screen; pick your office
and approve. Tokens land in your OS credential store (Windows Credential Manager /
macOS Keychain / Linux Secret Service) and refresh automatically — you won't log in
again.

> Headless Linux has no credential store by default; use a desktop session, or
> `mfc auth login --manual` on a machine that has one.

## 4. Use it

**With Claude Code** — just open this folder and ask; `.mcp.json` auto-starts the MCP
server:

> "Which bank transactions from last month are still unbooked?"
> "Book a ¥5,400 taxi expense for May 2nd, paid in cash."
> "Show me the P&L trial balance for this fiscal year."

(For Claude Desktop, add an MCP server running `uv run mfc-mcp` with this folder as
the working directory.)

**From the terminal:**

```sh
uv run mfc office get                  # confirm you're connected
uv run mfc accounts list --table       # chart of accounts
uv run mfc --help                      # everything else
```

That's it. Optional extras: multiple offices via `--profile <name>` (log in once per
office), and a live end-to-end check with `MFC_LIVE_TEST=1 uv run pytest tests/live`.
