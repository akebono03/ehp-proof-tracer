# Phase 164 R4-R2 — 変更対象

- `phase164_r4_r2_semantic_structure.py`（プロジェクト直下に新規追加）
  - `PROP51_COMPONENTS` 定数
  - `_find_row`、`compare_structured_leaves`、`audit_current`、`write_report`、`main` を新規追加
- `tests/test_phase164_r4_r2_semantic_structure.py`（`tests` に新規追加）
  - `inputs` fixture および6件の test 関数を新規追加
- 既存ファイル・クラス・関数・import の変更なし。
- 新規 Python ソースと import は ZIP 内の各ファイルに全文で収録。
- 全体 pytest は Phase 終了時のみ。原本照合・命題同値性・引用資格の認定はこの段階では実施しない。
