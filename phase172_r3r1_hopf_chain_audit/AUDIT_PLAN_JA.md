# Phase 172 R3R1：Hopf 導出表示の監査計画

## 位置づけ

R2・R2R1 は `PASS_R2_PRESENTATION_ONLY`・`PASS_R2R1_CORRECTION`。R3 では Hopf 像の長い導出表示を改善する。ただし、R3R1 は **AUDIT_ONLY（監査のみ）** とし、まず現行の証明木・引用・表示上の行対応を記録する。

## GitHub 事前確認

GitHub `akebono03/ehp-proof-tracer` の `develop` で、共通 Renderer `phase168_r3_5_model_renderer.py`、Phase 171 の Hopf 推論生成 `phase171_r2i_eta_hopf_bridge/source.py`、Web Adapter、関連 `phase171_r20r13_eta_sentence_layout/tests/test_projection.py` と `phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py` を確認した。R2R1 後のローカル HEAD はユーザーログに従い `737831c95d324983cb78f7d28fc4d11d6261a3c9`。実行時にも HEAD と origin/develop を照合する。

R1 の Proof Tree における最終 Hopf 像の ProofStep は 16。出典付き前提は [R3] Chapter V, i)、[R4] Proposition 2.2、[R5] (5.3)。この番号は**確認済みベースラインの診断値**であり、監査コードは固定の Step 件数や番号を使って探索しない。

## 新規追加ファイル

- `phase172_r3r1_hopf_chain_audit/audit.py`：Git/R2 内容ガード、実際の Backward Search、Trust Boundary 検証、Hopf 像から前提閉包を収集、出典・本文・ProofStep 対応を記録する新規関数群。
- `phase172_r3r1_hopf_chain_audit/tests/test_audit.py`：5件の新規限定ユニットテスト。
- `phase172_r3r1_hopf_chain_audit/run.ps1`：Windows PowerShell からの読み取り専用 Runner。
- 同ディレクトリの `__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`。

**変更する既存ファイル・既存クラス・既存関数・既存 import：なし。**

## 検査内容と完了条件

1. `develop`、コミット済み Renderer blob、適用済み R2 パッチの内容、R2R1 source/test 内容を照合する。
2. 実際の Canonical Proof Search は `complete`、未解決 Goal は 0。Trust Boundary PASS。
3. `generic-complete-proof`、Reference 8件を維持する。
4. Hopf 像の直接前提である証明済み全射性から、対応する INFERENCE の前提閉包のみを調べる。引用関係を推論規則名や表示文字列から捏造しない。
5. 本文と数式の完全一致は **診断候補** として記録する。数式等価性や消去の正当性と混同しない。
6. 既存 tracked worktree の状態は実行前後で一致。全体 pytest は実行しない。

## R3 以降との境界

R3R1 では表示抑制、式変形、Reference 修正を行わない。実際の表示と ProofStep 対応を確認してから、短縮に使う型付き証明前提および引用を設計する。R4 の全射性重複、R5 の DB prior 表記、Phase 173 の数学的 Goal は先取りしない。
