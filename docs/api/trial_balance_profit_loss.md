# TrialBalanceProfitLoss

Trial balance (PL) retrieval API

## GET `/api/v3/reports/trial_balance_pl`

**Retrieve the profit and loss statement of the trial balance** (`getReportsTrialBalanceProfitLoss`)

Retrieves the profit and loss statement of the trial balance. Accounts and sub-accounts whose amounts are 0 for all items, as well as some financial statement items, are not returned. The trial balance columns - opening_balance(previous period balance) - debit_amount(debit amount) - credit_amount(credit amount) - closing_balance(end-of-period balance) - ratio(composition ratio) are returned as a fixed set. Also, unrealized journal entries are not included, and figures are always aggregated as the total of all departments. ratio(composition ratio) is null instead of 0 when the denominator is 0, as it cannot be calculated.

**Scopes:** `mfc/accounting/report.read`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `fiscal_year` | query | integer |  | Specifies the fiscal year. If not specified, the latest fiscal year is used. |
| `start_month` | query | integer |  | Specifies the aggregation start month of the target fiscal year. Can be combined with `fiscal_year` to specify the aggregation start month. If not specified, the start month of the fiscal year is used. |
| `end_month` | query | integer |  | Specifies the aggregation end month of the target fiscal year. Can be combined with `fiscal_year` to specify the aggregation end month. If not specified, the end month of the fiscal year is used. |
| `start_date` | query | string (date) |  | Specifies the start date of the target period. |
| `end_date` | query | string (date) |  | Specifies the end date of the target period. |
| `with_sub_accounts` | query | boolean |  | Specifies whether to retrieve the amounts of sub-accounts linked to accounts. |
| `include_tax` | query | boolean |  | Specifies whether to calculate on a tax-inclusive basis. Can only be specified when "Office Settings > Accounting Method" is 「税抜（内税）」 (tax-exclusive, internal tax). For the 「税込」 (tax-inclusive) and 「税抜（別記）」 (tax-exclusive, separately stated) accounting methods, this parameter is ignored. |
| `journal_types` | query | array of string (enum: `journal_entry`, `adjusting_entry`) |  | Specifies the type of journal entries to target. You can specify either `journal_entry` (normal journal entries) or `adjusting_entry` (closing adjustment entries), or both. If omitted, both types are targeted. |

### Responses

| Status | Body |
|---|---|
| 200 | [TBResponse](schemas.md#tbresponse) |
| 400 | [getReportsTrialBalanceBalanceSheet_400_response](schemas.md#getreportstrialbalancebalancesheet_400_response) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

