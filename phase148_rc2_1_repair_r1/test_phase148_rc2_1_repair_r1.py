from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_contribution_ownership import (
  filter_toda_group_proof_narrative_exactness_body_contributions,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_argument_primary_exactness_component,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _argument_index_for_role(
  arguments,
  role,
  occurrence=0,
):
  matches = tuple(
    index
    for index, argument in enumerate(arguments)
    if argument.role is role
  )
  return matches[occurrence]


def _argument_exactness_data(
  n,
  k,
  role,
  occurrence=0,
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
  argument_index = _argument_index_for_role(
    arguments,
    role,
    occurrence,
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
  primary = (
    select_toda_group_proof_narrative_argument_primary_exactness_component(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )

  return (
    presentation,
    blocks,
    evidence,
    components,
    primary,
  )


def test_phase148_rc2_1_pi6_3_order_exactness_is_one_owned_component():
  (
    _presentation,
    _blocks,
    evidence,
    components,
    primary,
  ) = _argument_exactness_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  assert len(evidence) == 2
  assert len(components) == 1
  assert primary == components[0]


def test_phase148_rc2_1_pi6_3_group_structure_exactness_is_one_owned_component():
  (
    _presentation,
    _blocks,
    evidence,
    components,
    primary,
  ) = _argument_exactness_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert len(evidence) == 3
  assert len(components) == 1
  assert primary == components[0]


def test_phase148_rc2_1_pi8_5_group_structure_has_unowned_visible_recursive_evidence():
  (
    presentation,
    _blocks,
    evidence,
    components,
    primary,
  ) = _argument_exactness_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert len(evidence) == 2
  assert len(components) == 1
  assert primary is None

  visible = tuple(
    contribution
    for block in evidence
    for contribution in (
      filter_toda_group_proof_narrative_exactness_body_contributions(
        block,
        extract_toda_group_proof_narrative_exactness_display_contributions(
          presentation,
          block,
        ),
        primary,
      )
    )
  )

  assert visible


def test_phase148_rc2_1_pi12_5_definition_has_unowned_visible_recursive_evidence():
  (
    presentation,
    _blocks,
    evidence,
    components,
    primary,
  ) = _argument_exactness_data(
    5,
    7,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
  )

  assert len(evidence) == 2
  assert len(components) == 1
  assert primary is None

  visible = tuple(
    contribution
    for block in evidence
    for contribution in (
      filter_toda_group_proof_narrative_exactness_body_contributions(
        block,
        extract_toda_group_proof_narrative_exactness_display_contributions(
          presentation,
          block,
        ),
        primary,
      )
    )
  )

  assert visible
