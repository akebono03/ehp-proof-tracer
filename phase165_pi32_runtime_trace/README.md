# Phase 165 R49/R50: pi3^2 renderer runtime trace

読み取り専用の実行時監査。ProofStepからWeb出力までを段階ごとに追跡します。

- `audit.py`: 既存モジュールをメモリ上で一時的にwrapし、各段階の出力を記録する。finallyで元に戻す。本番ソースは書き換えない。
- `run.ps1`: Windows PowerShellから実行する。
- `phase165_pi32_runtime_trace_output/audit.json`: 構造化監査結果。
- `phase165_pi32_runtime_trace_output/report.md`: 段階ごとの文章と集計。

検査内容: ProofStepの対象命題と前提、Presentationのnodes/edges、ReasonSidecarの理由分類、文献抽出・使用判定、理由挿入、正規化、Web出力。監査中の一時的な関数wrapは実行経路の観測に限定する。`pytest`は実行しない。

**注意**: 実行時例外が発生しても報告書を保存する。原因は `audit.json` の `traceback` を確認する。結果が `status=ok` でない場合、監査は未完了。

## Runner fix

`audit.py` は `Path.cwd()`（プロジェクト直下）を `sys.path` に追加してから、プロジェクトのモジュールを import します。監査内容・本番コード・pytest の扱いは変更しません。
