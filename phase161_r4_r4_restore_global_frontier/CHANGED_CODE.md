# Phase 161-R4-R4 changed code

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

変更関数:

- `_toda_group_proof_narrative_reference_frontier_step_ids()`
  - Phase156-R13 の global frontier 契約へ復帰。
- `_toda_group_proof_narrative_reference_internal_step_ids()`
- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`
  - R4-repair1 で追加した early global frontier filtering を除去。

新規関数:

- `_toda_group_proof_narrative_root_fixed_statement_internal_step_ids()`

削除:

- `_filter_toda_group_proof_narrative_reference_entries_to_frontier()`
- `_toda_group_proof_narrative_fixed_frontier_internal_step_ids()`

各変更後関数全文は `output/` に出力する。

## import

production import の変更なし。

## テスト

新規:

- `tests/test_phase161_r4_r4_restore_global_frontier.py`

全文:

- `output/test_phase161_r4_r4_restore_global_frontier.py.txt`

## 一般規則

global Reference frontier の意味は変更しない。

root が `PROOF_INTERNAL` かつ、その root と同一 locator の
`FIXED_STATEMENT` が root ancestry に存在するときだけ、その fixed statement
の exclusive proof ancestry を public body から抑制する。

これにより pi_4^2 の Proposition 4.4 を内部化しつつ、pi_6^3 の既存 `(5.2)`
frontier を維持する。

## Phase 境界

今回変更しない:

- Phase156 repair8 の stale test expectation
- pi_5^3
- pi_6^4
- stable transport
- documentation
- 全体 pytest
