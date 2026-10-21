# Phase 166 終了試験：インストーラ誤収集の防止

## 変更対象

- 新規 `phase166_close_installer_exclusion/close.py`：`main()` 関数全体。
- 新規 `phase166_close_installer_exclusion/run.ps1`：実行スクリプト全文。
- 新規 `README.md` と `AUDIT.md`。
- 本番コード、既存テスト、既存文書への変更なし。

## 現行コードと関連テストの確認

GitHub `develop` の `phase165_r6_8_eta_name_fix/install_and_test.py`、`phase165_r6_8_phase58_cutover/install_and_test.py` を確認。どちらも import 時に本番ソースの書き換えまたは `SystemExit` を起こす可能性のある施工スクリプト。後者の通常テスト `test_phase165_r6_8_phase58_cutover.py` は引き続き収集対象。

## 実行範囲

`python -m pytest -q -p no:cacheprovider --ignore-glob=*install_and_test.py` を実行する。対象ファイルの実際のリスト、全体出力、終了コード、Git 状態を保存する。ほかのテストは除外しない。

## 完了条件

終了コード0。失敗または収集エラーが残れば Phase 166 正式完了は保留。全体テストの再実行は前回終了試験で生じた収集停止を解除する目的に限定する。

## Phase 167 との境界

証明探索、ProofStep、Narrative renderer の修正は Phase 167 で行う。
