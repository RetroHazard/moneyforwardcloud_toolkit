# SubAccounts

Sub-account API

## GET `/api/v3/sub_accounts`

**Retrieve sub-accounts** (`getSubAccounts`)

Retrieves sub-accounts.

**Scopes:** `mfc/accounting/accounts.read`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `account_id` | query | string |  | Account ID |

### Responses

| Status | Body |
|---|---|
| 200 | [SubAccountResponse](schemas.md#subaccountresponse) |
| 400 | [ErrorResponse400](schemas.md#errorresponse400) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

