# Phase 165 R14-R13 — 出典本文と対角懸垂同型の監査

## 変更対象

- 新規 `phase165_r14_r13_source_review.py`:
  - `ExactnessSourceReview`（クラス全体）
  - `collect_prop42_source_reviews()`（関数全体）
  - `diagonal_suspension_requirements()`（関数全体）
  - `audit_r13()`（関数全体）
- 新規 `test_phase165_r14_r13_source_review.py`（テスト関数5件）
- 新規 `audit.py`, `run.ps1`, `README.md`

import の変更や既存 API の変更はありません。各新規 Python ファイルにコード全文を格納しています。

## 目的

R12 が特定した Proposition 4.2 の2件の出典候補の原文（アーカイブ済み TeX）を、そのまま監査レポートへ出します。文面で `exact` と判定できても、該当命題・数学的特殊化を自動確定しません。

`E:π₁¹→π₂²` の同型性には、両端の自由巡回群構造だけでなく `E(ι₁)=ι₂` と一般的な生成元移送に関する根拠が必要です。これらを未認証の前提一覧として保持します。

## 実行

`run.ps1` は追加された5件の pytest と読み取り専用監査のみ実施し、既存の全体 pytest は走らせません。

## 完了条件・次段階との境界

原文候補2件を保存し、Registry と ProofStep を変えず、出典候補を証明資格へ昇格させないこと。次工程で原文の適用条件を数学的に確認し、許される特殊化を明確にしてから初めて認証可能となります。
