from toda_group_proof_aggregate_statement_catalog import (
  is_toda_group_proof_aggregate_statement,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _transition_data(
  n,
  k,
):
  (
    presentation,
    blocks,
    _sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )
  transitions = (
    extract_toda_group_proof_narrative_transitions(
      presentation,
      blocks,
      arguments,
    )
  )

  return (
    blocks,
    transitions,
  )


def test_phase143_53a_r_pi15_8_aggregate_source_is_derivation():
  (
    _blocks,
    transitions,
  ) = _transition_data(
    8,
    7,
  )

  target_transitions = tuple(
    transition
    for transition in transitions
    if (
      transition.target_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .TARGET
    )
  )

  assert len(
    target_transitions
  ) == 1

  transition = target_transitions[
    0
  ]

  assert (
    transition.role
    is TodaGroupProofNarrativeTransitionRole
    .DERIVATION
  )
  assert any(
    is_toda_group_proof_aggregate_statement(
      proof_step.conclusion
    )
    for block in transition.source_blocks
    for proof_step in block.steps
  )


def test_phase143_53a_r_pi6_3_precondition_definition_stays_support():
  (
    _blocks,
    transitions,
  ) = _transition_data(
    3,
    3,
  )

  definition_roles = tuple(
    transition.role
    for transition in transitions
    if (
      transition.target_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .DEFINITION
    )
  )

  assert definition_roles == (
    TodaGroupProofNarrativeTransitionRole
    .SUPPORT,
  )


def test_phase143_53a_r_pi16_9_aggregate_definition_stays_support():
  (
    _blocks,
    transitions,
  ) = _transition_data(
    9,
    7,
  )

  definition_transitions = tuple(
    transition
    for transition in transitions
    if (
      transition.target_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .DEFINITION
    )
  )

  assert len(
    definition_transitions
  ) == 1

  transition = definition_transitions[
    0
  ]

  assert (
    transition.role
    is TodaGroupProofNarrativeTransitionRole
    .SUPPORT
  )
  assert any(
    is_toda_group_proof_aggregate_statement(
      proof_step.conclusion
    )
    for block in transition.source_blocks
    for proof_step in block.steps
  )


def test_phase143_53a_r_all_four_targets_have_derivation():
  for n, k in (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ):
    (
      _blocks,
      transitions,
    ) = _transition_data(
      n,
      k,
    )

    target_roles = tuple(
      transition.role
      for transition in transitions
      if (
        transition.target_block.role
        is TodaGroupProofNarrativeMathematicalBlockRole
        .TARGET
      )
    )

    assert (
      TodaGroupProofNarrativeTransitionRole
      .DERIVATION
      in target_roles
    )
