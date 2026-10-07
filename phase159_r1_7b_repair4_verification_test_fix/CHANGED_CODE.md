# Phase 159-R1-7b repair4

## 変更対象

Production code の変更はありません。

変更するテスト:
- `tests/test_phase157_r20_repair37_short_exact_after_map_support.py`
- `tests/test_phase159_r1_7b_exact_sequence_display_order.py`

## 修正内容

- `は全射である.` / `は単射である.` という stale expectation を、
  現行 public Narrative の `は全射.` / `は単射.` に更新。
- exact sequence の空白配置を固定文字列で比較せず、
  `\[ ... \]` display math block を抽出して空白正規化後に比較。
- pytest より先に pi6_3 / pi11_4 の Narrative を必ず出力。

## Phase 境界

repair4 は test / verification repair のみです。
production behavior は repair3 から変更しません。
full pytest は実行しません。
