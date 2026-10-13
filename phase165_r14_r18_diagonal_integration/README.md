# Phase 165 R14-R18 — 基本事実と対角懸垂同型の ProofStep 接続

## 変更対象と追加位置

プロジェクト直下に `phase165_r14_r18_diagonal_integration.py` を新規追加する。
同ファイルに `DiagonalEvidenceMissing` クラス、`derive_diagonal_iso_from_certified_groups()`、`audit_r18()` を全文収録。
関連テスト6関数は `test_phase165_r14_r18_diagonal_integration.py` に全文収録。
監査用 `audit.py`、PowerShell 実行用 `run.ps1` を新規追加。既存ソース・APIは変更しない。

## 今回の実装

R17 の根拠付き `E(ι_n)=ι_(n+1)` を、既存 `InferenceRule` を使った懸垂同型導出に接続する。
**2件の群構造の ProofStep を呼び出し側が既に認証済みとして持っている場合**だけ、`TodaSuspensionIsomorphismStatement` の ProofStep を導出する。

テストの `ProofRule.GIVEN` は明示的な fixture。Toda 文献の認証ではない。
Registry や文献の自動昇格をしない。Proposition 4.2 の2候補原文は report.md に保存するが、完全性の適用条件を未確認のまま認証しない。

## 完了条件と次の境界

追加の対象 pytest 6関数が通り、異なる次数、欠けた群構造、異なる生成元を偽って導出できないこと。全体 pytest は実行しない。

次の工程は `(5.1)` の対角群の独立した認証済み ProofStep を利用可能にすること、および Proposition 4.2 の一般完全性命題の出典・適用条件を具体的に確定すること。実際の `π₃²` の証明は R18 では完成しない。
