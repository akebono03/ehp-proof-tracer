# Phase 165 R6：変更内容

- 新規 `phase165_rule_duplicate_review_r6/audit.py`: `describe_rule()`、`classify_pair()`、`main()` を追加。R5で見つかった5組を現行のR8規則から抽出し、定義情報を比較する。
- 新規 `phase165_rule_duplicate_review_r6/test_audit.py`: `test_distinct_conclusions_are_not_marked_duplicates()`、`test_missing_conclusion_patterns_are_not_certified_duplicates()` を追加。
- 新規 `run.ps1`: 対象監査と対象 pytest 2件を実行する。
- 本番コード・既存テスト・README.md等のルート文書には変更なし。
- 旧Catalogは使用しない。全体pytestは実行しない。
