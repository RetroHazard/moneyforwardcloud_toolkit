"""Minimal canned API responses matching the spec's schemas."""

SUB_ACCOUNT = {
    "account_id": "acc1", "id": "sub1", "name": "本店", "search_key": "HONTEN", "tax_id": "t1",
}

ACCOUNT = {
    "id": "acc1", "financial_statement_type": "BS", "name": "現金", "available": True,
    "tax_id": "t1", "search_key": "GENKIN", "sub_accounts": [SUB_ACCOUNT],
    "account_group": "ASSET", "category": "現金・預金",
}

OFFICE = {
    "name": "テスト株式会社", "code": "OFF1", "type": "CORPORATE", "is_manufacturing": False,
    "accounting_periods": [
        {"start_date": "2026-04-01", "end_date": "2027-03-31", "fiscal_year": 2026}
    ],
}

JOURNAL_LINE_DETAILS = {"value": 1000, "account_id": "acc1", "account_name": "現金"}

JOURNAL = {
    "entered_by": "JOURNAL_TYPE_NORMAL", "id": "j1", "number": 1, "term_period": 2026,
    "transaction_date": "2026-05-01", "is_realized": True, "journal_type": "NORMAL",
    "create_time": "2026-05-01T09:00:00+09:00", "update_time": "2026-05-01T09:00:00+09:00",
    "branches": [{"remark": "taxi", "debitor": JOURNAL_LINE_DETAILS,
                  "creditor": {**JOURNAL_LINE_DETAILS, "account_id": "acc2",
                               "account_name": "普通預金"}}],
    "tags": ["経費"], "voucher_file_ids": [],
}

DEPARTMENT = {"id": "d1", "name": "営業部", "parent_id": "", "search_key": "EIGYO"}

TAX = {"id": "t1", "name": "課税売上 10%", "abbreviation": "課売 10%",
       "tax_rate": 0.1, "search_key": "KAZEI10", "available": True}

TERM_SETTING = {
    "start_date": "2026-04-01", "end_date": "2027-03-31", "fiscal_year": 2026,
    "prefecture": "東京都", "business_types": ["SERVICE"], "tax_method": "SIMPLE",
    "sales_rounding_method": "ROUND_DOWN", "purchases_rounding_method": "ROUND_DOWN",
}

TRADE_PARTNER = {"name": "取引先A", "available": True, "code": "TP1",
                 "invoice_registration_number": "T1234567890123",
                 "corporate_number": "1234567890123", "search_key": "TORIHIKI"}

CONNECTED_ACCOUNT = {
    "id": "ca1", "name": "みずほ銀行", "is_manual": False, "account_id": "acc2",
    "sub_account_id": "sub1",
    "connected_sub_accounts": [
        {"id": "csa1", "name": "普通", "account_id": "acc2", "sub_account_id": "sub1"}
    ],
}

TRANSACTION = {
    "id": "tx1", "date": "2026-05-02", "value": 5400, "side": "expense",
    "content": "タクシー", "journalizing_status": "not_journalized",
    "connected_account_id": "ca1", "connected_sub_account_id": "csa1",
    "voucher_file_ids": [],
}

TB_RESPONSE = {
    "report_type": "trial_balance_bs", "start_date": "2026-04-01", "end_date": "2026-06-30",
    "created_at": "2026-07-01T00:00:00+09:00",
    "columns": ["opening_balance", "debit_amount", "credit_amount", "closing_balance", "ratio"],
    "rows": [{
        "type": "assets", "name": "資産", "values": [100.0, 50.0, 30.0, 120.0, None],
        "rows": [{"type": "account", "name": "現金",
                  "values": [100.0, 50.0, 30.0, 120.0, 1.0], "rows": []}],
    }],
}

TRANSITION_RESPONSE = {
    "report_type": "transition_pl", "fiscal_year": 2026, "start_month": 4, "end_month": 6,
    "start_date": "2026-04-01", "end_date": "2026-06-30",
    "created_at": "2026-07-01T00:00:00+09:00",
    "columns": ["4", "5", "6", "total"],
    "rows": [{"type": "financial_statement_item", "name": "売上高",
              "values": [100, 200, None, 300], "rows": []}],
}
