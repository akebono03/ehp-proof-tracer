# Phase 163 R4-R41 変更対象

新規ファイル：`phase163_r4_r41_tex_bulk_inventory/phase163_r4_r41_tex_inventory.py`。追加関数は `inspect_sources`、`inspect_registry`、`build_report`、`main`。既存クラス・関数は変更しない。

新規テスト：`tests/test_phase163_r4_r41_tex_inventory.py` の3件。新規 `run.ps1`、`README.md`。既存の `README.md`、`design.md`、`development_log.md`、`roadmap.md`、`proof_records.md` は変更しない。

完了条件：限定テスト合格、5章分の入力有無と SHA-256 記録、既存 ID の読み取り専用棚卸し、原本不変更。次工程：本文の抽出規則と同一性照合を確定してから書き込み処理を追加する。
