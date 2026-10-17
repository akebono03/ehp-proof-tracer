# Phase 165 R5 変更

- 新規 `phase165_rule_duplicate_audit_r5/audit.py`: `rule_signature`, `grouping`, `main` を追加。
- 新規 `phase165_rule_duplicate_audit_r5/test_audit.py`: `test_catalog_keys_are_unique`, `test_no_removed_pi43_dedicated_rule_names` を追加。
- 新規 `run.ps1` と `__init__.py`。本番コードは変更しない。
- 既存 API と本番テストは変更しない。全体 pytest を実行しない。
- 完了条件: 台帳の重複候補と共通探索との重なりを JSON に出力。数学的同値性の確定や削除は次段階。
