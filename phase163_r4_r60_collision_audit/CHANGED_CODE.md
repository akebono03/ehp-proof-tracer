# Phase 163 R4-R60 変更コード

変更対象の既存ファイル・クラス・関数・import：なし。

新規追加：

- `phase163_r4_r60_collision_audit.py`：`load_json`、`audit`、`live_id_snapshot`、`write_outputs`、`main`。各関数は新規ファイル内に全文掲載。
- `tests/test_phase163_r4_r60_collision_audit.py`：9件の限定テスト。import・関数全文を掲載。
- `run.ps1`：R4-R59 の既存出力パスを参照し、限定 pytest と監査を実行。
- `README.md`：英語の実行説明。

既存台帳の変更・正式 ID 発行・全体 pytest は行わない。次の R4-R61 では衝突監査結果に基づく ID 発行方針の検証を検討する。
