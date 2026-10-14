# Phase 165 R57-R5 テスト実行修正

## 原因
旧 `run.ps1` が複数 Phase のテストを一回の pytest に渡し、R57-R5 フォルダーを `PYTHONPATH` の先頭に設定していた。R57-R4 テストの `from install import clean_shadowed_public_renderer` が R57-R5 の `install.py` を参照したため、テスト収集が停止した。

## 変更対象
- `phase165_r57_r5_backup_reference_cleanup/run.ps1`：全文置換。
- Python import、クラス、関数、テスト、証明探索、Renderer は変更なし。

## 対象テスト
- R57-R5
- R57-R4
- R57-R3
- R57-R2
- R56-R2

各テストファイルごとに独立した pytest プロセスを起動し、該当 Phase のディレクトリをモジュール探索の先頭にする。

## 完了条件
対象テスト5モジュールの全件成功。初回の削除はすでに適用されたため、インストーラーは再実行可能であること。全体 pytest は Phase 165 終了時まで実施しない。

## 次 Phase との境界
公開 Renderer の稼働中専用分岐や互換 API は今回変更しない。
