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
):
  return next(
    index
    for index, argument in enumerate(arguments)
    if argument.role is role
  )


def test_phase148_rc2_1_pi6_3_exposes_non_primary_recursive_exactness_today():
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

  assert primary is not None
  non_primary_blocks = tuple(
    block
    for component in components
    if component != primary
    for block in component.evidence_blocks
  )
  assert non_primary_blocks

  assert any(
    filter_toda_group_proof_narrative_exactness_body_contributions(
      block,
      extract_toda_group_proof_narrative_exactness_display_contributions(
        presentation,
        block,
      ),
      primary,
    )
    for block in non_primary_blocks
  )


def test_phase148_rc2_1_pi6_3_primary_and_recursive_components_are_distinct():
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

  assert primary in components
  assert any(
    component != primary
    for component in components
  )
