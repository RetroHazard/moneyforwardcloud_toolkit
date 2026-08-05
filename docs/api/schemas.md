# Schemas

Component schemas referenced across the API.

## AccountResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `accounts` | array of [Account](#account) | yes |  |

## GetJournalsResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `metadata` | [Metadata](#metadata) | yes |  |
| `journals` | array of [JournalItem](#journalitem) | yes |  |

## CRUDJournalRequest

| Field | Type | Required | Description |
|---|---|---|---|
| `journal` | [CRUDJournalRequest_journal](#crudjournalrequest_journal) | yes |  |

## CRUDJournalResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `journal` | [JournalItem](#journalitem) | yes |  |

## PostVouchersRequest

| Field | Type | Required | Description |
|---|---|---|---|
| `journal_id` | string |  | ID of the journal entry to attach the voucher to Example: `JournalId` |
| `voucher_files` | array of [PostVouchersRequest_voucher_files_inner](#postvouchersrequest_voucher_files_inner) | yes | List of vouchers |

## PostVouchersResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `voucher_file_ids` | array of [PostVouchersResponse_voucher_file_ids_inner](#postvouchersresponse_voucher_file_ids_inner) | yes | List of voucher IDs |

## DeleteVouchersRequest

| Field | Type | Required | Description |
|---|---|---|---|
| `journal_id` | string | yes | ID of the journal entry to which the voucher is attached Example: `JournalId` |
| `voucher_file_id` | string | yes | ID of the voucher to detach Example: `a60cd25d-c0bc-46cf-b2af-3614e21b7fe5` |

## DepartmentResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `departments` | array of [Department](#department) | yes |  |

## TaxResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `taxes` | array of [Tax](#tax) | yes |  |

## Account

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Account ID Example: `BowMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `financial_statement_type` | string (enum: `BALANCE_SHEET`, `PROFIT_LOSS`, `COST_REPORT`, `REAL_ESTATE`, `UNKNOWN`) | yes | Financial statement category Example: `BALANCE_SHEET` |
| `name` | string | yes | Account name Example: `現金` |
| `available` | boolean | yes | Active Example: `True` |
| `tax_id` | string | yes | Tax category ID Example: `3uHWBCFlkrY_QmW0yo06Eg` |
| `search_key` | string | yes | Search key Example: `現金` |
| `sub_accounts` | array of [SubAccount](#subaccount) | yes |  |
| `account_group` | [AccountGroups](#accountgroups) | yes |  |
| `category` | string (enum: `CASH_AND_DEPOSITS`, `TRADE_RECEIVABLES`, `MARKETABLE_SECURITIES`, `INVENTORIES`, `OTHER_CURRENT_ASSETS`, `PROPERTY_PLANT_AND_EQUIPMENT`, `INTANGIBLE_ASSETS`, `INVESTMENTS_AND_OTHER_ASSETS`, `DEFERRED_ASSETS`, `OWNERS_DRAWINGS`, `SUNDRIES`, `TRADE_PAYABLES`, `OTHER_CURRENT_LIABILITIES`, `NON_CURRENT_LIABILITIES`, `EQUITY`, `OWNERS_CAPITAL`, `SALES_REVENUE`, `BEGINNING_MERCHANDISE_INVENTORY`, `COST_OF_PURCHASED_GOODS`, `ENDING_MERCHANDISE_INVENTORY`, `EXPENSES`, `REVERSALS`, `PROVISIONS`, `BEGINNING_RAW_MATERIALS`, `COST_OF_RAW_MATERIALS`, `ENDING_RAW_MATERIALS`, `LABOR_COSTS`, `OTHER_MANUFACTURING_EXPENSES`, `BEGINNING_SEMI_FINISHED_AND_WIP`, `ENDING_SEMI_FINISHED_AND_WIP`, `REAL_ESTATE_INCOME`, `REAL_ESTATE_EXPENSES`, `REAL_ESTATE_EMPLOYEE_SALARY`, `CAPITAL_STOCK`, `STOCK_SUBSCRIPTION_DEPOSITS`, `LEGAL_CAPITAL_SURPLUS`, `OTHER_CAPITAL_SURPLUS`, `LEGAL_RETAINED_EARNINGS`, `APPROPRIATED_RETAINED_EARNINGS`, `RETAINED_EARNINGS_BROUGHT_FORWARD`, `TREASURY_STOCK`, `TREASURY_STOCK_SUBSCRIPTION_DEPOSITS`, `VALUATION_AND_TRANSLATION_ADJUSTMENTS`, `SUBSCRIPTION_RIGHTS_TO_SHARES`, `NET_SALES`, `BEGINNING_INVENTORY`, `TRANSFERS_TO_OTHER_ACCOUNTS`, `ENDING_INVENTORY`, `SELLING_GENERAL_AND_ADMINISTRATIVE_EXPENSES`, `NON_OPERATING_INCOME`, `NON_OPERATING_EXPENSES`, `EXTRAORDINARY_INCOME`, `EXTRAORDINARY_LOSSES`, `CORPORATE_INCOME_TAXES_CURRENT`, `CORPORATE_INCOME_TAXES_DEFERRED`, `BEGINNING_MATERIALS`, `COST_OF_MATERIALS`, `ENDING_MATERIALS`, `MANUFACTURING_EXPENSES`, `BEGINNING_WORK_IN_PROCESS`, `ENDING_WORK_IN_PROCESS`) | yes | - "CASH_AND_DEPOSITS": Cash and deposits - "TRADE_RECEIVABLES": Trade receivables - "MARKETABLE_SECURITIES": Marketable securities - "INVENTORIES": Inventories - "OTHER_CURRENT_ASSETS": Other current assets - "PROPERTY_PLANT_AND_EQUIPMENT": Property, plant and equipment - "INTANGIBLE_ASSETS": Intangible assets - "INVESTMENTS_AND_OTHER_ASSETS": Investments and other assets - "DEFERRED_ASSETS": Deferred assets - "OWNERS_DRAWINGS": Owner's drawings - "SUNDRIES": Sundries - "TRADE_PAYABLES": Trade payables - "OTHER_CURRENT_LIABILITIES": Other current liabilities - "NON_CURRENT_LIABILITIES": Non-current liabilities - "EQUITY": Equity - "OWNERS_CAPITAL": Owner's capital - "SALES_REVENUE": Sales (revenue) amount - "BEGINNING_MERCHANDISE_INVENTORY": Beginning merchandise (finished goods) inventory - "COST_OF_PURCHASED_GOODS": Purchases during the period - "ENDING_MERCHANDISE_INVENTORY": Ending merchandise (finished goods) inventory - "EXPENSES": Expenses - "REVERSALS": Reversals, etc. - "PROVISIONS": Provisions, etc. - "BEGINNING_RAW_MATERIALS": Beginning raw materials inventory - "COST_OF_RAW_MATERIALS": Raw materials purchases - "ENDING_RAW_MATERIALS": Ending raw materials inventory - "LABOR_COSTS": Labor costs - "OTHER_MANUFACTURING_EXPENSES": Other manufacturing expenses - "BEGINNING_SEMI_FINISHED_AND_WIP": Beginning semi-finished goods and work-in-process inventory - "ENDING_SEMI_FINISHED_AND_WIP": Ending semi-finished goods and work-in-process inventory - "REAL_ESTATE_INCOME": Income amount (real estate) - "REAL_ESTATE_EXPENSES": Necessary expenses (real estate) - "REAL_ESTATE_EMPLOYEE_SALARY": Family employee salary (real estate) - "CAPITAL_STOCK": Capital stock - "STOCK_SUBSCRIPTION_DEPOSITS": New share subscription deposits - "LEGAL_CAPITAL_SURPLUS": Legal capital surplus - "OTHER_CAPITAL_SURPLUS": Other capital surplus - "LEGAL_RETAINED_EARNINGS": Legal retained earnings - "APPROPRIATED_RETAINED_EARNINGS": Appropriated reserves, etc. - "RETAINED_EARNINGS_BROUGHT_FORWARD": Retained earnings brought forward - "TREASURY_STOCK": Treasury stock - "TREASURY_STOCK_SUBSCRIPTION_DEPOSITS": Treasury stock subscription deposits - "VALUATION_AND_TRANSLATION_ADJUSTMENTS": Valuation and translation adjustments - "SUBSCRIPTION_RIGHTS_TO_SHARES": Subscription rights to shares - "NET_SALES": Net sales - "BEGINNING_INVENTORY": Beginning inventory - "TRANSFERS_TO_OTHER_ACCOUNTS": Transfers to other accounts - "ENDING_INVENTORY": Ending inventory - "SELLING_GENERAL_AND_ADMINISTRATIVE_EXPENSES": Selling, general and administrative expenses - "NON_OPERATING_INCOME": Non-operating income - "NON_OPERATING_EXPENSES": Non-operating expenses - "EXTRAORDINARY_INCOME": Extraordinary income - "EXTRAORDINARY_LOSSES": Extraordinary losses - "CORPORATE_INCOME_TAXES_CURRENT": Corporate income taxes - "CORPORATE_INCOME_TAXES_DEFERRED": Corporate income tax adjustments - "BEGINNING_MATERIALS": Beginning materials inventory - "COST_OF_MATERIALS": Materials purchases during the period - "ENDING_MATERIALS": Ending materials inventory - "MANUFACTURING_EXPENSES": Manufacturing expenses - "BEGINNING_WORK_IN_PROCESS": Beginning work-in-process inventory - "ENDING_WORK_IN_PROCESS": Ending work-in-process inventory Example: `CASH_AND_DEPOSITS` |

## Tax

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Tax category ID Example: `Sb0m10vvYk2dUdLU8aGxgQ%3D%3D` |
| `name` | string | yes | Tax category name Example: `Taxable sales 10% of total` |
| `abbreviation` | string | yes | Abbreviated name Example: `Section sales 10%` |
| `tax_rate` | number (float) | yes | Tax rate Example: `0.08` |
| `search_key` | string | yes | Search key Example: `Sales not covered` |
| `available` | boolean | yes | In use Example: `True` |

## SubAccount

| Field | Type | Required | Description |
|---|---|---|---|
| `account_id` | string | yes | Account ID Example: `BowMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `id` | string | yes | Sub-account ID Example: `Sb0m10vvYk2dUdLU8aGxgQ%3D%3D` |
| `name` | string | yes | Sub-account name Example: `小口現金` |
| `search_key` | string | yes | Search key Example: `現金` |
| `tax_id` | string | yes | Tax category ID Example: `3uHWBCFlkrY_QmW0yo06Eg` |

## SubAccountResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `sub_accounts` | array of [SubAccount](#subaccount) | yes |  |

## Office

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Office name Example: `Money Forward Inc.` |
| `code` | string | yes | Office code Example: `0000-0000` |
| `type` | string (enum: `INDIVIDUAL`, `CORPORATE`) | yes | Office type Example: `INDIVIDUAL` |
| `employee_count` | string (enum: `NOT_SELECTED`, `OWNER_ONLY`, `RANGE_1_5`, `RANGE_6_10`, `RANGE_11_30`, `RANGE_31_50`, `RANGE_51_100`, `RANGE_101_OR_MORE`) |  | Number of employees Returned only for corporate offices. - "NOT_SELECTED": not selected - "OWNER_ONLY": owner only - "RANGE_1_5": 1-5 people - "RANGE_6_10": 6-10 people - "RANGE_11_30": 11-30 people - "RANGE_31_50": 31-50 people - "RANGE_51_100": 51-100 people - "RANGE_101_OR_MORE": 101 or more people Example: `RANGE_1_5` |
| `is_real_estate` | boolean |  | Whether accounts for real estate income are available Returned only for sole proprietor offices. Example: `False` |
| `is_manufacturing` | boolean | yes | Whether manufacturing cost accounts are available Example: `False` |
| `pl_name_value_display_option` | string (enum: `SWITCH_NAME_AND_VALUE`, `SWITCH_NAME`, `SWITCH_VALUE`) |  | Name/balance display of profit and loss items (financial statements/trial balance) Returned only for corporate offices. - "SWITCH_NAME_AND_VALUE": switches the name between 「利益」 (profit) and 「損失」 (loss) depending on whether the balance is positive or negative - "SWITCH_NAME": switches the name between 「利益」 (profit) and 「損失」 (loss) depending on whether the balance is positive or negative, and always displays the balance as positive - "SWITCH_VALUE": always fixes the name to 「利益」 (profit) and switches the balance between positive and negative Example: `SWITCH_NAME_AND_VALUE` |
| `accounting_periods` | array of [AccountingPeriod](#accountingperiod) | yes | Fiscal year |

## AccountingPeriod

| Field | Type | Required | Description |
|---|---|---|---|
| `start_date` | string (date) | yes | Fiscal year start date Example: `2024-04-01` |
| `end_date` | string (date) | yes | Fiscal year end date Example: `2025-03-31` |
| `fiscal_year` | integer | yes | Fiscal year Example: `2024` |

## JournalLineDetails

| Field | Type | Required | Description |
|---|---|---|---|
| `value` | integer | yes | Amount Example: `100` |
| `tax_value` | integer |  | Consumption tax amount Example: `10` |
| `account_id` | string | yes | Account ID Example: `OwMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `account_name` | string | yes | Account name Example: `Cash` |
| `sub_account_id` | string |  | Sub-account ID Example: `OwMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `sub_account_name` | string |  | Sub-account name Example: `sub-account1` |
| `tax_long_name` | string |  | Tax category name Example: `` |
| `tax_id` | string |  | Tax category ID Example: `OwMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `tax_name` | string |  | Tax category abbreviated name Example: `` |
| `department_id` | string |  | Department ID Example: `OwMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `department_name` | string |  | Department name Example: `` |
| `trade_partner_name` | string |  | Trade partner name Example: `` |
| `trade_partner_code` | string |  | Trade partner code Example: `A0000000001` |
| `invoice_kind` | string (enum: `INVOICE_KIND_NONE`, `INVOICE_KIND_NOT_TARGET`, `INVOICE_KIND_QUALIFIED`, `INVOICE_KIND_UNQUALIFIED_80`, `INVOICE_KIND_UNQUALIFIED_50`, `INVOICE_KIND_UNQUALIFIED`) |  | Invoice category Example: `INVOICE_KIND_QUALIFIED` |

## TBResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `report_type` | [TBReportType](#tbreporttype) | yes |  |
| `start_date` | string (date) | yes | nil Example: `2022-04-01` |
| `end_date` | string (date) | yes | nil Example: `2023-03-31` |
| `created_at` | string (date-time) | yes | nil Example: `2023-07-04T20:56:26.978000+09:00` |
| `columns` | array of [TBColumn](#tbcolumn) | yes | nil |
| `rows` | array of [TBRow](#tbrow) | yes |  |

## TransitionResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `report_type` | [TransitionReportType](#transitionreporttype) | yes |  |
| `fiscal_year` | integer | yes | nil Example: `2022` |
| `start_month` | integer | yes | nil Example: `4` |
| `end_month` | integer | yes | nil Example: `3` |
| `start_date` | string (date) | yes | Start date of the aggregation period Example: `2022-04-01` |
| `end_date` | string (date) | yes | End date of the aggregation period Example: `2023-03-31` |
| `created_at` | string (date-time) | yes | nil Example: `2023-07-05T17:32:50.562000+09:00` |
| `columns` | array of [TransitionColumn](#transitioncolumn) | yes | nil |
| `rows` | array of [TransitionRow](#transitionrow) | yes |  |

## TradePartnersResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `trade_partners` | array of [TradePartnersResponse_trade_partners_inner](#tradepartnersresponse_trade_partners_inner) | yes | List of trade partners |

## PostTradePartnersRequest

| Field | Type | Required | Description |
|---|---|---|---|
| `trade_partners` | array of [PostTradePartnersRequest_trade_partners_inner](#posttradepartnersrequest_trade_partners_inner) | yes | List of trade partners to save |

## ConnectedAccountsResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `connected_accounts` | array of [ConnectedAccount](#connectedaccount) | yes |  |

## ConnectedAccount

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Connected service ID Example: `BowMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `name` | string | yes | Display name of the connected service Example: `account1` |
| `is_manual` | boolean | yes | Whether this is a connected service whose transactions are managed manually Example: `False` |
| `account_id` | string | yes | Account ID linked to the connected service Set only when `connected_sub_accounts` is empty. Example: `Sb0m10vvYk2dUdLU8aGxgQ%3D%3D` |
| `sub_account_id` | string | yes | Sub-account ID linked to the connected service Set only when `connected_sub_accounts` is empty. Example: `%2BowMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `connected_sub_accounts` | array of [ConnectedSubAccount](#connectedsubaccount) | yes | List of accounts of the connected service |

## ConnectedSubAccount

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Account ID of the connected service Example: `Sb0m10vvYk2dUdLU8aGxgQ%3D%3D` |
| `name` | string | yes | Display name of the connected service's account Example: `デモ支店1` |
| `account_id` | string | yes | Account ID linked to the bank/card account (口座) Example: `BowMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `sub_account_id` | string | yes | Sub-account ID linked to the account Example: `%2BowMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |

## PostTransactionJournalizeRequest

| Field | Type | Required | Description |
|---|---|---|---|
| `transaction_id` | string | yes | ID of the transaction to register as a journal entry Example: `BowMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `transaction_date` | string (date) |  | Transaction date If not specified, the transaction date of the source transaction is used. Example: `2025-04-01` |
| `tags` | array of string |  | Array of tags |
| `memo` | string |  | Memo Example: `This is a memo` |
| `account_id` | string | yes | Account ID Example: `OwMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `sub_account_id` | string |  | Sub-account ID Example: `Sb0m10vvYk2dUdLU8aGxgQ%3D%3D` |
| `department_id` | string |  | Department ID Example: `3uHWBCFlkrY_QmW0yo06Eg` |
| `trade_partner_code` | string |  | Trade partner code Example: `A0000000001` |
| `tax_id` | string |  | Tax category ID Example: `OwMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `invoice_kind` | string (enum: `INVOICE_KIND_NOT_TARGET`, `INVOICE_KIND_QUALIFIED`, `INVOICE_KIND_UNQUALIFIED_80`) |  | Invoice category Example: `INVOICE_KIND_QUALIFIED` |
| `remark` | string |  | Remark Example: `This is a remark` |

## Transaction

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Transaction ID Example: `BowMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `date` | string (date) | yes | Transaction date (YYYY-MM-DD format) Example: `2024-10-01` |
| `value` | integer | yes | Transaction amount (yen, positive integer) Example: `3000` |
| `side` | string (enum: `INCOME`, `EXPENSE`) | yes | Income/expense type Example: `INCOME` |
| `content` | string |  | Transaction description Example: `Supermarket purchase` |
| `memo` | string |  | Memo Example: `For lunch meeting` |
| `journalizing_status` | string (enum: `excluded`, `none`, `registered`, `modified`, `new_voucher_attached`) | yes | Journalizing status. - excluded: excluded from journalizing - none: not yet journalized - registered: journalized - modified: the transaction was changed after journalizing - new_voucher_attached: the first voucher was attached after journalizing Example: `none` |
| `connected_account_id` | string | yes | Connected service ID Example: `BowMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `connected_sub_account_id` | string | yes | Account ID. If the transaction is linked directly to a connected_account, connected_sub_account_id will be null. Example: `Sb0m10vvYk2dUdLU8aGxgQ%3D%3D` |
| `voucher_file_ids` | array of string | yes | List of IDs of the vouchers linked to this transaction |

## GetTransactionsResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `transactions` | array of [Transaction](#transaction) | yes | Array of transactions |
| `metadata` | [Metadata](#metadata) | yes |  |

## PostTransactionsRequest

| Field | Type | Required | Description |
|---|---|---|---|
| `connected_account_id` | string | yes | ID of the connected service in which to create the transactions Example: `BowMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `transactions` | array of [PostTransactionsRequest_transactions_inner](#posttransactionsrequest_transactions_inner) | yes | List of transactions |

## PostTransactionsResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `connected_account_id` | string | yes | ID of the connected service in which the transaction was created Example: `BowMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `transactions` | array of [PostTransactionsResponse_transactions_inner](#posttransactionsresponse_transactions_inner) | yes | List of transactions |

## Error

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `XMLName` | object |  |  |
| `code` | string (enum: `resource_not_found`, `resource_already_exists`, `server_busy`, `request_body_too_large`, `request_url_too_long`, `unsupported_http_verb`, `unsupported_media_type`) | yes | Example: `resource_not_found` |
| `message` | string (enum: `The specified resource does not exist.`, `The specified resource already exists.`, `The server is currently unable to receive requests. Please try again.`, `The size of the request body exceeds the maximum size permitted.`, `The length of the URL exceeds the maximum size permitted.`, `The resource doesn't support the specified HTTP verb.`, `The Content-Type of the request is not supported.`) | yes | nil Example: `The specified resource does not exist.` |

## Error400

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string (enum: `invalid_http_verb`, `invalid_resource_name`, `invalid_uri`, `missing_required_header`, `unsupported_header`, `invalid_input`, `invalid_query_parameter_value`, `missing_required_query_parameter`, `unsupported_query_parameter`, `redundant_query_parameter`, `invalid_request_body_value`, `missing_required_request_body_key`, `invalid_request_path_parameter`) | yes | nil Example: `invalid_query_parameter_value` |
| `message` | string (enum: `The HTTP verb specified was not recognized by the server.`, `The specified resource name contains invalid characters.`, `The requested URI does not represent any resource on the server.`, `A required HTTP header was not specified.`, `One of the requests inputs is not valid. Target`, `An invalid value was specified for one of the query parameters in the request URI. Target`, `An invalid value was specified for one of the path parameters in the request URI. Target`, `One of the query parameters specified in the request URI is not supported. Target`, `The page parameter must be larger than 0 (default is 1)`, `The page parameter must not exceed the total_pages`, `The per_page parameter must be within 1 and 100 (default is 10)`, `One of the HTTP headers specified in the request is not supported.`, `A required parameter was not specified for this request. Target`, `The following parameters cannot be provided simultaneously. Target`, `The specified value for one of the request body keys is not valid. Target`, `The specified value for one of the request body keys is required. Target`, `The specified value for one of the request body keys must be between 1 and 255 characters. Target`) | yes | nil Example: `The HTTP verb specified was not recognized by the server.` |

## Error401

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string (enum: `no_authentication_information`, `access_token_is_not_active_or_invalid`) | yes | nil Example: `no_authentication_information` |
| `message` | string (enum: `No authorization header.`, `Access token supplied is not active or it is invalid.`) | yes | nil Example: `No authorization header.` |

## Error403

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string (enum: `account_is_disabled`, `office_is_disabled`, `insufficient_permissions`) | yes | nil Example: `account_is_disabled` |
| `message` | string (enum: `The specified account is disabled.`, `The specified office is disabled.`, `The office being accessed does not have sufficient permissions to execute this operation.`) | yes | nil Example: `The specified account is disabled.` |

## Error409

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string (enum: `no_accounting_period_found`, `no_office_found`) | yes | nil Example: `no_accounting_period_found` |
| `message` | string (enum: `The specified office doesn't have any accounting period.`, `The specified office isn't registered to Cloud Accounting.`) | yes | nil Example: `The specified office doesn't have any accounting period.` |

## Error429

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string (enum: `too_many_requests`) | yes | Example: `too_many_requests` |
| `message` | string (enum: `Operations per second is over the account limit.`) | yes | nil Example: `Operations per second is over the account limit.` |

## Error500

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string (enum: `operation_timed_out`, `internal_error`) | yes | nil Example: `operation_timed_out` |
| `message` | string (enum: `The operation could not be completed within the permitted time.`, `The server encountered an internal error. Please retry the request.`) | yes | nil Example: `The operation could not be completed within the permitted time.` |

## JournalError

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string (enum: `invalid_query_parameter_value`, `missing_required_query_parameter`, `missing_required_request_body_key`, `invalid_request_body_value`) | yes | nil Example: `invalid_query_parameter_value` |
| `message` | string (enum: `Accounting period doesn't exist for the fiscal year.`, `Start date is after end date.`, `Given date is not matching any accounting periods.`, `Given date is outside the accounting period.`, `The parameters cannot be provided simultaneously.`, `Please specify either start_date or end_date.`, `Please specify creditor and debitor.`, `Please specify memo of 200 characters or less.`, `The given id does not exist for this office.`, `Journal cannot be moved to a different term.`, `The specified account is inactive.`) | yes | nil Example: `Accounting period doesn't exist for the fiscal year.` |

## VoucherError

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string (enum: `invalid_request_body_parameter`, `internal_error`) | yes | nil Example: `invalid_request_body_parameter` |
| `message` | string | yes | nil Example: `The specified value for one of the request body keys is not valid.` |

## TransactionError

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string (enum: `invalid_request_body_parameter`, `internal_error`) | yes | nil Example: `invalid_request_body_parameter` |
| `message` | string | yes | nil Example: `The specified value for one of the request body keys is not valid.` |

## ErrorResponse

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `errors` | array of [Error](#error) | yes | nil |

## ErrorResponse400

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `errors` | array of [Error400](#error400) | yes | nil |

## ErrorResponse401

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `errors` | array of [Error401](#error401) | yes | nil |

## ErrorResponse403

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `errors` | array of [Error403](#error403) | yes | nil |

## ErrorResponse409

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `errors` | array of [Error409](#error409) | yes | nil |

## ErrorResponse429

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `errors` | array of [Error429](#error429) | yes | nil |

## ErrorResponse500

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `errors` | array of [Error500](#error500) | yes | nil |

## JournalErrorResponse

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `errors` | array of [JournalError](#journalerror) | yes | nil |

## TrialBalanceErrorResponse

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `errors` | array of [TrialBalanceError](#trialbalanceerror) | yes | nil |

## TransitionErrorResponse

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `errors` | array of [TransitionError](#transitionerror) | yes | nil |

## TradePartnersErrorResponse

Error response of the trade partner API

| Field | Type | Required | Description |
|---|---|---|---|
| `errors` | array of [TradePartnersError](#tradepartnerserror) | yes | List of errors |

## VoucherErrorResponse

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `errors` | array of [VoucherError](#vouchererror) | yes | nil |

## TransactionErrorResponse

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `errors` | array of [TransactionError](#transactionerror) | yes | nil |

## TermSetting

| Field | Type | Required | Description |
|---|---|---|---|
| `start_date` | string (date) | yes | Fiscal year start date Example: `2024-04-01` |
| `end_date` | string (date) | yes | Fiscal year end date Example: `2025-03-31` |
| `fiscal_year` | integer | yes | Fiscal year Example: `2024` |
| `prefecture` | string | yes | Prefecture Example: `東京都` |
| `business_types` | array of string (enum: `MANUFACTURING`, `EDUCATION`, `MEDICAL_WELFARE`, `INFORMATION_COMMUNICATION`, `FOOD_SERVICE`, `TRANSPORTATION`, `WHOLESALE`, `RETAIL`, `FINANCE_INSURANCE`, `REAL_ESTATE`, `SERVICES`, `OTHER`, `CONSTRUCTION`) | yes | Business type - "MANUFACTURING": manufacturing - "EDUCATION": education - "MEDICAL_WELFARE": medical/welfare - "INFORMATION_COMMUNICATION": information and communication - "FOOD_SERVICE": food service - "TRANSPORTATION": transportation - "WHOLESALE": wholesale - "RETAIL": retail - "FINANCE_INSURANCE": finance and insurance - "REAL_ESTATE": real estate - "SERVICES": services - "OTHER": other - "CONSTRUCTION": construction |
| `tax_method` | string (enum: `FREE`, `SIMPLE`, `PROPORTIONAL_ALLOCATION`, `INDIVIDUAL_ALLOCATION`) | yes | Taxation method - "FREE": tax-exempt business (免税事業者) - "SIMPLE": simplified taxation - "PROPORTIONAL_ALLOCATION": standard taxation (lump-sum proportional allocation method) - "INDIVIDUAL_ALLOCATION": standard taxation (individual correspondence method) Example: `SIMPLE` |
| `accounting_method` | string (enum: `TAX_INCLUDED`, `TAX_EXCLUDED_SEPARATE`, `TAX_EXCLUDED_INCLUDED`) |  | Accounting method Not returned when the taxation type is a tax-exempt (免税) office. - "TAX_INCLUDED": 「税込」 (tax-inclusive) - "TAX_EXCLUDED_SEPARATE": 「税抜（別記）」 (tax-exclusive, separately stated) - "TAX_EXCLUDED_INCLUDED": 「税抜（内税）」 (tax-exclusive, internal tax) Example: `TAX_INCLUDED` |
| `sales_rounding_method` | string (enum: `ROUND_DOWN`, `ROUND_UP`, `ROUND_OFF`) | yes | Rounding method for sales Example: `ROUND_OFF` |
| `purchases_rounding_method` | string (enum: `ROUND_DOWN`, `ROUND_UP`, `ROUND_OFF`) | yes | Rounding method for purchases Example: `ROUND_OFF` |

## TermSettingsResponse

| Field | Type | Required | Description |
|---|---|---|---|
| `term_settings` | array of [TermSetting](#termsetting) | yes | List of fiscal year settings |

## Metadata

| Field | Type | Required | Description |
|---|---|---|---|
| `total_pages` | integer | yes | nil Example: `101` |
| `total_count` | integer | yes | nil Example: `101` |

## JournalItem

| Field | Type | Required | Description |
|---|---|---|---|
| `entered_by` | [EnteredBy](#enteredby) | yes |  |
| `id` | string | yes | Journal entry ID Example: `tfAQxNx%2BSnC9teuXKMjdYNpEVoee%2F%2Bn%2B97E9vQmfAupTjPMQ0eZt3lRC7IeI%2FN1L` |
| `number` | integer | yes | Journal entry number Example: `100` |
| `term_period` | integer | yes | Fiscal year Example: `2020` |
| `transaction_date` | string (date) | yes | Transaction date |
| `is_realized` | boolean | yes | Flag specifying whether the journal entry is unrealized Example: `True` |
| `journal_type` | string (enum: `journal_entry`, `adjusting_entry`) | yes | Flag specifying whether the journal entry is a closing adjustment entry Example: `journal_entry` |
| `create_time` | string (datetime) | yes | Date and time the journal entry was created Example: `2015-04-28T01:15:31Z` |
| `update_time` | string (datetime) | yes | Date and time the journal entry was updated Example: `2015-04-28T01:15:31Z` |
| `branches` | array of [JournalLine](#journalline) | yes |  |
| `tags` | array of string | yes | Array of tags |
| `memo` | string |  | Memo |
| `voucher_file_ids` | array of string | yes | Array of attached voucher IDs |
| `transaction_id` | string |  | Transaction ID linked to the journal entry. Set when the journal entry was created from a transaction. Example: `BowMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |

## CRUDJournalLine

| Field | Type | Required | Description |
|---|---|---|---|
| `remark` | string |  | Remark Example: `Sell furniture for 100 yen` |
| `creditor` | [CRUDJournalLineDetails](#crudjournallinedetails) |  |  |
| `debitor` | [CRUDJournalLineDetails](#crudjournallinedetails) |  |  |

## Department

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Department ID Example: `Sb0m10vvYk2dUdLU8aGxgQ%3D%3D` |
| `name` | string | yes | Department name Example: `Development Department` |
| `parent_id` | string | yes | Parent department ID Example: `BowMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `search_key` | string | yes | Search key Example: `code` |

## AccountGroups

- “NONE”: none - “ASSET”: assets - “LIABILITY”: liabilities - “CAPITAL”: capital (net assets) - “REVENUE”: revenue - “EXPENSE”: expenses

Type: string (enum: `NONE`, `ASSET`, `LIABILITY`, `CAPITAL`, `REVENUE`, `EXPENSE`)

## TBReportType

Type: string (enum: `trial_balance_bs`, `trial_balance_pl`)

## TBColumn

nil

Type: string (enum: `opening_balance`, `debit_amount`, `credit_amount`, `closing_balance`, `ratio`)

## TBRow

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | [RowType](#rowtype) | yes |  |
| `name` | string | yes | nil |
| `values` | array of [TBRowValue](#tbrowvalue) | yes | nil |
| `rows` | array of [TBRow](#tbrow) | yes | nil |

## TransitionReportType

Type: string (enum: `transition_bs`, `transition_pl`)

## TransitionColumn

nil

Type: string (enum: `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `1`, `2`, `3`, `settlement_balance`, `total`)

## TransitionRow

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | [RowType](#rowtype) | yes |  |
| `name` | string | yes | nil |
| `values` | array of [TransitionRowValue](#transitionrowvalue) | yes | nil |
| `rows` | array of [TransitionRow](#transitionrow) | yes | nil |

## TrialBalanceError

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string (enum: `invalid_query_parameter_value`, `missing_required_query_parameter`, `invalid_query_parameter_combination`) | yes | nil Example: `invalid_query_parameter_value` |
| `message` | string (enum: `The given months are not matching with any accounting periods.`, `The combination of date parameters combined with month and fiscal year parameters is invalid.`) | yes | nil Example: `The given months are not matching with any accounting periods.` |

## TransitionError

nil

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string (enum: `invalid_query_parameter_value`, `missing_required_query_parameter`) | yes | nil Example: `invalid_query_parameter_value` |
| `message` | string (enum: `The given months are not matching with any accounting periods.`) | yes | nil Example: `The given months are not matching with any accounting periods.` |

## TradePartnersError

Trade partner API error

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string (enum: `invalid_request_body_value`) | yes | Error code of the trade partner API Example: `invalid_request_body_value` |
| `message` | string (enum: `The specified value for one of the request body keys must be a 13-digit half-width number. Target`, `The values of corporate_number and invoice_registration_number must be the same.`, `Maximum 500 trade partners can be registered at once.`) | yes | Error message of the trade partner API Example: `Maximum 500 trade partners can be registered at once.` |

## EnteredBy

- “JOURNAL_TYPE_NONE”: none - “JOURNAL_TYPE_NORMAL”: normal journal entry - “JOURNAL_TYPE_OPENING”: opening journal entry - “JOURNAL_TYPE_HOME_DEVOTE”: journal entry created by the home-use allocation (家事按分) feature - “JOURNAL_TYPE_DEPRECIATION”: journal entry generated by depreciation - “JOURNAL_TYPE_BILLING”: journal entry created from Cloud Invoice - “JOURNAL_TYPE_PAYROLL”: journal entry created from Cloud Payroll - “JOURNAL_TYPE_IMPORT”: journal entry created by CSV import - “JOURNAL_TYPE_EXPENSE”: journal entry created from Cloud Expense - “JOURNAL_TYPE_DEBT”: journal entry created from Cloud Debt Payment - “JOURNAL_TYPE_STREAMED”: journal entry created from streamed (bookkeeping system) - “JOURNAL_TYPE_MOBILE_APP”: journal entry created from the mobile app - “JOURNAL_TYPE_ME”: journal entry created from Money Forward ME - “JOURNAL_TYPE_AI_OCR”: journal entry created by the AI-OCR feature - “JOURNAL_TYPE_E_INVOICE”: journal entry created via digital invoice - “JOURNAL_TYPE_EXTERNAL”: journal entry created via the API - “JOURNAL_TYPE_DATA_LINKAGE”: journal entry created via data linkage

Type: string (enum: `JOURNAL_TYPE_NONE`, `JOURNAL_TYPE_NORMAL`, `JOURNAL_TYPE_OPENING`, `JOURNAL_TYPE_HOME_DEVOTE`, `JOURNAL_TYPE_DEPRECIATION`, `JOURNAL_TYPE_BILLING`, `JOURNAL_TYPE_PAYROLL`, `JOURNAL_TYPE_IMPORT`, `JOURNAL_TYPE_EXPENSE`, `JOURNAL_TYPE_DEBT`, `JOURNAL_TYPE_STREAMED`, `JOURNAL_TYPE_MOBILE_APP`, `JOURNAL_TYPE_ME`, `JOURNAL_TYPE_AI_OCR`, `JOURNAL_TYPE_E_INVOICE`, `JOURNAL_TYPE_EXTERNAL`, `JOURNAL_TYPE_DATA_LINKAGE`)

## JournalLine

| Field | Type | Required | Description |
|---|---|---|---|
| `remark` | string |  | Remark Example: `Sell furniture for 100 yen` |
| `creditor` | [JournalLineDetails](#journallinedetails) |  |  |
| `debitor` | [JournalLineDetails](#journallinedetails) |  |  |

## CRUDJournalLineDetails

| Field | Type | Required | Description |
|---|---|---|---|
| `value` | integer | yes | Amount Example: `100` |
| `account_id` | string | yes | Account ID Example: `owMhLnFvzZ1y9TeF5%2B3QQ%3D%3D` |
| `tax_id` | string |  | Tax category ID Example: `3uHWBCFlkrY_QmW0yo06Eg` |
| `sub_account_id` | string |  | Sub-account ID Example: `Sb0m10vvYk2dUdLU8aGxgQ%3D%3D` |
| `department_id` | string |  | Department ID Example: `3uHWBCFlkrY_QmW0yo06Eg` |
| `trade_partner_code` | string |  | Trade partner code Example: `A0000000001` |
| `invoice_kind` | string (enum: `INVOICE_KIND_NOT_TARGET`, `INVOICE_KIND_QUALIFIED`, `INVOICE_KIND_UNQUALIFIED_80`) |  | Invoice category Example: `INVOICE_KIND_QUALIFIED` |

## RowType

nil

Type: string (enum: `assets`, `liabilities`, `net_assets`, `liabilities_net_assets`, `financial_statement_item`, `account`, `sub_account`)

## TBRowValue

nil

## TransitionRowValue

nil

## getJournals_400_response

## postVouchers_400_response

## getReportsTrialBalanceBalanceSheet_400_response

## postTradePartners_400_response

## CRUDJournalRequest_journal

| Field | Type | Required | Description |
|---|---|---|---|
| `transaction_date` | string (date) | yes | Transaction date Example: `2015-04-28` |
| `journal_type` | string (enum: `journal_entry`, `adjusting_entry`) | yes | Flag specifying whether the journal entry is a closing adjustment entry Example: `journal_entry` |
| `branches` | array of [CRUDJournalLine](#crudjournalline) | yes | A maximum of 300 lines can be created |
| `memo` | string |  | Memo Example: `Memo` |
| `tags` | array of string |  | Array of tags |

## PostVouchersRequest_voucher_files_inner

| Field | Type | Required | Description |
|---|---|---|---|
| `file_name` | string | yes | Voucher name Example: `file1` |
| `file_data` | string | yes | Base64-encoded voucher data Example: `YmFzZTY044Ko44Oz44Kz44O844OH44Kj44Oz44Kw` |

## PostVouchersResponse_voucher_file_ids_inner

| Field | Type | Required | Description |
|---|---|---|---|
| `file_name` | string | yes | Voucher name Example: `file1` |
| `file_id` | string | yes | Voucher ID Example: `a60cd25d-c0bc-46cf-b2af-3614e21b7fe5` |

## TradePartnersResponse_trade_partners_inner

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Trade partner name Example: `株式会社マネーフォワードベンチャーズ` |
| `available` | boolean | yes | Active Example: `True` |
| `code` | string | yes | Trade partner code Example: `A0000000001` |
| `invoice_registration_number` | string | yes | Qualified invoice issuer registration number Example: `1234567890231` |
| `corporate_number` | string | yes | Corporate number Example: `1234567890231` |
| `search_key` | string | yes | Trade partner search name Example: `株式会社マネーフォワードベンチャーズ` |

## PostTradePartnersRequest_trade_partners_inner

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Trade partner name Example: `株式会社マネーフォワードベンチャーズ` |
| `search_key` | string |  | Trade partner search name Example: `株式会社マネーフォワードベンチャーズ` |
| `invoice_registration_number` | string |  | Qualified invoice issuer registration number Example: `1234567890231` |
| `corporate_number` | string |  | Corporate number Example: `1234567890231` |
| `available` | boolean |  | nil Example: `True` |

## PostTransactionsRequest_transactions_inner

| Field | Type | Required | Description |
|---|---|---|---|
| `date` | string (date) | yes | Transaction date Example: `2025-04-01` |
| `value` | integer | yes | Transaction amount Example: `100` |
| `side` | string (enum: `INCOME`, `EXPENSE`) | yes | Income or expense Example: `EXPENSE` |
| `content` | string | yes | Transaction description Example: `This is the content` |
| `memo` | string |  | Transaction memo The maximum length is 200 characters. However, it may be shorter depending on the ratio of character types included. (As a guideline: 200 characters if all ASCII characters, 74 characters if all full-width characters.) Example: `This is the memo` |

## PostTransactionsResponse_transactions_inner

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Transaction ID Example: `123456` |
| `date` | string (date) | yes | Transaction date Example: `2025-04-01` |
| `value` | integer | yes | Transaction amount Example: `100` |
| `side` | string (enum: `INCOME`, `EXPENSE`) | yes | Income or expense Example: `EXPENSE` |
| `content` | string | yes | Transaction description Example: `This is the content` |
| `memo` | string |  | Transaction memo Example: `This is the memo` |

