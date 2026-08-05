# TradePartners

Trade partner API

## GET `/api/v3/trade_partners`

**Retrieve trade partners** (`getTradePartners`)

Retrieves trade partners.

**Scopes:** `mfc/accounting/trade_partners.read`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `available` | query | boolean |  |  |

### Responses

| Status | Body |
|---|---|
| 200 | [TradePartnersResponse](schemas.md#tradepartnersresponse) |
| 400 | [ErrorResponse400](schemas.md#errorresponse400) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

## POST `/api/v3/trade_partners`

**Create trade partners** (`postTradePartners`)

Creates trade partners.

**Scopes:** `mfc/accounting/trade_partners.write`

### Request body

Type: [PostTradePartnersRequest](schemas.md#posttradepartnersrequest)

### Responses

| Status | Body |
|---|---|
| 201 | [TradePartnersResponse](schemas.md#tradepartnersresponse) |
| 400 | [postTradePartners_400_response](schemas.md#posttradepartners_400_response) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 415 | [ErrorResponse](schemas.md#errorresponse) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

