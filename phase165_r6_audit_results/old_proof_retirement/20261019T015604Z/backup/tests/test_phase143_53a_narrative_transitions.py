import pytest

from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransition,
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _transitions(
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

  return (
    presentation,
    blocks,
    arguments,
    extract_toda_group_proof_narrative_transitions(
      presentation,
      blocks,
      arguments,
    ),
  )


@pytest.mark.parametrize(
  "n,k",
  (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ),
)
def test_phase143_53a_four_targets_extract_transitions_safely(
  n,
  k,
):
  (
    _presentation,
    _blocks,
    _arguments,
    transitions,
  ) = _transitions(
    n,
    k,
  )

  assert isinstance(
    transitions,
    tuple,
  )
  assert all(
    isinstance(
      transition,
      TodaGroupProofNarrativeTransition,
    )
    for transition in transitions
  )
  assert all(
    transition.source_blocks
    for transition in transitions
  )


@pytest.mark.parametrize(
  "n,k",
  (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ),
)
def test_phase143_53a_argument_transitions_target_argument_conclusions(
  n,
  k,
):
  (
    _presentation,
    _blocks,
    arguments,
    transitions,
  ) = _transitions(
    n,
    k,
  )

  conclusion_ids = {
    id(
      argument.conclusion_block
    )
    for argument in arguments
  }

  argument_transitions = tuple(
    transition
    for transition in transitions
    if (
      transition.role
      in (
        TodaGroupProofNarrativeTransitionRole.SUPPORT,
        TodaGroupProofNarrativeTransitionRole.DERIVATION,
      )
    )
  )

  assert all(
    id(
      transition.target_block
    )
    in conclusion_ids
    for transition in argument_transitions
  )


def test_phase143_53a_pi6_3_has_derivation_to_target():
  (
    _presentation,
    _blocks,
    _arguments,
    transitions,
  ) = _transitions(
    3,
    3,
  )

  assert any(
    (
      transition.role
      is TodaGroupProofNarrativeTransitionRole
      .DERIVATION
      and transition.target_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .TARGET
    )
    for transition in transitions
  )


def test_phase143_53a_pi8_5_has_derivation_to_target():
  (
    _presentation,
    _blocks,
    _arguments,
    transitions,
  ) = _transitions(
    5,
    3,
  )

  assert any(
    (
      transition.role
      is TodaGroupProofNarrativeTransitionRole
      .DERIVATION
      and transition.target_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .TARGET
    )
    for transition in transitions
  )


def test_phase143_53a_does_not_mutate_narrative_objects():
  (
    presentation,
    blocks,
    _sidecar,
    arguments,
  ) = _method_evidence_data(
    9,
    7,
  )

  block_snapshot = tuple(
    (
      block.role,
      tuple(
        id(
          step
        )
        for step in block.steps
      ),
    )
    for block in blocks
  )
  argument_snapshot = tuple(
    (
      argument.role,
      tuple(
        id(
          block
        )
        for block in argument.supporting_blocks
      ),
      id(
        argument.conclusion_block
      ),
      argument.child_argument_indices,
    )
    for argument in arguments
  )

  extract_toda_group_proof_narrative_transitions(
    presentation,
    blocks,
    arguments,
  )

  assert block_snapshot == tuple(
    (
      block.role,
      tuple(
        id(
          step
        )
        for step in block.steps
      ),
    )
    for block in blocks
  )
  assert argument_snapshot == tuple(
    (
      argument.role,
      tuple(
        id(
          block
        )
        for block in argument.supporting_blocks
      ),
      id(
        argument.conclusion_block
      ),
      argument.child_argument_indices,
    )
    for argument in arguments
  )


def test_phase143_53a_rejects_non_tuple_arguments():
  (
    presentation,
    blocks,
    _sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  with pytest.raises(
    TypeError,
    match="arguments must be a tuple",
  ):
    extract_toda_group_proof_narrative_transitions(
      presentation,
      blocks,
      list(
        arguments
      ),
    )
