# Phase 166 R3-Q: 定義の掲載順による選択

## 変更対象

- `phase165_r52_r16_web_citation_gate.py`：`screen_shared_proof_context()` 全体を置換（変更箇所は `DEFINITION` を除外しない条件のみ）。import の変更なし。変更後の関数全文は実行時にバックアップフォルダー内の `modified_function.py.txt` に保存。
- `phase166_r3q_definition_order_fix/test_phase166_r3q_definition_order_fix.py`：新規4テスト。import と各テスト関数全文は同ファイルに記載。
- `phase166_r3q_definition_order_fix/apply.py`：新規適用スクリプト、適用前に関数構造と置換箇所を検証。
- `phase166_r3q_definition_order_fix/run.ps1`：実行と失敗時復元。

## 変更一覧

掲載順モードで `AssertionKind.STATEMENT` と `AssertionKind.DEFINITION` の両方を位置比較する。`precedes_citing_assertion()` は未変更。既存の通常モードは変更しない。

## 限定 pytest

`python -m pytest -q phase166_r3q_definition_order_fix/test_phase166_r3q_definition_order_fix.py phase166_r3d_pi32_regression/tests/test_phase166_r3d_pi32_regression.py`

## 完了条件

先行する定義のみ使用し、同位置・後続定義は使用しない。既存の $\pi_3^2$ Web 回帰6件が通ること。

## 次工程との境界

`GeneratorImage` の位置調査、一般主張の特殊化との対応、通常 Web 経路への順序接続は対象外。全体 pytest は Phase 最後に実施。
