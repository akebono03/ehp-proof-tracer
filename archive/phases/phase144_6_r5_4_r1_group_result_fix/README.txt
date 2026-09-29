Phase 144-6-R5-4-R1 Argument dependency gap audit repair

変更対象
--------
audit_phase144_6_r5_4_argument_dependency_gap.py
- _group_result() のみ修正。

修正内容
--------
誤:
  report.group_result

正:
  report.candidates[0].source_candidate.group_result

R5-2/R5-3 と同じ既存 API 経路を使用する。

production code: 変更なし
tests: 変更なし
project documents: 変更なし
監査ロジック: 変更なし
full pytest: 実行しない
