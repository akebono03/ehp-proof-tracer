# Phase 168 R3-41P1 — 監査ランナー実行エラー修正

2026年10月24日

## 目的と範囲

R3-41P の audit-only 実行が Windows PowerShell 上で `NativeCommandError` により中断した問題を修正する。R3-41P の証明責務監査そのものは未完了とし、数学的なコード変更は一切行わない。

## 事前確認

- 前回取得した GitHub `develop` の Renderer/Projection/Model/関連テスト実装を参照。
- 前回作成した R3-41P audit-only ZIP の `audit.py` と `run.ps1` の全体を再点検。
- 問題のトリガーを `run.ps1` の `$ErrorActionPreference = "Stop"` と Python 標準エラーの `2>&1` に確認。
- Python が実際に起こした例外の内容は現時点で不明。新しい監査結果のログから診断する。

## 変更ファイル・関数

1. `phase168_r3_41p_boundary_audit/run.ps1`：スクリプト全体を置き換え。新規 `Invoke-LoggedPython()` は変数宣言の直後に追加。標準出力と標準エラーを別々に取得し、例外発生後もログ・ZIP を作成。
2. `phase168_r3_41p_boundary_audit/audit.py`：`runtime_audit()` 全体を変更。3群の監査を独立して実行し、群別エラーを JSON とテキストに保存。
3. 同 `audit.py`：`render_report()` 全体を変更。エラーが発生した群を `ERROR` として表示し、詳細 Traceback を掲載。
4. 同 `audit.py`：`main()` 全体を変更。古い群別の結果を消去し、新しい監査状態を保存、エラーがあれば非ゼロ終了を維持。
5. `phase168_r3_41p_boundary_audit/tests/test_audit_error_reporting.py`：新規ファイル。テスト3件全文と必要 import を収録。
6. `phase168_r3_41p_boundary_audit/README.md`：実行方法と出力ファイルの説明を更新し、全文を収録。

既存のアプリケーションファイルの import、クラス、関数、API は変更しない。コードの省略はない。

## 事前テスト

```text
python -m pytest -q -p no:cacheprovider phase168_r3_41p_boundary_audit/tests/test_audit_error_reporting.py
3 passed in 0.08s
```

これは監査ランナーの単体テストのみである。ユーザーの Windows 上の監査・限定 pytest は未実行。全体 pytest は Phase 168 終了まで行わない。

## 完了条件

- 失敗時も `output/audit_console_stderr.log` と `output/audit.json` と `output/audit.md` が残る。
- 群別失敗時、ほかの2群の監査を続行する。
- `output/review_bundle.zip` を出力する。
- 既存ソース・ProofStep・Reference を変更しない。
- 既存の限定 pytest と今回の回帰テストの結果を収集する。

## 次工程との境界

R3-41P1 はランナー修正に限定する。取得した監査結果から数学的再判定の責務分離が必要な箇所を判断する工程とは切り離す。
