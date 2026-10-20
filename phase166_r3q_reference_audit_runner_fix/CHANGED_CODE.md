# Phase 166 R3-Q 監査起動修正

## 対象ファイル・関数

- `phase166_r3q_reference_audit_runner_fix/run.ps1`：監査の起動方法を修正（関数・クラスなし）。
- `phase166_r3q_reference_audit_runner_fix/audit.py`：前回と同一の監査コードを収録（変更なし）。
- `README.md`：英語の実行方法を全文記載。
- `CHANGED_CODE.md`：日本語の変更説明を全文記載。

## 原因と変更

従来の `python <subdirectory>/audit.py` 実行では Python の `sys.path[0]` が監査ディレクトリとなり、リポジトリ直下の `homotopy_groups.py` を import できなかった。
今回は `Push-Location` でリポジトリ直下へ移動し、`python -m phase166_r3q_reference_audit_runner_fix.audit` として起動する。`finally` で元の場所に戻す。

## 実行するテスト・完了条件

限定確認：監査コマンドが終了コード0で完了し `phase166_r3q_reference_audit_results/audit.json` が作成されること。今回 pytest は実行しない。全体 pytest は Phase 166 終了時のみ実行。

## 次工程との境界

順序判定、本番コード、命題台帳、既存テストには手を加えず、監査で確定した原因を次の作業で扱う。
