# Office

Office information API

## GET `/api/v3/offices`

**Retrieve office information** (`currentOffice`)

Retrieves office information and accounting periods. If multiple accounting periods exist, `accounting_periods` is returned as an array. Accounting periods are output in descending order of start date; if no accounting period exists, an error occurs.

**Scopes:** `mfc/accounting/offices.read`

### Responses

| Status | Body |
|---|---|
| 200 | [Office](schemas.md#office) |
| 400 | [ErrorResponse400](schemas.md#errorresponse400) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 409 | [ErrorResponse409](schemas.md#errorresponse409) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

