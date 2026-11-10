# Phase 174 R55R2 — 証明木と引用本文の切り分け監査

## 前提

- GitHub `akebono03/ehp-proof-tracer` の `develop` を実装前に確認した。
- 2026-11-10 に確認した HEAD: `7224260731ca5e61fffc4ee047cf31b6cc5ce6c5`。
- 引き継ぎ HEAD: `2dc8ac9faacc0630a18ecc5591c6951bf4e2f7a9`。その後に1コミット進んでいることを確認した。
- Git blob pin と未変更検査を行い、意図しない版では監査を拒否する。

## 今回変更する対象

既存コードの変更は **0件**。

新規ファイル:
- `phase174_r3_r7_r55r2_reference_tree_audit/__init__.py`
- `phase174_r3_r7_r55r2_reference_tree_audit/audit.py` の `git()`、`verify_checkout()`、`reference_snapshot()`、`ancestor_contains()`、`lines_containing()`、`inspect_public_proof()`、`report_path()`、`main()`
- `phase174_r3_r7_r55r2_reference_tree_audit/tests/test_audit.py` の4テスト
- `phase174_r3_r7_r55r2_reference_tree_audit/run.ps1`
- 本ドキュメントと README / CODE_FULL_JA / TEST_RESULTS_JA

## 監査方針

実際の Source-first Search → Screened Registry → Verified Proof Tree → ProofNarrativeModel → 共通 Renderer を読み取り専用で通す。

- Toda (5.9) 一般 GIVEN と $n=6$ の INFERENCE を区別する。
- Proposition 2.7 一般 GIVEN、型付き一般前提、$n=6$ 特殊化を別 ProofStep として検査する。
- 上側の $\Delta:\pi_{13}^{13}\to\pi_{11}^{6}$ に4つの別々の推論前提があることを検査する。
- R2、R7 の Citation に source assertion-ID、source GIVEN、statement_bodies がついているかを検査する。
- Reference 本文と証明本文の有無は検査結果として保存し、補完・推測・自動挿入は一切行わない。

## 完了条件と Phase 境界

- DryRun の Source Guard が通ること。
- 限定 pytest が通ること。
- 実際の証明木と Citation の監査 JSON が生成されること。
- R2/R7 の本文が不足していても、証明木自体が完全なら監査を成功として報告し、表示不足フラグを残すこと。
- 本工程では数学規則、既存 Renderer、文書5点、R56 全体 pytest は変更・実行しない。
