# Japanese ⇔ English Accounting Glossary

Canonical terminology for this project. All translations (spec, docs, CLI, MCP tool
descriptions) use these terms consistently. The API's JSON keys are already English;
this glossary maps the Japanese domain terms that appear in the platform UI and the
upstream spec's descriptions.

| Japanese | English | Notes |
|---|---|---|
| 事業者 | office | Business entity; the API resource is `offices`. Tokens are office-scoped. |
| 勘定科目 | account | Chart-of-accounts item (`accounts`). |
| 補助科目 | sub-account | Subdivision of an account (`sub_accounts`). |
| 部門 | department | Cost center (`departments`). |
| 税区分 | tax category | (`taxes`). Consumption-tax treatment of a line. |
| 仕訳 | journal entry | (`journals`). |
| 仕訳帳 | journal book | The ledger of journal entries. |
| 借方 / 貸方 | debit / credit | |
| 証憑 | voucher | Receipt/supporting document attached to a journal entry (`vouchers`). |
| 取引先 | trade partner | Customer/vendor (`trade_partners`). |
| 明細 | transaction | Imported bank/card line item (`transactions`). |
| 仕訳候補 | journal suggestion | Auto-suggested entry for a transaction. |
| 連携サービス | connected service | Linked bank/card/e-commerce account (`connected_accounts`). |
| 会計期間 / 会計年度 | accounting period / fiscal year | (`term_settings`). |
| 期首 / 期末 | beginning of period / end of period | |
| 開始残高 | opening balance | |
| 残高試算表 | trial balance | |
| 貸借対照表 (BS) | balance sheet (BS) | |
| 損益計算書 (PL) | profit and loss statement (PL) | |
| 推移表 | transition report | Month-over-month balance movement. |
| 決算 | closing | Year-end settlement of accounts. |
| 決算整理仕訳 | closing adjustment entry | |
| 消費税 | consumption tax | Japanese VAT. |
| 税込 / 税抜 | tax-inclusive / tax-exclusive | |
| 課税 / 非課税 / 不課税 / 免税 | taxable / tax-exempt / non-taxable / duty-free | Consumption-tax statuses. |
| 摘要 | remark | Free-text memo line on an entry (`remark` fields). |
| メモ | memo | |
| タグ | tag | |
| 品目 | item | |
| インボイス | invoice (qualified) | Japan's qualified invoice system (適格請求書). |
| 適格請求書発行事業者 | qualified invoice issuer | |
| 登録番号 | registration number | Invoice-issuer registration number. |
| 未実現 | unrealized | |
| 振替 | transfer | |
| 残高 | balance | |
