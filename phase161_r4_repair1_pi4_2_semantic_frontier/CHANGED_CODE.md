# Phase 161-R4 repair1 changed code

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

変更関数:

- `_toda_group_proof_narrative_reference_frontier_step_ids()`
- `_toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan()`
- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

新規関数:

- `_filter_toda_group_proof_narrative_reference_entries_to_frontier()`

追加位置:

- `_toda_group_proof_narrative_reference_frontier_step_ids()` の直前。

各関数の変更後全文は `output/` に出力する。

## import

import 変更なし。

## テスト

新規:

- `tests/test_phase161_r4_repair1_pi4_2_semantic_frontier.py`

テストファイル全文は:

- `output/test_phase161_r4_repair1_pi4_2_semantic_frontier.py.txt`

## 修正内容

1. `Toda52CompositionIsomorphismStatement` を実際の semantic fields
   `source_group`, `target_group`, `composition` から読む。
2. `FIXED_STATEMENT` を Reference frontier として扱い、その背後の
   literature dependency を public frontier に通さない。
3. root-reference exclusion の直後に frontier filter を適用する。
4. Proposition 4.4 は `(5.2)` の proof-internal dependency として public
   Reference / proof body から除外する。

## Phase 境界

今回変更しないもの:

- `pi_5^3`
- `pi_6^4` stable base
- stable transport
- documentation
- Phase157 の既知 failure
- 全体 pytest
