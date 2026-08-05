---
name: mf-accounting
description: Manage Money Forward Cloud Accounting data in English via the mf-accounting MCP tools (or mfc CLI) — booking journal entries, journalizing bank transactions, month-end reviews, voucher handling. Use whenever the user asks about their MF Cloud accounting data, journal entries, trial balances, or bookkeeping tasks.
---

# Money Forward Cloud Accounting workflows

Interface: `mf-accounting` MCP tools (fallback: `uv run mfc ...` CLI, JSON output).
Reference: MCP resources `spec://reference/{page}`; glossary in `docs/glossary.md`.

## Ground rules

- Amounts: tax-inclusive yen integers. Dates: `YYYY-MM-DD`. IDs: opaque strings —
  always resolve via list tools first, never invent them.
- Master data (accounts, taxes, departments, partners) is small: fetch once per
  conversation and reuse. Match user-named accounts against `name` and `search_key`
  (values may be Japanese — 現金 = cash, 普通預金 = ordinary deposit, etc.).
- Destructive tools return `{"status": "confirmation_required", ...}` first. Present
  the preview to the user; call again with `confirm=true` only after explicit consent.
- On `not_logged_in` errors: user runs `uv run mfc auth login` (docs/oauth-setup.md).

## Recipe: book an expense journal entry

1. `list_accounts(available=true)` → find debit account (expense) and credit account
   (cash/bank). Note their `id` and appropriate `tax_id` via `list_taxes(available=true)`.
2. Build one branch with balancing sides (values equal):
   `create_journal(journal={"transaction_date": ..., "journal_type": "NORMAL",
   "branches": [{"remark": ..., "debitor": {"value": N, "account_id": ..., "tax_id": ...},
   "creditor": {"value": N, "account_id": ...}}]})`
3. Echo the returned entry (id, number, lines) back to the user in English.

## Recipe: journalize unbooked bank transactions

1. `list_transactions(start_date=..., end_date=...,
   journalizing_statuses=["not_journalized"], all_pages=true)`.
2. For each transaction, propose an account/tax from its `content` (e.g. タクシー →
   travel expense). Group similar lines and confirm the mapping with the user once.
3. Per approved line: `journalize_transaction(request={"transaction_id": ...,
   "account_id": ..., "tax_id": ...})`. The rate limiter paces calls automatically —
   just loop.

## Recipe: month-end review

1. `get_report(report_type="trial_balance_pl", fiscal_year=Y, start_month=M, end_month=M)`
   and the `_bs` variant. Rows nest group → item → account; values align with `columns`.
2. Flag anomalies: negative balances on asset accounts, unusually large ratios,
   accounts with activity but no prior history.
3. Cross-check unbooked items: `list_transactions(..., journalizing_statuses=["not_journalized"])`.
4. Summarize in English with yen amounts formatted (e.g. ¥1,234,567).

## Recipe: attach a receipt to an entry

1. Find the entry: `list_journals(start_date=..., end_date=...)` or `get_journal(...)`.
2. `upload_voucher(file_name="receipt.pdf", file_path="C:/...", journal_id=...)`
   (local path preferred; base64 for in-memory data).

## Vocabulary quick map

journal entry=仕訳 · account=勘定科目 · sub-account=補助科目 · department=部門 ·
tax category=税区分 · trade partner=取引先 · voucher=証憑 · transaction=明細 ·
debit=借方 · credit=貸方 · trial balance=残高試算表 · remark=摘要
