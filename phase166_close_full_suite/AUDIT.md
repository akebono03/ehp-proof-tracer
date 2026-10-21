# Phase 166 終了判定

## 変更対象

新規 `phase166_close_full_suite/close.py` の `run_command()`・`main()`、`run.ps1`、`README.md`、`AUDIT.md`。本番コード・既存テスト・既存文書は変更しない。

## 実施内容

現在の Git HEAD と作業ツリーの状況を記録し、`python -m pytest -q -p no:cacheprovider` を Phase 166 終了時に実行する。全ログと終了コードを保存する。

## 完了条件

全体 pytest の終了コード 0、出力ログと git 状態の確認を経て正式完了とする。失敗時は Phase 166 を未完了扱いにして原因を整理する。成功したという報告は実行前にしない。

## Phase 167 との境界

Phase 167 は π₄³ の ProofStep と Narrative・出典表示を再監査・修正する。`generic-complete-proof` と表示の適切さは区別し、次に π₅³ の partial 状態を調査する。Phase 166 終了スクリプトはこれらの修正を実施しない。
