import inspect

import pytest

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReason,
  TodaGroupProofNarrativeReasonKind,
  TodaGroupProofNarrativeReasonSidecar,
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeDependencySemanticRole,
)


def _reason_data(
  n,
  k,
):
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )

  return (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  )


def test_phase150_rc4_4_pi6_definition_applicability_comes_from_typed_dependency():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _reason_data(
    3,
    3,
  )

  dependencies = tuple(
    dependency
    for dependency in semantic_sidecar.dependency_semantics
    if (
      dependency.role
      is TodaGroupProofNarrativeDependencySemanticRole
      .PRECONDITION_FOR_DEFINITION
    )
  )

  assert len(
    dependencies
  ) == 1

  definition_reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .DEFINITION_APPLICABILITY
    )
  )
  assert len(
    definition_reasons
  ) == 1

  dependency = dependencies[
    0
  ]
  reason = definition_reasons[
    0
  ]

  assert (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .DEFINITION_APPLICABILITY
  )
  assert reason.premise_steps == (
    dependency.prerequisite_step,
  )
  assert (
    reason.conclusion_step
    is dependency.dependent_step
  )
  assert (
    reason.owner_argument_index
    is None
  )


@pytest.mark.parametrize(
  "n,k",
  (
    (5, 3),
    (4, 6),
    (5, 7),
    (8, 7),
    (9, 7),
  ),
)
def test_phase150_rc4_4_other_representative_groups_do_not_invent_reasons(
  n,
  k,
):
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _reason_data(
    n,
    k,
  )

  expected_count = sum(
    1
    for dependency in semantic_sidecar.dependency_semantics
    if (
      dependency.role
      is TodaGroupProofNarrativeDependencySemanticRole
      .PRECONDITION_FOR_DEFINITION
    )
  )

  definition_reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .DEFINITION_APPLICABILITY
    )
  )

  assert len(
    definition_reasons
  ) == expected_count


def test_phase150_rc4_4_reason_sidecar_rejects_foreign_semantic_sidecar():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _reason_data(
    3,
    3,
  )
  (
    other_presentation,
    other_blocks,
    other_semantic_sidecar,
    other_arguments,
  ) = _method_evidence_data(
    5,
    3,
  )

  with pytest.raises(
    ValueError,
    match=(
      "semantic_sidecar must belong "
      "to presentation"
    ),
  ):
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      other_semantic_sidecar,
    )


def test_phase150_rc4_4_reason_rejects_empty_premises():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _reason_data(
    3,
    3,
  )

  reason = reason_sidecar.reasons[
    0
  ]

  with pytest.raises(
    ValueError,
    match=(
      "premise_steps must not be empty"
    ),
  ):
    TodaGroupProofNarrativeReason(
      kind=reason.kind,
      premise_steps=(),
      conclusion_step=reason.conclusion_step,
    )


def test_phase150_rc4_4_reason_sidecar_rejects_duplicate_relations():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _reason_data(
    3,
    3,
  )

  reason = reason_sidecar.reasons[
    0
  ]

  with pytest.raises(
    ValueError,
    match=(
      "reasons must not contain "
      "duplicate reason relations"
    ),
  ):
    TodaGroupProofNarrativeReasonSidecar(
      presentation=presentation,
      reasons=(
        reason,
        reason,
      ),
    )


def test_phase150_rc4_4_has_no_target_or_rendered_text_special_case():
  import toda_group_proof_narrative_reasons as module

  source = inspect.getsource(
    module
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
    "_render_generic_narrative_step",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
