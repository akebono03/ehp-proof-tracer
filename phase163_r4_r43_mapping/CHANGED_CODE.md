# Phase 163 R4-R43 — 変更対象と実行境界

- 新規 `phase163_r4_r43_mapping/phase163_r4_r43_mapping.py`: `classify`, `build_mapping`, `check_sources`, `write_output`, `main`。原稿ハッシュ検証、文献参照 ID 候補照合、未解決分類、監査出力。
- 新規 `phase163_r4_r43_mapping/tests/test_phase163_r4_r43_mapping.py`: 限定テスト6件。
- 新規 `phase163_r4_r43_mapping/run.ps1`: 既存 R4-R42 結果を利用し、限定 pytest 後に監査実行。
- 新規 `README.md`, `CHANGED_CODE.md`: 全文同梱。
- 既存ファイル、クラス、関数、import、Statement ID は変更しない。証明探索接続なし。
- 次工程ではコンポーネント単位の同一性を確認する。今回は一括登録を実施しない。
