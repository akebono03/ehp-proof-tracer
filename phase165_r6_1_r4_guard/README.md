# Phase 165 R6-1 R4：旧群専用経路の参照監査

変更対象の production ファイル、クラス、関数はありません。新規監査ファイルは `audit.py` の `inspect()`、`test_audit.py` の3つのテスト関数、`run.ps1` です。

リポジトリ直下の Python ファイルに限り、旧群専用関数の `Call` / `ImportFrom` を AST（抽象構文木）で確認します。全階層・実行時の到達可能性の保証ではありません。削除可否は使用箇所が確認できてから決定します。既存の文献 Registry は維持します。

実行：`powershell -ExecutionPolicy Bypass -File .\phase165_r6_1_r4_guard\run.ps1`

出力：`phase165_r6_1_r4_guard/remaining_paths.json`。全体 pytest は行いません。

R6-1 の完了条件：共通証明入口に使われる各関数の置換先と、旧経路のみの関数を識別する。R6-2 は共通逆向き規則を接続し、撤去可能になった Adapter を削除する工程です。
