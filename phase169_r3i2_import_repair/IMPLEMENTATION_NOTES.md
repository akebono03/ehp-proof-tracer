# Phase 169 R3I2 — R3H テストの import 復旧

## 原因

R3I1 の限定テストは 37 PASS・1 FAIL で停止した。旧 R3H テストを全文置換する際、`ProofSearchStatus` の import を削除したにもかかわらず、既存の `test_r3h_pi4_2_remains_complete()` が `ProofSearchStatus.COMPLETE` を参照し続けたため、`NameError` が発生した。

## 変更対象

- `phase169_r3h_toda53_hopf_source/tests/test_phase169_r3h_toda53_hopf_source.py` — **変更後の import 全文を含むテストファイル全文**は `full_tests/test_phase169_r3h_toda53_hopf_source.py` に保存。`from phase165_r52_partial_proof import ProofSearchStatus` の1行を復旧。R3I1 で変更した2つの既存テストの関数全体は変更しない。
- `tests/test_phase169_r3i2_import_regression.py` — 新規テスト2関数を全文収録。修復した import と元の `test_r3h_pi4_2_remains_complete()` の参照を検査。
- `tests/test_phase169_r3i2_proof_closure_audit.py` — R3I1 の監査テスト2関数全文。監査モジュールの import 先のみ新 ZIP のパッケージ名に合わせる。
- `run.ps1` — 必要ファイルおよび復旧された import を **適用前**に検査。限定 pytest・完成証明監査と失敗時の復元処理を維持。
- `audit.py` — R3I1 と同じ証明木監査内容。フェーズ表示およびレポートのフェーズ番号のみ更新。
- `patch_r3h_tests.py` — R3I1 と同じ内容のガード付き全文置換・復元（表示フェーズ番号のみ更新）。
- `apply.py`、`full_functions/shared_expansion_provider.py`、`full_functions/expand_cited_ehp_terminal_goal.py` — R3I1 と同一。数学的規則・Production API は変更しない。

## 限定テスト

`run.ps1` に記載の R3I、R3I2、R3H、R3F3、および既存 EHP 関連テストだけを実行する。全体 pytest は行わない。

## 完了条件

`R3I2_FOCUSED_PYTEST_EXIT_CODE=0`、`R3I2_CLOSED_PROOF_TREE_VERIFIED=True`、`R3I2_AUDIT_EXIT_CODE=0`、`R3I2_COMPLETE`。これらの実測をもって $\pi_5^3$ の完成証明木を確認する。

## 次段階との境界

R3I2 は import と監査の最小限の修正のみ。Renderer（文章表示）と Reference の改善、$\pi_6^4$ への輸送、および全体 pytest はここで実施しない。
