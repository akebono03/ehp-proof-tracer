# Phase 175 R4R12R13R8R6 — 共通引用契約監査

## 対象と前提

GitHub `akebono03/ehp-proof-tracer` の `develop` にある現行実装を確認した。対象は `phase168_r3_3_proof_narrative_model.py`、`phase168_r3_4_link_bridge.py`、`phase168_r3_12_body_binding.py`、`phase168_r3_37c_reference_projection.py`、`phase168_r3_5_model_renderer.py`、`web_group_proof.py`。関連する `unified_statement_registry.py` と既存の Toda (5.8)、(5.11) 出典テストを確認した。

前段 R13R8R5R2 の実環境監査で `(5,4)`、`(6,5)`、`(7,5)` の完成証明に登録済み FIXED_STATEMENT の本文欠落はなかった。R3、R7 の本文引用も表示済み。

## 今回の変更対象

既存ファイル、既存クラス、既存関数、既存 import：**変更しない**。

新規ファイル：

- `phase175_r4r12r13r8r6_binding_contract/audit.py`
- `phase175_r4r12r13r8r6_binding_contract/tests/test_contract.py`
- `phase175_r4r12r13r8r6_binding_contract/run.ps1`
- `phase175_r4r12r13r8r6_binding_contract/__init__.py`
- `phase175_r4r12r13r8r6_binding_contract/README.md`
- `phase175_r4r12r13r8r6_binding_contract/AUDIT_PLAN_JA.md`
- `phase175_r4r12r13r8r6_binding_contract/CODE_FULL_JA.md`

`audit.py` 内に `git`、`source_guard`、`inspect_binding`、`check_public_lines`、`inspect_live_target`、`run`、`main` をこの順序で追加した。テストには6つの回帰テストを追加した。

## 合否判定

1. citation number と ProofStep index の対応が双方向に一致する。
2. 使用済み登録 FIXED_STATEMENT には空でない本文がある。未登録の先行 DB 出典は別種として扱う。
3. 直接の GIVEN → INFERENCE を記録する。すべての子へ番号を機械的に複製することは要求しない。
4. `(5,4)` の `(5.11)` および `(5.8)` に出典見出し、数式、`[R番号]より` がある。
5. 3群の Proof Search は COMPLETE。Proof Tree と Renderer の数学的意味を改変しない。

本監査は万能な表示保証ではない。新しい型付き出典に対する射影未対応は、監査対象を拡大して確認する。

## 検証

限定 pytest：`python -B -m pytest -q -p no:cacheprovider phase175_r4r12r13r8r6_binding_contract/tests/test_contract.py`。

全体 pytest は Phase 175 終了時まで実行しない。次 R13R8R7 は今回の実環境結果に基づき、必要な場合にのみ production 変更を検討する。
