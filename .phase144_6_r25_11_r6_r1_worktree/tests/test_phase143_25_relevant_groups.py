import pytest

from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _relevant_groups(
  n,
  k,
  role,
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

  argument = next(
    argument
    for argument in arguments
    if argument.role is role
  )

  return (
    extract_toda_group_proof_narrative_argument_relevant_groups(
      presentation,
      blocks,
      argument,
    )
  )


def test_phase143_25_pi6_3_group_structure_relevant_group_is_target():
  groups = _relevant_groups(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert groups == (
    TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=3,
    ),
  )


def test_phase143_25_pi6_3_order_subject_membership_gives_pi6_3():
  groups = _relevant_groups(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  assert TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  ) in groups


@pytest.mark.parametrize(
  "n,k",
  (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ),
)
def test_phase143_25_group_structure_relevant_group_is_target(
  n,
  k,
):
  groups = _relevant_groups(
    n,
    k,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert groups == (
    TodaPrimaryGroup(
      group_dimension=n + k,
      sphere_dimension=n,
    ),
  )


def test_phase143_25_pi8_5_definition_returns_tuple():
  groups = _relevant_groups(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
  )

  assert isinstance(
    groups,
    tuple,
  )


def test_phase143_25_pi16_9_definition_returns_tuple():
  groups = _relevant_groups(
    9,
    7,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
  )

  assert isinstance(
    groups,
    tuple,
  )


def test_phase143_25_rejects_non_tuple_blocks():
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
    match="blocks must be a tuple",
  ):
    extract_toda_group_proof_narrative_argument_relevant_groups(
      presentation,
      list(
        blocks
      ),
      arguments[
        0
      ],
    )
