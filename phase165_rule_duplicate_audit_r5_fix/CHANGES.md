# Phase 165 R5 修正内容

- 新規 `audit.py`: `rule_signature()`、`grouping()`、`main()`。廃止済み Catalog の構築を廃止し、有効な R8 規則発見結果だけを監査する。
- 新規 `test_audit.py`: `test_grouping_identifies_repeated_names_only()` と `test_active_discovery_does_not_reintroduce_removed_pi43_rules()`。
- `run.ps1`: モジュール起動と対象 pytest 2件。
- 本番ファイル・既存テストに変更なし。全体 pytest は実施しない。
- 統一規則台帳全体の一意性判定は監査対象外と明示。
