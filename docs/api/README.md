# Money Forward Cloud Accounting API — English Reference

Translated from the official Japanese OpenAPI spec (version V3).
Base URL: `https://api-accounting.moneyforward.com`. All paths below are relative to it.

Authentication: OAuth 2.0 authorization-code flow; pass the access token as a
`Authorization: Bearer <token>` header. Rate limit: 3 requests/second per
(Client ID, office) pair; 429 on excess.

## Resources

| Page | Operations |
|---|---|
| [Accounts](accounts.md) | `GET /api/v3/accounts` |
| [ConnectedAccounts](connected_accounts.md) | `GET /api/v3/connected_accounts` |
| [Departments](departments.md) | `GET /api/v3/departments` |
| [Journals](journals.md) | `GET /api/v3/journals`, `POST /api/v3/journals`, `GET /api/v3/journals/{id}`, `PUT /api/v3/journals/{id}`, `DELETE /api/v3/journals/{id}` |
| [Office](office.md) | `GET /api/v3/offices` |
| [SubAccounts](sub_accounts.md) | `GET /api/v3/sub_accounts` |
| [Taxes](taxes.md) | `GET /api/v3/taxes` |
| [TermSettings](term_settings.md) | `GET /api/v3/term_settings` |
| [TradePartners](trade_partners.md) | `GET /api/v3/trade_partners`, `POST /api/v3/trade_partners` |
| [Transactions](transactions.md) | `GET /api/v3/transactions`, `POST /api/v3/transactions`, `POST /api/v3/transactions/journalize` |
| [TransitionBalanceSheet](transition_balance_sheet.md) | `GET /api/v3/reports/transition_bs` |
| [TransitionProfitLoss](transition_profit_loss.md) | `GET /api/v3/reports/transition_pl` |
| [TrialBalanceBalanceSheet](trial_balance_balance_sheet.md) | `GET /api/v3/reports/trial_balance_bs` |
| [TrialBalanceProfitLoss](trial_balance_profit_loss.md) | `GET /api/v3/reports/trial_balance_pl` |
| [Vouchers](vouchers.md) | `POST /api/v3/vouchers`, `DELETE /api/v3/vouchers` |
| [Schemas](schemas.md) | All component schemas |

