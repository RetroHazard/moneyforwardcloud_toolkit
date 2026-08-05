# Departments

Department API

## GET `/api/v3/departments`

**Retrieve departments** (`getDepartments`)

Retrieves departments.

**Scopes:** `mfc/accounting/departments.read`

### Responses

| Status | Body |
|---|---|
| 200 | [DepartmentResponse](schemas.md#departmentresponse) |
| 400 | [ErrorResponse400](schemas.md#errorresponse400) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

