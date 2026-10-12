# Phase 164 R8-R7 変更コード全文

## phase164_r8_proofstep_factory.py

### import 全文

```python
from proof import (
    InferenceMatch,
    ProofRule,
    ProofStep,
    Relation,
    apply_inference_match,
    relation_proof_step,
)
```

### 変更した関数全文

```python
def replace_legacy_proof_step_fields(step: ProofStep, **changes) -> ProofStep:
    """Route a legacy dataclass projection through the common factory.

    This retains the old rule and provenance status. It does not validate a
    substituted conclusion and must not be used to claim a new inference.
    """
    from dataclasses import fields, replace
    if not isinstance(step, ProofStep):
        raise TypeError("step must be a ProofStep")
    allowed = {field.name for field in fields(ProofStep)}
    if not set(changes).issubset(allowed):
        raise TypeError("unknown ProofStep field")
    if "rule" in changes and changes["rule"] is not step.rule:
        raise ValueError("legacy projection must preserve proof rule")
    return replace(step, **changes)
```

## toda_group_proof_narrative_contribution_renderer.py

### import 全文

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
  TodaPrimaryGroupZeroStatement,
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
  get_toda_fixed_statement_component,
)
from phase164_r8_proofstep_factory import (
    project_reference_component_step,
)
from phase164_r8_proofstep_factory import (
    replace_legacy_proof_step_fields,
)
```

### 変更した関数全文

```python
def _phase157_r20_specialize_reference_value(
  value,
  symbol,
  binding: int,
):
  if isinstance(
    value,
    ScalarSymbol,
  ):
    if value == symbol:
      return binding

    return value

  if isinstance(
    value,
    ScalarSum,
  ):
    left = (
      _phase157_r20_specialize_reference_value(
        value.left,
        symbol,
        binding,
      )
    )
    right = (
      _phase157_r20_specialize_reference_value(
        value.right,
        symbol,
        binding,
      )
    )

    if (
      isinstance(
        left,
        int,
      )
      and isinstance(
        right,
        int,
      )
    ):
      return left + right

    return replace(
      value,
      left=left,
      right=right,
    )

  if isinstance(
    value,
    tuple,
  ):
    return tuple(
      _phase157_r20_specialize_reference_value(
        item,
        symbol,
        binding,
      )
      for item in value
    )

  if isinstance(
    value,
    list,
  ):
    return [
      _phase157_r20_specialize_reference_value(
        item,
        symbol,
        binding,
      )
      for item in value
    ]

  if isinstance(
    value,
    dict,
  ):
    return {
      key: (
        _phase157_r20_specialize_reference_value(
          item,
          symbol,
          binding,
        )
      )
      for key, item in value.items()
    }

  if not is_dataclass(
    value
  ):
    return value

  changes = {}

  for field in fields(
    value
  ):
    if not field.init:
      continue

    original = getattr(
      value,
      field.name,
    )
    specialized = (
      _phase157_r20_specialize_reference_value(
        original,
        symbol,
        binding,
      )
    )

    if specialized != original:
      changes[
        field.name
      ] = specialized

  if not changes:
    return value

  if isinstance(value, ProofStep):
    return replace_legacy_proof_step_fields(value, **changes)

  return replace(
    value,
    **changes,
  )
```
