import pytest

from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_method_renderer import (
  render_toda_group_proof_narrative_exactness_method_transition,
)
from toda_group_proof_narrative_exactness_selection import (
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


def _transition_data(
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

  matches = tuple(
    (
      argument_index,
      argument,
    )
    for argument_index, argument in enumerate(
      arguments
    )
    if argument.role is role
  )
  argument_index, argument = matches[
    occurrence
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
  primary_component = (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )

  return (
    primary_component,
    render_toda_group_proof_narrative_exactness_method_transition(
      primary_component
    ),
  )


def test_phase143_30_pi6_3_order_renders_exactness_transition():
  primary_component, transition = _transition_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  assert primary_component is not None
  assert transition == (
    "そのために、次の完全列を考える."
  )


def test_phase143_30_pi6_3_group_structure_renders_exactness_transition():
  primary_component, transition = _transition_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert primary_component is not None
  assert transition == (
    "そのために、次の完全列を考える."
  )


def test_phase143_30_pi6_3_definition_has_no_transition():
  primary_component, transition = _transition_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
  )

  assert primary_component is None
  assert transition is None


def test_phase143_30_pi8_5_group_structure_has_no_transition():
  primary_component, transition = _transition_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert primary_component is None
  assert transition is None


def test_phase143_30_pi8_5_detached_nu_prime_order_renders_transition():
  primary_component, transition = _transition_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
    occurrence=1,
  )

  assert primary_component is not None
  assert transition == (
    "そのために、次の完全列を考える."
  )


def test_phase143_30_pi15_8_group_structure_has_no_transition():
  primary_component, transition = _transition_data(
    8,
    7,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert primary_component is None
  assert transition is None


def test_phase143_30_pi16_9_group_structure_has_no_transition():
  primary_component, transition = _transition_data(
    9,
    7,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert primary_component is None
  assert transition is None


def test_phase143_30_none_renders_no_transition():
  assert (
    render_toda_group_proof_narrative_exactness_method_transition(
      None
    )
    is None
  )


def test_phase143_30_rejects_non_component():
  with pytest.raises(
    TypeError,
    match=(
      "primary_component must be a "
      "TodaGroupProofNarrativeExactnessMethodComponent "
      "or None"
    ),
  ):
    render_toda_group_proof_narrative_exactness_method_transition(
      object()
    )
