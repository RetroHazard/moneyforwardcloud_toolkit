# Transactions

Transaction API

## GET `/api/v3/transactions`

**Retrieve transaction list** (`getTransactions`)

Retrieves the list of transactions collected by connected services. To narrow down by connected service, specify connected_account_id or connected_sub_account_id.

**Scopes:** `mfc/accounting/transaction.read`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `start_date` | query | string (date) | yes | Specifies the start date of the retrieval range (YYYY-MM-DD format). The difference from end_date must be within 366 days. |
| `end_date` | query | string (date) | yes | Specifies the end date of the retrieval range (YYYY-MM-DD format). The difference from start_date must be within 366 days. |
| `connected_account_id` | query | string |  | Specifies the ID of the connected service to filter by. Cannot be specified together with connected_sub_account_id. |
| `connected_sub_account_id` | query | string |  | Specifies the ID of the account to filter by. If omitted, all accounts linked to the connected_account_id are targeted. Cannot be specified together with connected_account_id. |
| `value_min` | query | integer |  | Minimum amount (yen). If specified, side is required. |
| `value_max` | query | integer |  | Maximum amount (JPY). If specified, side is required. |
| `side` | query | string (enum: `INCOME`, `EXPENSE`) |  | Filters by the income/expense type of the transaction. If value_min and value_max are omitted, the full range of the specified income/expense type is applied. Required when value_min or value_max is specified. |
| `content` | query | string |  | Filters by transaction content. The match method is specified with content_match_type. |
| `content_match_type` | query | string (enum: `exact`, `partial`, `forward`, `backward`) |  | Specifies the matching method for transaction content. Ignored if content is not specified. - exact: exact match - partial: partial match (default) - forward: prefix match - backward: suffix match |
| `journalizing_statuses` | query | array of string (enum: `excluded`, `none`, `registered`, `modified`, `new_voucher_attached`) |  | Filters by journalizing status (multiple values allowed). If omitted, all statuses are included. - excluded: excluded from journalizing - none: not yet journalized - registered: journalized - modified: the transaction was modified after journalizing - new_voucher_attached: the first voucher was attached after journalizing |
| `order` | query | string (enum: `asc`, `desc`) |  | Specifies the sort order by transaction date. If omitted, desc is applied. |
| `page` | query | integer |  | Page number |
| `per_page` | query | integer |  | Number of items per page (default: 50, minimum: 10, maximum: 1000) |

### Responses

| Status | Body |
|---|---|
| 200 | [GetTransactionsResponse](schemas.md#gettransactionsresponse) |
| 400 | [ErrorResponse400](schemas.md#errorresponse400) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

## POST `/api/v3/transactions`

**Create transactions** (`postTransactions`)

Creates transactions.

**Scopes:** `mfc/accounting/transaction.write`

### Request body

Type: [PostTransactionsRequest](schemas.md#posttransactionsrequest)

### Responses

| Status | Body |
|---|---|
| 201 | [PostTransactionsResponse](schemas.md#posttransactionsresponse) |
| 400 | [TransactionErrorResponse](schemas.md#transactionerrorresponse) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 415 | [ErrorResponse](schemas.md#errorresponse) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

## POST `/api/v3/transactions/journalize`

**Create journal entries from transactions** (`postTransactionJournalize`)

Creates a journal entry from the specified transaction.

**Scopes:** `mfc/accounting/journal.write`

### Request body

Type: [PostTransactionJournalizeRequest](schemas.md#posttransactionjournalizerequest)

### Responses

| Status | Body |
|---|---|
| 201 | [CRUDJournalResponse](schemas.md#crudjournalresponse) |
| 400 | [ErrorResponse400](schemas.md#errorresponse400) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 415 | [ErrorResponse](schemas.md#errorresponse) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

