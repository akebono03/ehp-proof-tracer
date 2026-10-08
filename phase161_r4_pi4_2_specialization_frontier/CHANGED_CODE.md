# Phase 161-R4 changed code

## 変更対象

### `toda_group_proof_narrative_references.py`

変更関数:

- `exclude_toda_group_proof_narrative_root_reference()`

変更後全文:

- `output/exclude_toda_group_proof_narrative_root_reference.py.txt`

### `toda_group_proof_narrative_contribution_renderer.py`

新規関数。追加位置は
`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`
の直前:

- `_toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan()`
- `specialize_toda_group_proof_narrative_fixed_composition_isomorphism_application()`

変更関数:

- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

各関数の全文は `output/` に出力する。

## import

import 変更なし。

## テスト

新規:

- `tests/test_phase161_r4_pi4_2_specialization_frontier.py`

全文:

- `output/test_phase161_r4_pi4_2_specialization_frontier.py.txt`

## 実装境界

R4 は `(5.2)` fixed statement の frontier と、その target specialization のみを扱う。

Proposition 4.4 自体の定義・証明、`pi_5^3`、stable transport、Phase157 の既知 failure は変更しない。

## 更新テスト

- `tests/test_phase161_pi4_2_restored_reference_relink.py`
  - R3 の `(5.2)` linkage 回帰は保持。
  - R4 で public frontier から除外する Proposition 4.4 の旧期待値を削除。
  - 更新後全文は `output/test_phase161_pi4_2_restored_reference_relink.py.txt` に出力。
