# Phase 161-R4-R3 changed code

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

新規関数:

- `_toda_group_proof_narrative_fixed_frontier_internal_step_ids()`

追加位置:

- `_toda_group_proof_narrative_reference_internal_step_ids()` の直前。

変更関数:

- `_toda_group_proof_narrative_reference_internal_step_ids()`

変更後・新規関数の全文は `output/` に出力する。

## import

production import の変更なし。

## テスト

変更:

- `tests/test_phase161_r4_pi4_2_specialization_frontier.py`
- `tests/test_phase161_r4_repair1_pi4_2_semantic_frontier.py`

新規:

- `tests/test_phase161_r4_r3_fixed_frontier_internal_ancestry.py`

各テストファイル全文は `output/` に出力する。

## 一般規則

public frontier 上の `FIXED_STATEMENT` の証明にのみ使われる upstream step は、
明示的な literature reference を持っていてもその fixed statement の
proof-internal ancestry として扱う。

ただし、closure 外にも consumer を持つ shared step は吸収しない。

## Phase 境界

R4-R3 では以下を変更しない。

- `(5.2)` の数学的 statement
- Proposition 4.4 の repository 上の provenance
- `pi_5^3`
- `pi_6^4`
- stable transport
- documentation
- Phase157 の既知 failure
- 全体 pytest
