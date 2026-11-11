# Phase 174 R60R1 — Reviewed HEAD Lineage Fix

## 事前監査

- GitHub `akebono03/ehp-proof-tracer` の `develop` は `17b96a63c1ee400d587c14c785c4c1e697334206`。`git compare` で local HEAD と同一と確認。
- R60 は `82d725d8649cd6307c2abd67024e3ef4f3cddfe2` を要求するため、Source Guard の6 blobが変更されていなくても HEAD 不一致で停止する。
- `82d725d8649cd6307c2abd67024e3ef4f3cddfe2` から `17b96a63c1ee400d587c14c785c4c1e697334206` までの GitHub 差分は R59 監査ディレクトリの追加と `.pytest_cache/v/cache/nodeids` の更新。R60 の6つの監査依存ファイルは変更されていない。
- 既存の `phase174_r3_r7_r60_reference_ownership_audit/audit.py` と `tests/test_audit.py`、`run.ps1` を監査した。

## 変更対象

- `phase174_r3_r7_r60_reference_ownership_audit/audit.py`: モジュール定数 `REVIEWED_HEAD` のみ `82d725d8649cd6307c2abd67024e3ef4f3cddfe2` から `17b96a63c1ee400d587c14c785c4c1e697334206` に更新（実装ファイル、関数、import は変更なし）。置換後全文は `output/R60_AUDIT_FULL_AFTER.py`。
- `phase174_r3_r7_r60r1_reviewed_head_lineage_fix/install.py`: 新規。`sha256_bytes`、`checked_patch`、`git_head`、`preflight`、`atomic_write`、`main` をファイル内に新規追加。既存クラス変更なし。
- `phase174_r3_r7_r60r1_reviewed_head_lineage_fix/tests/test_install.py`: 新規限定テスト。テスト関数は全てこのファイルに記載。
- `run.ps1`, `README.md`, `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`, `TEST_RESULTS_JA.md`：新規ファイル。

R60 による Production code の変更なし。`PINS`、Source Guard、ProofStep、Reference、Narrative、GIVEN、推論規則は変更しない。

## 実行と完了条件

1. `R60R1` の DryRun が HEAD、旧ファイル SHA256、6 blob pin を検証し PASS。
2. 本実行が1行のみを置換、旧 R60 DryRun が PASS。
3. 新規限定 pytest、R60 公開証明監査と R60/R59 限定 pytest が PASS。
4. `π_11^6` の Reference 7件、`π_12^7` の Reference 3件を維持。
5. Source Guard の緩和、新規数学規則、新規 GIVEN、全体 pytest は行わない。

## 次 Phase との境界

R60R1 は監査コードの lineage 修正のみ。Reference の出典所有関係監査は R60 が担当する。引用選択処理の統一実装は、R60 の結果を確認してから別 Phase で扱う。
