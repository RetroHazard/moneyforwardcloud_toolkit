# Vouchers

Voucher API

## POST `/api/v3/vouchers`

**Save a new voucher** (`postVouchers`)

Saves a new voucher.<br>For details, see <a href="/specs/vouchers">this documentation</a>.

**Scopes:** `mfc/accounting/voucher.write`

### Request body

Type: [PostVouchersRequest](schemas.md#postvouchersrequest)

### Responses

| Status | Body |
|---|---|
| 201 | [PostVouchersResponse](schemas.md#postvouchersresponse) |
| 400 | [postVouchers_400_response](schemas.md#postvouchers_400_response) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 415 | [ErrorResponse](schemas.md#errorresponse) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

## DELETE `/api/v3/vouchers`

**Detach a voucher** (`deleteVouchers`)

Removes the association between a journal entry and a voucher.

**Scopes:** `mfc/accounting/voucher.write`

### Request body

Type: [DeleteVouchersRequest](schemas.md#deletevouchersrequest)

### Responses

| Status | Body |
|---|---|
| 204 | — |
| 400 | [postVouchers_400_response](schemas.md#postvouchers_400_response) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 404 | [VoucherErrorResponse](schemas.md#vouchererrorresponse) |
| 415 | [ErrorResponse](schemas.md#errorresponse) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

