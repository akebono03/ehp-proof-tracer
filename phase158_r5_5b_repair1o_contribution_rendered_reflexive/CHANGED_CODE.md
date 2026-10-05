# Phase 158-R5-5b repair1o changed code

## 変更対象

`toda_group_proof_narrative_contribution_renderer.py`

### 変更後 import 部分

```python
from collections import deque
from dataclasses import (
  fields,
  is_dataclass,
  replace,
)

from expression import (
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)

from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_group_proof_generic_narrative_renderer import (
  _generic_short_exact_sequence_latex,
  _generic_short_exact_sequence_reason_prose,
  _render_generic_narrative_step,
)
from toda_human_readable_renderer import (
  _render_scalar_latex,
  render_toda_expression_latex,
)
from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_renderer import (
  render_toda_group_proof_narrative_argument_purpose_sentence,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
)
from toda_group_proof_narrative_contribution_ordering import (
  TodaGroupProofNarrativeContributionPlacement,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_hidden_bridge_semantics import (
  TodaGroupProofNarrativeHiddenBridgeOperationKind,
  TodaGroupProofNarrativeHiddenBridgeSemanticRole,
  build_toda_group_proof_narrative_hidden_bridge_semantics,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_reason_renderer import (
  insert_toda_group_proof_narrative_reason_prose,
  order_toda_group_proof_narrative_injective_image_order_reason,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  extract_toda_group_proof_step_literature_reference,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  filter_toda_group_proof_narrative_reference_entries_by_step_usage,
  restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage,
  render_toda_group_proof_narrative_reference_entries_markdown,
  select_toda_group_proof_narrative_reference_statement_steps,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeDependencySemanticRole,
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
)
from toda_proof_dependency import (
  TodaProofDependencyRole,
  classify_toda_proof_step_role,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
)
```

### 変更関数全文

```python
def suppress_toda_group_proof_narrative_reflexive_equalities(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  reflexive_keys = set()

  for node in presentation.nodes:
    statement = node.proof_step.conclusion

    if (
      not isinstance(
        statement,
        Relation,
      )
      or statement.relation_type
      is not RelationType.EQUALITY
    ):
      continue

    try:
      rendered = (
        _render_generic_narrative_step(
          node.proof_step
        )
      )
    except (
      TypeError,
      ValueError,
    ):
      continue

    if (
      not rendered.startswith(
        "$"
      )
      or not rendered.endswith(
        "$"
      )
    ):
      continue

    equation = rendered[
      1:-1
    ]
    separator = " = "

    if separator not in equation:
      continue

    lhs_rendered, rhs_rendered = equation.split(
      separator,
      1,
    )

    if (
      lhs_rendered
      != rhs_rendered
    ):
      continue

    reflexive_keys.add(
      _phase157_r11_reference_statement_match_key(
        rendered
      )
    )

  if not reflexive_keys:
    return markdown

  retained = []

  for paragraph in markdown.split(
    "\n\n"
  ):
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]より, "
      )

      if marker_end >= 0:
        stripped = stripped[
          marker_end
          + len(
            "]より, "
          ):
        ]

    key = (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

    if key in reflexive_keys:
      continue

    retained.append(
      paragraph
    )

  return "\n\n".join(
    retained
  )
```

## Tests

新規・変更なし。

## Phase boundary

- contribution-level reflexive suppression のみ修正
- equation numbering algorithm は変更しない
- proof graph / semantic closure は変更しない
- Argument ordering は変更しない
- group-specific rule は追加しない
- repository-wide pytest は実行しない
