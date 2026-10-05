# Phase 158-R5-5b repair1l changed code

## 変更対象

`toda_group_proof_narrative_argument_body_renderer.py`

変更関数:
`_relocatable_toda_group_proof_narrative_direct_derivation_premises()`

import の変更はありません。

変更後の関数全文:

```python
def _relocatable_toda_group_proof_narrative_direct_derivation_premises(
  direct_derivation_premises: tuple[
    ProofStep,
    ...,
  ],
  sources_by_target_id: dict[
    int,
    tuple[
      ProofStep,
      ...,
    ],
  ],
  conclusion_block: TodaGroupProofNarrativeBlock,
) -> tuple[
  ProofStep,
  ...,
]:
  transition_source_step_ids = frozenset(
    id(
      source_step
    )
    for source_steps in sources_by_target_id.values()
    for source_step in source_steps
  )

  return tuple(
    premise_step
    for premise_step in direct_derivation_premises
    if (
      premise_step not in conclusion_block.steps
      and id(
        premise_step
      ) not in transition_source_step_ids
      and not sources_by_target_id.get(
        id(
          premise_step
        ),
        (),
      )
      and not (
        is_toda_group_proof_narrative_provenance_only_statement(
          premise_step.conclusion
        )
      )
    )
  )
```

## Tests

新規・変更なし。

既存 tests:
- Phase 148 calculation-chain restoration
- Phase 156 canonical connector/local-order
- Phase 156 relation-side normalization
- Phase 157 reflexive-equality suppression
- Phase 149 local-body ordering
- Phase 158-R5-5b ordering
- Phase 150 route contracts

## Phase boundary

- transition-source relocation guard のみ追加
- equation numbering algorithm は変更しない
- proof graph は変更しない
- semantic dependency は変更しない
- Argument ordering は変更しない
- group-specific rule は追加しない
- repository-wide pytest は実行しない
