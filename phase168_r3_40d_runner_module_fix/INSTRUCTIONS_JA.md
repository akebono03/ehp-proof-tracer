# Phase 168 R3-40D — 監査起動の修正

## 発生した問題

R3-40C の限定 pytest は13件 PASS しましたが、その後 `check_and_capture.py` をファイルパスで直接起動したため、リポジトリ直下の Python モジュールを読み込めずに失敗しました。実装の3ファイルは R3-40C の `run.ps1` によってロールバックされています。

## 変更対象

- **今回の変更**：この ZIP 内の `run.ps1`。`check_and_capture.py` をリポジトリ直下から `python -m phase168_r3_40d_runner_module_fix.check_and_capture` で起動します。スクリプト全体を同梱しています。
- **追加テスト**：`tests/test_phase168_r3_40d_runner_module_fix.py`。import 検索経路に関する回帰テスト2件を同梱しています。
- **再適用する R3-40C 実装**：`phase168_r3_29_order_projection.py` の `project_narrative_order()`、`phase168_r3_27_typed_statement_projection.py` の新規 `project_stable_eta_notation_transition()`、`phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()`。これらの実装と関連テストは R3-40C から一切変更していません。すべての関数全文は `full_functions/` にあります。冒頭の import は変更しません。

## 実行方法

PowerShell でリポジトリ直下へ移動します。

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r3_40d_runner_module_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_40d_runner_module_fix\run.ps1"
```

## テスト・完了条件・境界

限定 pytest（R3-40C の13件＋新規2件）、4群の依存関係逆転チェック、既存3群の固定基準比較を実行します。すべて正常終了して初めて今回の修正を完了とします。途中で失敗すれば実装の3ファイルを再びロールバックします。全体 pytest は Phase 168 終了時だけ実行します。

Proof Search、命題台帳、文献順、全体 Renderer 構造や将来 Phase に変更を加えません。
