# Phase 163 R4-R59 変更一覧

既存ファイル・クラス・関数・import は変更していません。

## 新規ファイルと位置

- `phase163_r4_r59_id_order_trial/phase163_r4_r59_id_order_trial.py`：新規モジュール。`OrderSnapshot`、`read_readiness`、`build_trial_registry`、`simulate_insertion`、`write_outputs`、`main` を収録。
- `phase163_r4_r59_id_order_trial/tests/test_phase163_r4_r59_id_order_trial.py`：新規テスト9件。
- `phase163_r4_r59_id_order_trial/run.ps1`：限定 pytest と監査の実行。
- `phase163_r4_r59_id_order_trial/README.md`：英語の説明。
- このファイル：日本語の変更一覧。

新規の import・クラス・関数・テストは各 Python ファイルに全文収録しています。既存 Registry は変更せず、合成項目は正式登録しません。Phase 163 の全体 pytest は実施しません。次の Phase では、本番 ID の付与方針と重複防止の設計を検討できますが、本 Phase には含みません。
