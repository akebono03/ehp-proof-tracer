# Phase 165 R14-R11 — Δ=0 の一般導出

## 変更対象
- 新規 `phase165_r14_r11_delta_zero.py`
  - `_matching_delta_exactness`, `_delta_zero_conclusion`, `delta_zero_from_suspension_iso_and_exactness_rule`, `expand_delta_zero_from_suspension_iso`, `audit_delta_pi32`
- 新規 `test_phase165_r14_r11_delta_zero.py`（テスト関数6件）
- 新規 `audit.py`, `run.ps1`, `README.md`

## 証明論理
EHP 完全性 `Im(Δ)=ker(E)` と懸垂写像 `E` の同型性を前提として、`Δ=0` を導出する。個別の Δ=0 文献命題を作らない。

`π₃³ → π₁¹ → π₂²` に対し、必要な `E:π₁¹→π₂²` 同型性と Proposition 4.2 の完全性を Subgoal として出す。

## 完了条件とテスト
一致する例からの Inference ProofStep 生成、異なる E / 完全列の拒否、未証明リーフを生成しないこと。実行対象は新規テスト6件のみ。全体 pytest は行わない。

## 次工程
`E:π₁¹→π₂²` の同型性について型付き出典と認証、Proposition 4.2 一般形の登録を行い、承認した前提だけを共通探索に渡す。今回の例示 `GIVEN` はテスト用であり Toda の前提を認証しない。
