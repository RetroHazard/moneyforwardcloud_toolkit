# Journals

Journal book API

## GET `/api/v3/journals`

**Retrieve journal entry list** (`getJournals`)

Retrieves a list of journal entries by specifying conditions such as the accounting period and journal entry date. Either start_date or end_date must be specified. Only journal entries in the accounting period that contains the specified date are returned.

**Scopes:** `mfc/accounting/journal.read`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `start_date` | query | string (date) |  | Specifies the start date of the target period. The transaction date of each journal entry is used as the basis. |
| `end_date` | query | string (date) |  | Specifies the end date of the target period. The transaction date of each journal entry is used as the basis. |
| `account_id` | query | string |  | Account ID Only journal entries that have the specified account on either the debit or credit side are returned. |
| `is_realized` | query | boolean |  | Flag specifying whether the journal entry is unrealized If not specified, all journal entries are returned. |
| `transaction_ids` | query | array of string |  | Filters by transaction ID (multiple values allowed). |
| `page` | query | integer |  | Page number |
| `per_page` | query | integer |  | Number of items per page |

### Responses

| Status | Body |
|---|---|
| 200 | [GetJournalsResponse](schemas.md#getjournalsresponse) |
| 400 | [getJournals_400_response](schemas.md#getjournals_400_response) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

## POST `/api/v3/journals`

**Create a journal entry** (`postJournals`)

Creates a journal entry.

**Scopes:** `mfc/accounting/journal.write`

### Request body

Type: [CRUDJournalRequest](schemas.md#crudjournalrequest)

### Responses

| Status | Body |
|---|---|
| 201 | [CRUDJournalResponse](schemas.md#crudjournalresponse) |
| 400 | [getJournals_400_response](schemas.md#getjournals_400_response) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 415 | [ErrorResponse](schemas.md#errorresponse) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

## GET `/api/v3/journals/{id}`

**Retrieve a journal entry** (`getJournalById`)

Returns the specific journal entry of the current office for the specified journal entry ID.

**Scopes:** `mfc/accounting/journal.read`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `id` | path | string | yes | Specify the required ID. |

### Responses

| Status | Body |
|---|---|
| 200 | [CRUDJournalResponse](schemas.md#crudjournalresponse) |
| 400 | [getJournals_400_response](schemas.md#getjournals_400_response) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

## PUT `/api/v3/journals/{id}`

**Update a journal entry** (`putJournals`)

Updates a specific journal entry of the current office using the specified journal entry ID.

**Scopes:** `mfc/accounting/journal.write`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `id` | path | string | yes | Specify the required ID. |

### Request body

Type: [CRUDJournalRequest](schemas.md#crudjournalrequest)

### Responses

| Status | Body |
|---|---|
| 200 | [CRUDJournalResponse](schemas.md#crudjournalresponse) |
| 400 | [getJournals_400_response](schemas.md#getjournals_400_response) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 415 | [ErrorResponse](schemas.md#errorresponse) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

## DELETE `/api/v3/journals/{id}`

**Delete a journal entry** (`deleteJournals`)

Deletes the specific journal entry with the specified journal entry ID within the current office. Take a backup before use if necessary.

**Scopes:** `mfc/accounting/journal.write`

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `id` | path | string | yes | Specify the required ID. |

### Responses

| Status | Body |
|---|---|
| 204 | — |
| 400 | [getJournals_400_response](schemas.md#getjournals_400_response) |
| 401 | [ErrorResponse401](schemas.md#errorresponse401) |
| 403 | [ErrorResponse403](schemas.md#errorresponse403) |
| 429 | [ErrorResponse429](schemas.md#errorresponse429) |
| 500 | [ErrorResponse500](schemas.md#errorresponse500) |

