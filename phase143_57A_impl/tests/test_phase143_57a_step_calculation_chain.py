import pytest

from proof import (
  ProofStep,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_step_transitions import (
  TodaGroupProofNarrativeStepTransition,
  TodaGroupProofNarrativeStepTransitionRole,
  extract_toda_group_proof_narrative_step_transitions,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _step_transitions(
  n,
  k,
):
  (
    presentation,
    blocks,
    _sidecar,
    _arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  transitions = (
    extract_toda_group_proof_narrative_step_transitions(
      presentation,
      blocks,
    )
  )

  return (
    presentation,
    blocks,
    transitions,
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
def test_phase143_57a_four_targets_extract_safely(
  n,
  k,
):
  (
    _presentation,
    _blocks,
    transitions,
  ) = _step_transitions(
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
      TodaGroupProofNarrativeStepTransition,
    )
    for transition in transitions
  )
  assert all(
    transition.role
    is TodaGroupProofNarrativeStepTransitionRole
    .CALCULATION_CHAIN
    for transition in transitions
  )


def test_phase143_57a_pi6_3_has_step_level_calculation_chain():
  (
    _presentation,
    _blocks,
    transitions,
  ) = _step_transitions(
    3,
    3,
  )

  assert transitions


def test_phase143_57a_transitions_follow_direct_proof_edges():
  (
    presentation,
    _blocks,
    transitions,
  ) = _step_transitions(
    3,
    3,
  )

  direct_edge_keys = {
    (
      id(
        edge.premise_step
      ),
      id(
        edge.parent_step
      ),
    )
    for edge in presentation.edges
  }

  assert all(
    (
      id(
        transition.source_step
      ),
      id(
        transition.target_step
      ),
    )
    in direct_edge_keys
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
def test_phase143_57a_transitions_stay_inside_one_calculation_block(
  n,
  k,
):
  (
    _presentation,
    blocks,
    transitions,
  ) = _step_transitions(
    n,
    k,
  )

  block_by_step_id = {
    id(
      proof_step
    ): block
    for block in blocks
    for proof_step in block.steps
  }

  assert all(
    (
      block_by_step_id[
        id(
          transition.source_step
        )
      ]
      is block_by_step_id[
        id(
          transition.target_step
        )
      ]
    )
    for transition in transitions
  )
  assert all(
    block_by_step_id[
      id(
        transition.source_step
      )
    ].role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .CALCULATION
    for transition in transitions
  )


def test_phase143_57a_direction_is_premise_to_parent():
  (
    presentation,
    _blocks,
    transitions,
  ) = _step_transitions(
    3,
    3,
  )

  assert transitions

  for transition in transitions:
    matching_edges = tuple(
      edge
      for edge in presentation.edges
      if (
        edge.premise_step
        is transition.source_step
        and edge.parent_step
        is transition.target_step
      )
    )

    assert matching_edges


def test_phase143_57a_does_not_infer_non_edge_pairs():
  (
    presentation,
    blocks,
    transitions,
  ) = _step_transitions(
    3,
    3,
  )

  direct_edge_keys = {
    (
      id(
        edge.premise_step
      ),
      id(
        edge.parent_step
      ),
    )
    for edge in presentation.edges
  }
  transition_keys = {
    (
      id(
        transition.source_step
      ),
      id(
        transition.target_step
      ),
    )
    for transition in transitions
  }

  for block in blocks:
    if (
      block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole
      .CALCULATION
    ):
      continue

    for source_step in block.steps:
      for target_step in block.steps:
        if source_step is target_step:
          continue

        key = (
          id(
            source_step
          ),
          id(
            target_step
          ),
        )

        if key not in direct_edge_keys:
          assert key not in transition_keys


def test_phase143_57a_transition_validates_step_types():
  step = ProofStep(
    conclusion="source",
  )

  with pytest.raises(
    TypeError,
    match="target_step must be a ProofStep",
  ):
    TodaGroupProofNarrativeStepTransition(
      role=(
        TodaGroupProofNarrativeStepTransitionRole
        .CALCULATION_CHAIN
      ),
      source_step=step,
      target_step="target",
    )


def test_phase143_57a_rejects_non_tuple_blocks():
  (
    presentation,
    blocks,
    _sidecar,
    _arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  with pytest.raises(
    TypeError,
    match="blocks must be a tuple",
  ):
    extract_toda_group_proof_narrative_step_transitions(
      presentation,
      list(
        blocks
      ),
    )
