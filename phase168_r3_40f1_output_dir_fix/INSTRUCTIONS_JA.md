# Phase 168 R3-40F1 — 監査出力先の作成修正

## 変更対象

- `phase168_r3_40f_residual_route_audit/audit.py`: `audit_four_cases()` 全文置換（関数自身が `OUTPUT.mkdir(parents=True, exist_ok=True)` を実行する）。追加位置は `results = []` の直前。
- `phase168_r3_40f_residual_route_audit/tests/test_phase168_r3_40f_residual_route_audit.py`: `test_four_existing_narratives_have_no_deferred_entries()` 全文置換。pytest の一時ディレクトリを未作成状態で指定し、自動作成と4群の保存結果を確認する。
- `run.ps1`: R3-40F の監査パッケージだけに上記2ファイルを適用し、限定 pytest と監査を実行する。

モジュールの import は変更しない。関数全文・変更後ファイル全文は `full_functions/`, `full_files/` に収録した。`README.md`, `design.md`, `development_log.md`, `roadmap.md`, `proof_records.md` は変更しない。

## 使い方

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r3_40f1_output_dir_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_40f1_output_dir_fix\run.ps1"
```

## 検証

限定 `pytest` は R3-40F の4件を実行する。その後 `python -m phase168_r3_40f_residual_route_audit.audit` を実行し、`phase168_r3_40f_residual_route_audit/output/` に `audit.json`, `audit.md`, 4群の `*_current.md`, `review_bundle.zip` を生成する。失敗時には監査コードとテストを復元する。数学的推論、Renderer、Projection、固定基準、登録命題は変更しない。全体 pytest は Phase 168 終了時まで実行しない。
