# ConnectedAccounts

Connected service API

## GET `/api/v3/connected_accounts`

**Retrieve connected services** (`getConnectedAccounts`)

Retrieves connected services.

**Scopes:** `mfc/accounting/connected_account.read`

### Responses

| Status | Body |
|---|---|
| 200 | [ConnectedAccountsResponse](schemas.md#connectedaccountsresponse) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

