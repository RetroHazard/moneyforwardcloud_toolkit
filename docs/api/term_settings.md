# TermSettings

Fiscal year settings API

## GET `/api/v3/term_settings`

**Retrieve fiscal year settings** (`getTermSettings`)

Retrieves all fiscal year settings. Fiscal years are sorted in descending order by start date.

**Scopes:** `mfc/accounting/offices.read`

### Responses

| Status | Body |
|---|---|
| 200 | [TermSettingsResponse](schemas.md#termsettingsresponse) |
| 400 | [ErrorResponse400](schemas.md#errorresponse400) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 409 | [ErrorResponse409](schemas.md#errorresponse409) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

