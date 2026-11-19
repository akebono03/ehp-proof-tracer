# Phase 175 R4R14R8 — 監査計画

## 対象

- 新規 `audit.py`：探索内の ProofStep と正規先行 DB ステップの属性を全件比較する。
- 新規 `tests/test_audit.py`：読み取り専用の診断と検証境界を検査する。
- 新規 `run.ps1`：DryRun と限定 pytest を実行する。

## 比較事項

`conclusion`、`premises`、`rule`、`note`、`inference_rule` の不一致を、内容を変えずに JSON に記録する。`verified_db_step()` と実際の R41 matcher の結果も記録する。出典を偽造したり、前提の証明種別を変更して成功扱いにしない。

## 境界

本番コードの変更なし。新規数学規則・新規 GIVEN はゼロ。結果により不一致の由来が分かった後、必要なら次段階で最小限の修正を検討する。全体 pytest は Phase 終了時のみ。
