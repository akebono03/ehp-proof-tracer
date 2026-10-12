# Phase 164 R8-R6 変更コード全文

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
def annotate_derived_reference_step(step: ProofStep, reference) -> ProofStep:
    """Preserve an inferred step's ancestry while attaching known citation identity.

    A reference label alone does not certify a statement's mathematical truth.
    """
    from dataclasses import replace
    from proof import FoundationalReferenceIdentity
    if not isinstance(step, ProofStep) or step.rule is not ProofRule.INFERENCE:
        raise TypeError("step must be an inferred ProofStep")
    if not isinstance(reference, FoundationalReferenceIdentity):
        raise TypeError("reference must be a FoundationalReferenceIdentity")
    if step.foundational_reference is not None and step.foundational_reference != reference:
        raise ValueError("cannot overwrite another foundational reference")
    return replace(step, foundational_reference=reference)
```

```python
def project_reference_component_step(source_step: ProofStep, component) -> ProofStep:
    """Create a display-only projection without promoting its evidence status.

    This is NOT an inference and must never be inserted as a proof-tree node.
    """
    if not isinstance(source_step, ProofStep):
        raise TypeError("source_step must be a ProofStep")
    return ProofStep(
        conclusion=component,
        premises=(),
        rule=source_step.rule,
        note=source_step.note,
        inference_rule=source_step.inference_rule,
    )
```

## phase162_reference_boundary.py

### import 全文

```python
from __future__ import annotations
from dataclasses import replace
from proof import (
    FoundationalReferenceIdentity, InferenceRule, LiteratureReference,
    PremisePattern, ProofRule, ProofStep, apply_inference_match,
    find_inference_match,
)
from phase161_r7_premise_provenance_validation import validate_phase161_r7_provenance
from toda_literature_statement_boundary import get_toda_fixed_statement_component
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    derive_inference_proof_step,
)
from phase164_r8_proofstep_factory import (
    annotate_derived_reference_step,
)
```

### 変更した関数全文

```python
def cite_verified_fixed_statement(
    witness: ProofStep,
    reference_locator: str,
    component_key: str,
    expected_conclusion: object,
) -> ProofStep:
    """Collapse verified ancestry at a registered citation boundary.

    The caller must identify the exact fixed statement and pass the mathematical
    conclusion it claims. A registered component is necessary, not sufficient,
    to establish the external truth of that mathematical citation.
    """
    if not isinstance(witness, ProofStep):
        raise TypeError("witness must be a ProofStep")
    if witness.rule is not ProofRule.INFERENCE or not witness.premises:
        raise ValueError("Citation witness must be a derived inference")
    if witness.conclusion != expected_conclusion:
        raise ValueError("Citation statement does not match verified witness")
    component = get_toda_fixed_statement_component(reference_locator, component_key)
    if component.reference_locator != reference_locator or component.component_key != component_key:
        raise ValueError("Registered component mismatch")
    validate_phase161_r7_provenance((witness,), _trusted_given_ancestors(witness))
    citation_identity = FoundationalReferenceIdentity(
        key=f"literature:{reference_locator}:{component_key}",
        label=reference_locator,
    )
    citation_leaf = create_legacy_given_proof_step(
        conclusion=witness.conclusion,
        premises=(),
        rule=ProofRule.GIVEN,
        foundational_reference=citation_identity,
    )
    citation_rule = InferenceRule(
        name="phase162_verified_literature_citation",
        description="Use a verified fixed literature statement",
        premise_patterns=(PremisePattern(proof_rule=ProofRule.GIVEN),),
        match_guard=lambda premises, bindings=(): (
            len(premises) == 1
            and premises[0].foundational_reference == citation_identity
            and premises[0].conclusion == expected_conclusion
        ),
        conclusion_builder=lambda premises: premises[0].conclusion,
        literature_reference=LiteratureReference(
            label="Toda " + reference_locator,
            locator=reference_locator,
        ),
    )
    match = find_inference_match(citation_rule, (citation_leaf,))
    if match is None:
        raise ValueError("Citation inference failed to match the trusted leaf")
    result = derive_inference_proof_step(match)
    return annotate_derived_reference_step(result, citation_identity)
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
```

### 変更した関数全文

```python
def _phase153_r6_render_reference_statement(
  presentation: TodaGroupProofPresentation,
  entry,
  proof_step: ProofStep,
  rendered_statement: str,
) -> str:
  boundary = (
    classify_toda_literature_statement_step(
      proof_step
    )
  )

  if (
    boundary is not None
    and boundary.classification
    is TodaLiteratureStatementClassification.FIXED_STATEMENT
    and boundary.reference_locator
    == "Proposition 2.2"
    and boundary.component_key
    == "hopf_right_composition_formula"
  ):
    return (
      r"$H(lpha\circ Eeta) = "
      r"H(lpha)\circ Eeta$."
    )

  component = (
    _phase153_r6_reference_aggregate_component(
      presentation,
      entry,
      proof_step,
    )
  )

  if component is None:
    return rendered_statement

  component_step = project_reference_component_step(
    proof_step, component
  )

  return _render_generic_narrative_step(
    component_step
  )
```

