# Phase 163 R4-R56 変更一覧

## 対象

- 新規 `phase163_r4_r56_scope_evidence_trial.py`：`ScopeEvidence`、`sha256`、`_compact`、`_evidence`、`build_scope_report`、`write_report`、`main` を新規追加。
- 新規 `tests/test_phase163_r4_r56_scope_evidence_trial.py`：9 テストと `inputs` を新規追加。
- 新規 `run.ps1`：PowerShell 実行用。
- 新規 `README.md` と `CHANGED_CODE.md`。

既存ファイル、クラス、関数、import は変更なし。すべてのコードは同梱ファイルをそのまま利用可能。出典明示の式のみを採録し、不明な数学的制約の補完はしない。

## pytest

`python -m pytest -q phase163_r4_r56_scope_evidence_trial/tests/test_phase163_r4_r56_scope_evidence_trial.py`

## 完了条件

仮登録3件について明示的な変数、2件の定義域と値域、1件の3場合分けを出典付きで保存し、9テストを通す。

## 次 Phase 境界

R4-R57 以降に条件の意味検証と他の定義候補への一般化を残す。本番登録は行わない。
