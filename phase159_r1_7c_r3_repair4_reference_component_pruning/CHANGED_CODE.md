# Phase 159 R1-7c R3 repair4 — changed code

## 変更対象

### Production
`toda_group_proof_narrative_contribution_renderer.py`

新規 functions:
- `_phase159_r1_7c_r3_repair4_aggregate_zero_component_line()`
- `prune_toda_group_proof_narrative_root_zero_direct_premise_references()`

変更 function:
- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

import の変更:
- なし。R3 で追加済みの `fields`, `is_dataclass`, `replace`,
  `ScalarSymbol`, `TodaPrimaryGroupZeroStatement`,
  `ScalarGreaterEqualStatement`, `_render_scalar_latex` を再利用する。

apply 後、変更後 function 全文を以下に出力する:
- `output_after_apply/prune_reference_function_after.txt`
- `output_after_apply/render_multi_argument_function_after.txt`

## 新規 test file

`tests/test_phase159_r1_7c_r3_repair4_reference_component_pruning.py`

package 内の同名ファイルが必要 import と test functions の全文である。
