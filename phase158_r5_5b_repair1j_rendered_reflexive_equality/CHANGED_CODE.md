# Phase 158-R5-5b repair1j changed code

## 変更対象

`toda_group_proof_narrative_argument_body_renderer.py`

### 変更後 import 部分

```python
from toda_group_proof_generic_narrative_renderer import (
  _generic_narrative_dependency_labels,
  _generic_narrative_sentence_lead,
  _generic_short_exact_sequence_reason_prose,
  _render_generic_narrative_proof_block,
  _render_generic_narrative_step,
)
from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  TodaGroupProofNarrativeExactnessMethodComponent,
)
from toda_group_proof_narrative_exactness_contribution_ownership import (
  filter_toda_group_proof_narrative_exactness_body_contributions,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  TodaGroupProofNarrativeExactnessDisplayContributionKind,
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_group_proof_narrative_exactness_exposure import (
  TodaGroupProofNarrativeExactnessExposureClass,
)
from toda_group_proof_narrative_group_structure_semantics import (
  extract_toda_group_structure_narrative_redundant_direct_premise_step_ids,
)
from toda_group_proof_narrative_provenance_catalog import (
  is_toda_group_proof_narrative_provenance_only_statement,
)
from toda_group_proof_narrative_step_transitions import (
  extract_toda_group_proof_narrative_step_transitions,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)
```

### 変更関数全文

```python
def _is_toda_group_proof_narrative_rendered_reflexive_equality_step(
  proof_step: ProofStep,
) -> bool:
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  statement = proof_step.conclusion

  if (
    not isinstance(
      statement,
      Relation,
    )
    or statement.relation_type
    is not RelationType.EQUALITY
  ):
    return False

  try:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    return False

  if (
    not rendered.startswith(
      "$"
    )
    or not rendered.endswith(
      "$"
    )
  ):
    return False

  equation = rendered[
    1:-1
  ]
  separator = " = "

  if separator not in equation:
    return False

  lhs_rendered, rhs_rendered = equation.split(
    separator,
    1,
  )

  return (
    lhs_rendered
    == rhs_rendered
  )
```

## Tests

新規・変更なし。

既存 tests を使用する。

## Phase boundary

- generic reflexive-equality display判定だけを修正
- equation numbering algorithm は変更しない
- proof graph は変更しない
- semantic dependency は変更しない
- Argument ordering は変更しない
- group-specific rule は追加しない
- repository-wide pytest は実行しない
