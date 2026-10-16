# Phase 165 R6-1 追加監査

静的 import グラフであり、実行時呼び出しの証明ではありません。

## 件数

- ACTIVE_GROUP_SPECIFIC_ADAPTER: 1
- GROUP_TYPE_BRANCH_REVIEW: 109
- NAMED_GROUP_BRANCH_REVIEW: 7
- NOT_REACHABLE_FROM_SELECTED_ENTRIES: 162
- REACHABLE_COMMON_OR_UNCLASSIFIED: 334

## 接続確認

- pi43_adapter_imported: True
- pi43_adapter_in_shared_provider: True
- pi43_adapter_has_fixed_target: True
- generic_backward_provider_connected: True

## 審査が必要な候補

- `phase162_pi5_3_backward_selection.py:85` `expand_phase162_pi5_3_group_goal` — NAMED_GROUP_BRANCH_REVIEW (import-reachable: False)
- `phase162_pi5_3_backward_selection.py:119` `reconstruct_phase162_pi5_3_group_goal` — NAMED_GROUP_BRANCH_REVIEW (import-reachable: False)
- `phase165_r14_r37_closure.py:46` `strict_search_attempt` — NAMED_GROUP_BRANCH_REVIEW (import-reachable: False)
- `phase165_r14_r38_direct_registry.phase165_r42_backup.py:79` `reconstruct_registered_pi32` — NAMED_GROUP_BRANCH_REVIEW (import-reachable: False)
- `phase165_r14_r38_direct_registry.py:95` `reconstruct_registered_pi32` — NAMED_GROUP_BRANCH_REVIEW (import-reachable: True)
- `phase165_r52_r23_existing_rule_adapter.py:52` `expand_existing_pi43_rules` — ACTIVE_GROUP_SPECIFIC_ADAPTER (import-reachable: True)
- `toda_rules.py:29780` `toda_prop51_finite_dimensional_integration_inference_rule` — NAMED_GROUP_BRANCH_REVIEW (import-reachable: True)
- `toda_rules.py:32576` `toda_prop53_finite_dimensional_integration_inference_rule` — NAMED_GROUP_BRANCH_REVIEW (import-reachable: True)

## 制限

- import reachability is an over-approximation, not runtime call proof
- dynamic imports and classes/nested functions may be missed
- named-group branches require human semantic judgment
- prior 450 candidates are not reproduced verbatim by this different classifier
