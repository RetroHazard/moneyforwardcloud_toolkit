# TransitionBalanceSheet

Transition report (BS) retrieval API

## GET `/api/v3/reports/transition_bs`

**Retrieve the balance sheet transition report** (`getReportsTransitionBalanceSheet`)

Retrieves the balance sheet of the transition report. Currently only monthly is supported. Accounts and sub-accounts whose amounts are 0 for all items, as well as some financial statement items, are not returned. Also, unrealized journal entries are not included, and figures are always aggregated as the total of all departments. The transition report columns return the values for the specified period.

**Scopes:** `mfc/accounting/report.read`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `type` | query | string (enum: `monthly`) | yes | Specifies the aggregation type of the transition report. Currently only 'monthly' is supported. - monthly: monthly aggregation |
| `fiscal_year` | query | integer |  | Specifies the fiscal year. If not specified, the latest fiscal year is used. |
| `start_month` | query | integer |  | Specifies the aggregation start month of the target fiscal year. Can be combined with `fiscal_year` to specify the aggregation start month. If not specified, the start month of the fiscal year is used. |
| `end_month` | query | integer |  | Specifies the aggregation end month of the target fiscal year. Can be combined with `fiscal_year` to specify the aggregation end month. If not specified, the end month of the fiscal year is used. |
| `with_sub_accounts` | query | boolean |  | Specifies whether to retrieve the amounts of sub-accounts linked to accounts. |
| `include_tax` | query | boolean |  | Specifies whether to calculate on a tax-inclusive basis. Can only be specified when "Office Settings > Accounting Method" is 「税抜（内税）」 (tax-exclusive, internal tax). For the 「税込」 (tax-inclusive) and 「税抜（別記）」 (tax-exclusive, separately stated) accounting methods, this parameter is ignored. |

### Responses

| Status | Body |
|---|---|
| 200 | [TransitionResponse](schemas.md#transitionresponse) |
| 400 | [TransitionErrorResponse](schemas.md#transitionerrorresponse) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

