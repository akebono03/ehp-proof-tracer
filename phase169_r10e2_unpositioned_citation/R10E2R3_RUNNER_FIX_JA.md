# Phase 169 R10E2-R3 — 差分検査の誤判定を修正

対象は `run.ps1` のみ。本番ソース、引用規則、既存テストの内容を変更しません。

R10E2-R2 では Git の除外 pathspec が機能せず、パッチ対象の6ファイルを無関係な変更と誤判定しました。R10E2-R3 では `git diff --name-only HEAD -- .` の結果を取得してから、PowerShell の `$targets -notcontains $_` で承認済みファイルを除外します。

実行前にパッチ対象6ファイルに既存の Git 差分がある場合は、上書きを防ぐため停止します。実行後は対象6ファイルの変更を確認し、それ以外の追跡ファイルで差分が増減していないことを検証します。ロールバックはパッチ実行前に保存したバックアップだけを使用し、Git reset は実行しません。

限定 pytest は R10E2-R2 と同じファイル群です。全体 pytest は実行しません。実行後の `R10E2R3_INTEGRITY_RESULT=PASS` と `R10E2R3_LIMITED_TESTS_AND_AUDIT=PASS` をもって当該工程の完了を判断します。
