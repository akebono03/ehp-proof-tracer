# Phase 164 R3 — 変更対象一覧

## 新規追加（既存コード変更なし）

1. `phase164_r3_registry_search_connection.py`（リポジトリ直下）
   - `RegisteredLiteraturePremise`（新規クラス）
   - `RegistrySearchInput`（新規クラス）
   - `select_phase164_r3_pi5_3_leaves`（新規関数）
   - `reconstruct_phase164_r3_pi5_3`（新規関数）
2. `tests/test_phase164_r3_registry_search_connection.py`（既存 `tests/` 内）
   - `make_case`, `invoke`, `test_r3_selects_same_existing_six_leaf_objects`, `test_r3_reconstructs_pi5_3_with_unchanged_phase161_rules`, `test_r3_rejects_unreviewed_citation`, `test_r3_rejects_metadata_archive_late_or_unknown`, `test_r3_rejects_wrong_statement_binding`, `test_r3_rejects_missing_exactness`, `test_r3_rejects_untrusted_given_root`, `test_r3_rejects_duplicate_step_identity`
3. `phase164_r3_registry_search_connection/run.ps1`（ZIP 配布ディレクトリ）
4. `phase164_r3_registry_search_connection/README.md`（英語）
5. `phase164_r3_registry_search_connection/CHANGED_CODE.md`（日本語）

Python の新規クラス・関数はすべて新規ファイル内に全文定義。import を含め省略していない。

## 局所 pytest

```powershell
python -B -m pytest -q tests/test_phase164_r3_registry_search_connection.py tests/test_phase164_r2_citation_eligibility.py tests/test_phase161_r5_backward_proof_reconstruction.py tests/test_phase161_r7_premise_provenance_validation.py tests/test_phase163_r3_registry_validation.py
```

## 完了条件と次の境界

R3 完了条件：明示的に構造照合・引用資格判定した二つの文献前提と四つの独立した完全性証人が既存 R7 に渡り、七つの推論で目標に到達すること。拒否・未知・不正な対応付けは渡さないこと。R4 では実際の対象命題 ID、出典根拠、完成した証明の各前提を監査する。Phase 165 の汎用探索や新 Renderer は実装しない。全体 pytest は Phase 164 R5 のみ。
