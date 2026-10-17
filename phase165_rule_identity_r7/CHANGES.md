# Phase 165 R7 変更一覧

- 新規 `audit.py`: `callable_evidence()`、`rule_evidence()`、`classify_pair()`、`main()`。有効な R8 規則から5組を取得し、前提・結論・Guard・結論生成処理を比較する。
- 新規 `test_audit.py`: `test_review_pair_inventory_has_five_unique_pairs()`、`test_review_preserves_rules_and_reports_five_pairs()`。
- 新規 `run.ps1`: 監査と対象限定 pytest 2件を実行。
- 本番コード・既存テストは変更しない。
- 完了条件: 5組の証拠を JSON に保存し、規則の削除・統合を行わない。
- 次 Phase 境界: Rule ID の正式統合や規則改修は今回行わない。
