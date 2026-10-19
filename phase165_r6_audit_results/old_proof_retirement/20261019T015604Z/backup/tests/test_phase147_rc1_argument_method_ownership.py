import pytest

from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_argument_primary_exactness_component,
  select_toda_group_proof_narrative_primary_exactness_component,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _argument_index_for_role(
  arguments,
  role,
):
  return next(
    argument_index
    for argument_index, argument in enumerate(
      arguments
    )
    if argument.role is role
  )


def _legacy_primary_component(
  presentation,
  blocks,
  sidecar,
  arguments,
  argument_index,
):
  argument = arguments[
    argument_index
  ]
  relevant_groups = (
    extract_toda_group_proof_narrative_argument_relevant_groups(
      presentation,
      blocks,
      argument,
    )
  )
  evidence = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )
  components = (
    build_toda_group_proof_narrative_exactness_method_components(
      evidence
    )
  )

  return (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )


def test_phase147_rc1_3_pi6_3_order_owns_primary_exactness_component():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )
  argument_index = _argument_index_for_role(
    arguments,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  selected = (
    select_toda_group_proof_narrative_argument_primary_exactness_component(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )

  assert selected is not None


def test_phase147_rc1_3_pi6_3_group_structure_owns_primary_exactness_component():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )
  argument_index = _argument_index_for_role(
    arguments,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  selected = (
    select_toda_group_proof_narrative_argument_primary_exactness_component(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )

  assert selected is not None


def test_phase147_rc1_3_pi8_5_group_structure_has_no_owned_primary_component():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    5,
    3,
  )
  argument_index = _argument_index_for_role(
    arguments,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  selected = (
    select_toda_group_proof_narrative_argument_primary_exactness_component(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )

  assert selected is None


@pytest.mark.parametrize(
  "n,k",
  (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ),
)
def test_phase147_rc1_3_ownership_matches_existing_selection_pipeline(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  for argument_index in range(
    len(
      arguments
    )
  ):
    expected = _legacy_primary_component(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
    actual = (
      select_toda_group_proof_narrative_argument_primary_exactness_component(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )

    assert actual == expected


def test_phase147_rc1_3_ownership_reuses_existing_argument_index_validation():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  with pytest.raises(
    ValueError,
    match="argument_index is out of range",
  ):
    select_toda_group_proof_narrative_argument_primary_exactness_component(
      presentation,
      blocks,
      sidecar,
      arguments,
      len(
        arguments
      ),
    )
