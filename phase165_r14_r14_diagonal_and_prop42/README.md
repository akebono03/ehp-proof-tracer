# Phase 165 R14-R14 — 対角懸垂と Proposition 4.2

## 変更対象
- 新規 `phase165_r14_r14_diagonal_and_prop42.py`：`GeneratorSuspension`、`diagonal_suspension_subgoals()`、`diagonal_suspension_isomorphism_rule()`、`expand_diagonal_suspension()`、`review_prop42_scope()`、`audit_r14()` とすべての補助関数
- 新規 `test_phase165_r14_r14_diagonal_and_prop42.py`：6テストの完全な実装
- 新規 `audit.py`、`run.ps1`、`README.md`

既存コードは編集しない。

## 実装した推論
任意の n>=1 で、`π_n^n=Z{ι_n}`、`π_(n+1)^(n+1)=Z{ι_(n+1)}`、`Eι_n=ι_(n+1)` の三前提が認証されている場合に限り、E が同型であることを導く。`GeneratorSuspension` は未認証の主張型で、ProofStep を生成しない。

## 出典境界
Proposition 4.2 の2候補の原文を保存するが、どちらが完全性の一般命題に対応するかは、原文の確認が済むまで決定しない。報告は `phase165_r14_r14_output/report.md` に保存する。

## 完了条件とテスト
6件の対象 pytest が成功すること。異なる生成元・非対角写像を拒否すること。テスト用 GIVEN は実文献の認証ではないこと。既存 Registry を変更せず、Toda の ProofStep を作らないこと。

## 次の境界
原文の意味と適用範囲の確定後、Proposition 4.2 の一般命題を型付きで固定し、登録済み認証前提を共通探索へ渡す。全体 pytest は Phase 165 の最後。
