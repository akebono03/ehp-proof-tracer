# Phase 163 R4-R58 変更一覧

既存コードは変更なし。以下の新規ファイルを追加する。

- `phase163_r4_r58_registration_readiness.py`: 新規関数 `digest`、`assess`、`write_report`、`main` を同ファイル内に追加。import はファイル冒頭に全文記載。
- `tests/test_phase163_r4_r58_registration_readiness.py`: 新規テスト9件。import はファイル冒頭に全文記載。
- `run.ps1`: 既存 R55-R57 JSON を入力としてテスト・監査実行。
- `README.md`: 英語の実行説明。
- `CHANGED_CODE.md`: 本記録。

完了条件：3件の文献位置・原文根拠・仮 ID を検証し、形式的意味検証と証明利用を未完了として保持。全体 pytest は Phase 163 終了時のみ実行。次 Phase では ID 衝突・文献掲載順の確定に進めるが、この Phase で本番移行しない。

## R4-R58 入力パス修正版

- 変更対象：`tests/test_phase163_r4_r58_registration_readiness.py` の import 全体と `inputs()` fixture 全体。
- 変更対象：`run.ps1` 全体。R55、R56、R57 の絶対パスを環境変数でテストに渡す。
- README.md は全文を更新。
- `assess`、`write_report`、`main` および既存本番コードは変更なし。
- root 直下の `trial.json`、`scope.json`、`boundary.json` を参照しない。
