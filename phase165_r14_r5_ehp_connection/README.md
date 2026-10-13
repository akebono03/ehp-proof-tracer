# Phase 165 R14-R5 — EHP Expansion Interface Audit

## 変更対象

- 新規 `phase165_r14_r5_ehp_connection.py`
  - `adapt_registered_goal_expansion()`、`expand_registered_ehp_goal()`、`audit_ehp_connection()` の全文
- 新規 `test_phase165_r14_r5_ehp_connection.py` — 関連テスト関数全文
- 新規 `audit.py`、`run.ps1`

既存のコード、Registry、ProofStep、Web は変更しない。

## 設計

Phase 161 の `BackwardGoalExpansion` を Phase 165 の `GoalExpansion` に写像する。
既存 EHP の型付き推論規則を再利用するだけで、前提を新規作成しない。
`π₃² = ℤ{η₂}` の Goal に一致する展開がなければ `ROOT_RULE_CATALOG_MISSING` とする。
専用の group proof や `GIVEN` step を作ることは禁止する。

## テストと完了条件

`run.ps1` は新規テストと出典台帳を使った root expansion 監査だけを実施。
実行結果が新規 ProofStep 0、legacy proof なし、正確な不足条件を示すこと。
全体 pytest は実行しない。

## 次 Phase 境界

R14-R6 以降で一般的な group structure / EHP Hopf isomorphism からの導出規則と出典付きの前提を接続。
本パッケージは EHP 展開のアダプターであり、完全な数学的証明ではない。
