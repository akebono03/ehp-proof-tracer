# Phase 163 R4-R61 変更内容

既存の GitHub 実装 `unified_statement_registry.py`、`phase163_r4_registry_bridge.py` および関連テストを確認済み。既存のクラス・関数・import は変更しない。

## 新規ファイル

- `phase163_r4_r61_registration_gate.py`：読み取り専用照合。新規関数 `load_json`, `assess`, `write_outputs`, `main` をファイル内に追加。
- `tests/test_phase163_r4_r61_registration_gate.py`：fixture `inputs` とテスト関数9件を新規追加。
- `run.ps1`：R4-R58、R4-R59、R4-R60 の標準サブディレクトリを参照。
- `README.md`：英語の操作説明。
- `CHANGED_CODE.md`：本記録。

変更後の import、すべての新規関数とテスト関数は、それぞれ上記 Python ファイルに省略なしで収録。変更対象となる既存関数・クラスはない。

## 完了条件

限定 pytest 9件が通過し、3つの入力の出典同一性・ID 不変性・衝突監査が一致すること。数学的未検証9事項を保持し、正式登録・引用・証明利用を許可しないこと。全体 pytest は Phase 163 の最後だけ実行する。

次 R4-R62 への境界：正式な ID 発行、数学的意味解析、本番 Registry の移行は今回行わない。
