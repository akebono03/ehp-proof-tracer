# Phase 167 R4-②: 表示呼び出し監査（改訂版）

読み取り専用です。公開 Web 経路を実行し、Python の `sys.setprofile` で Renderer 系関数の実呼び出しを記録します。ProofStep オブジェクトの `id()` に依存しません。

現行コードを変更せず、`trace_v2.json` に呼び出し関数数・型付き引数・Web Narrative 全文を出力します。2-stem や全体 pytest は実行しません。

PowerShell のリポジトリルートで `run.ps1` を実行し、`trace_v2.json` を添付してください。
