# Phase 164 R4-R3 — 変更一覧

## 対象ファイル・クラス・関数

- 新規 `phase164_r4_r3_independent_semantic_audit.py`（リポジトリ直下）
  - `EXPECTED_SOURCES`
  - `_element`, `_group`, `_source_row`
  - `assess_typed_clauses`, `audit_current`, `write_report`, `main`
- 新規 `tests/test_phase164_r4_r3_independent_semantic_audit.py`（`tests` 直下）
  - `inputs` fixture と7つのテスト関数
- 補助 `run.ps1`（この ZIP のディレクトリ内）

既存クラス・関数・import の変更はない。新規ファイルの全文を import から末尾まで同梱し、省略はない。

## 実行テスト

```powershell
python -B -m pytest -q tests/test_phase164_r4_r3_independent_semantic_audit.py tests/test_phase164_r4_r2_semantic_structure.py tests/test_phase164_r4_r1_source_crosswalk.py
```

## 完了条件と境界

5つの型付き数式検査が成立し、不一致が拒否され、数学的真偽・原本照合・引用資格は未認定と記録されること。R4-R3 では命題を Registry に昇格させず、Backward Search へ渡さない。Phase 164 の最後まで全体 pytest は行わない。
