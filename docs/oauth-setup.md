# OAuth App Registration — English Walkthrough

The Accounting API supports **only** OAuth 2.0 authorization-code flow. App Portal API
keys (`mf_api_pro_…`) do **not** work for this API. You register an OAuth application
once, then `mfc auth login` handles everything else.

## Prerequisites

- A Money Forward Cloud account with **full administrator** (全権管理者) rights on the
  target office (事業者).

## 1. Register the application

1. Open the Money Forward **App Portal** (アプリポータル): [https://app-portal.moneyforward.com/apps/](https://app-portal.moneyforward.com/apps/)
   (reachable from クラウド会計 → 設定 if the direct link changes).
2. Choose **アプリ新規作成** (Create new app).
3. Fill in:
   - **アプリ名** (App name): anything, e.g. `mfcloud-toolkit`.
   - **リダイレクトURI** (Redirect URI): `http://127.0.0.1:8730/callback`
     — must match exactly. If port 8730 is taken on your machine, pick another and set
     `redirect_port` in `%APPDATA%\mfcloud\config.toml` (or `MFC_REDIRECT_PORT`).
   - **クライアント認証方式** (Client authentication method), if shown: either
     option works — the toolkit tries HTTP Basic (`CLIENT_SECRET_BASIC`) first and
     automatically falls back to sending credentials in the request body
     (`CLIENT_SECRET_POST`).
4. Save, then copy the issued **クライアントID** (Client ID) and
   **クライアントシークレット** (Client Secret).

## 2. Scopes

`mfc auth login` requests all 13 scopes by default so every toolkit feature works:

| Scope | Grants |
|---|---|
| `mfc/accounting/offices.read` | Read office info |
| `mfc/accounting/accounts.read` | Read accounts and sub-accounts |
| `mfc/accounting/departments.read` | Read departments |
| `mfc/accounting/journal.read` | Read journal entries |
| `mfc/accounting/journal.write` | Create/update/delete journal entries |
| `mfc/accounting/voucher.write` | Upload/delete vouchers |
| `mfc/accounting/report.read` | Read reports (trial balance, transitions) |
| `mfc/accounting/taxes.read` | Read tax categories |
| `mfc/accounting/trade_partners.read` | Read trade partners |
| `mfc/accounting/trade_partners.write` | Create trade partners |
| `mfc/accounting/connected_account.read` | Read connected services |
| `mfc/accounting/transaction.read` | Read transactions |
| `mfc/accounting/transaction.write` | Create/journalize transactions |

## 3. Log in

```sh
uv run mfc auth login --client-id <CLIENT_ID>
```

- You'll be prompted for the Client Secret with **hidden input** — prefer this over
  the `--client-secret` flag, which would linger in your shell history.
- The Client ID is saved to `%APPDATA%\mfcloud\config.toml` (`~/.config/mfcloud/` on
  macOS/Linux); the secret and all tokens go to your **OS credential store** — Windows
  Credential Manager, macOS Keychain, or Linux Secret Service (GNOME Keyring/KWallet).
  Never plain files. Headless Linux has no Secret Service by default: install/run a
  keyring daemon, or log in from a desktop session. Avoid plaintext keyring backends
  (e.g. `keyrings.alt`) for accounting credentials.
- A browser opens on Money Forward's consent screen. Pick the office you want to
  authorize — **tokens are office-scoped**. The chosen office = this profile.
- Headless/broken browser? Use `mfc auth login --manual` and paste the redirect URL back.

Multiple offices: log in once per office with `--profile <name>`:

```sh
uv run mfc auth login --profile tokyo-office
uv run mfc auth status --profile tokyo-office
```

Tokens auto-refresh; you should rarely need to log in again.

## Troubleshooting

- **`invalid_redirect_uri`** — the URI registered in the App Portal doesn't exactly
  match `http://127.0.0.1:<port>/callback`.
- **`HTTP 401` / `invalid_client` right after the browser step succeeds** — the token
  exchange rejected your client credentials. The stored Client Secret is wrong or
  stale: it's cached in the OS credential store and silently reused on every login.
  Re-copy the secret from the App Portal and overwrite it with
  `mfc auth login --client-secret <SECRET>` (watch for stray whitespace when pasting).
- **403 from API calls** — the office you picked on the consent screen isn't the one
  you meant, or a needed scope was declined. Re-run `mfc auth login`.
- **`mfc auth status` says not logged in** after a successful login — you're using a
  different `--profile` / `MFC_PROFILE` than you logged in with.
