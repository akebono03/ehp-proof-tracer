# Phase 163 R4-R42 変更一覧

- 新規 `phase163_r4_r42_tex_extract.py`: `uncomment`, `clean_source`, `locate`, `extract_chapter`, `existing_reference_ids`, `make_report`, `main`。元コードは変更しない。
- 新規 `tests/test_phase163_r4_r42_tex_extract.py`: 限定テスト4件。既存テストは変更しない。
- 新規 `run.ps1`: ZIP 解凍後に限定テストと抽出監査を実行。
- `inputs/`: ユーザーがアップロードした第1〜5章 TeX 原稿をそのまま収録。

## 完了条件

原稿5件が読み込まれ、抽出 JSON と SHA-256 を生成し、限定テストが通り、元の原稿・Registry・既存 ID が変わらないこと。

## 次の境界

R4-R42 では登録・構造化・原本照合・証明探索接続をしない。次工程で label の曖昧性、TeX 外の記述と既存 ID との完全対応を確認してから登録方式を決める。
