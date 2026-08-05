# Taxes

Tax category API

## GET `/api/v3/taxes`

**Retrieve tax categories** (`getTaxes`)

Retrieves tax categories.

**Scopes:** `mfc/accounting/taxes.read`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `available` | query | boolean |  |  |

### Responses

| Status | Body |
|---|---|
| 200 | [TaxResponse](schemas.md#taxresponse) |
| 400 | [ErrorResponse400](schemas.md#errorresponse400) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

