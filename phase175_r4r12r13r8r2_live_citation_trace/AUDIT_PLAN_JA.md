# Phase 175 R13R8R2 — 実証用出典トレース

## 目的

`π_9^5` の既存 Backward Proof Search を一度実行し、完成証明の `ProofStep`、`NarrativeCitation`、`step_citation_numbers`、Web 表示を同一実行から記録する。R3 `(5.11)` と R7 `(5.8)` に対応する典拠の内容・本文の引用位置を特定する。

## 対象

- 新規 `trace.py`: `git`, `compact`, `step_details`, `trace_model`, `trace`, `main`
- 新規 `tests/test_trace.py`: 限定構造テスト３件
- 新規 `run.ps1`: DryRun、本実行、Git 作業ツリー不変確認
- 既存本番コード・数学規則・GIVEN・ドキュメント: 変更なし

## 完了境界

このパッケージは原因を特定する監査だけを実施する。Reference の表示修正と完成証明の退行テストは R13R8 後続修正で行う。全体 pytest は Phase 175 終了時まで行わない。
