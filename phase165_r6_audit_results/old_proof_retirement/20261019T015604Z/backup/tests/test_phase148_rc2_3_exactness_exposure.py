from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_exposure import (
  TodaGroupProofNarrativeExactnessExposureClass,
  classify_toda_group_proof_narrative_exactness_component_exposure,
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


def _argument_exposure_data(
  n,
  k,
  role,
  occurrence=0,
):
  presentation, blocks, sidecar, arguments = (
    _method_evidence_data(
      n,
      k,
    )
  )
  matches = tuple(
    index
    for index, argument in enumerate(
      arguments
    )
    if argument.role is role
  )
  argument_index = matches[
    occurrence
  ]
  argument = arguments[
    argument_index
  ]
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
  relevant_groups = (
    extract_toda_group_proof_narrative_argument_relevant_groups(
      presentation,
      blocks,
      argument,
    )
  )
  exposures = tuple(
    classify_toda_group_proof_narrative_exactness_component_exposure(
      relevant_groups,
      components,
      component,
    )
    for component in components
  )
  return (
    presentation,
    blocks,
    sidecar,
    arguments,
    components,
    exposures,
  )


def _render(
  n,
  k,
):
  presentation, blocks, sidecar, arguments = (
    _method_evidence_data(
      n,
      k,
    )
  )
  return (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )


def test_phase148_rc2_3_pi6_3_group_structure_is_owned_primary():
  *_, components, exposures = _argument_exposure_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )
  assert len(components) == 1
  assert exposures == (
    TodaGroupProofNarrativeExactnessExposureClass
    .OWNED_PRIMARY,
  )


def test_phase148_rc2_3_pi8_5_group_structure_is_unowned_recursive():
  *_, components, exposures = _argument_exposure_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )
  assert len(components) == 1
  assert exposures == (
    TodaGroupProofNarrativeExactnessExposureClass
    .UNOWNED_RECURSIVE,
  )


def test_phase148_rc2_3_pi12_5_definition_is_unowned_recursive():
  *_, components, exposures = _argument_exposure_data(
    5,
    7,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
  )
  assert len(components) == 1
  assert exposures == (
    TodaGroupProofNarrativeExactnessExposureClass
    .UNOWNED_RECURSIVE,
  )


def test_phase148_rc2_3_ambiguous_relevant_class_is_conservative():
  *_, components, _exposures = _argument_exposure_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )
  component = components[
    0
  ]
  relevant_group = component.windows[
    0
  ].middle_term
  assert isinstance(
    relevant_group,
    TodaPrimaryGroup,
  )
  assert (
    classify_toda_group_proof_narrative_exactness_component_exposure(
      (
        relevant_group,
      ),
      (
        component,
        component,
      ),
      component,
    )
    is TodaGroupProofNarrativeExactnessExposureClass
    .AMBIGUOUS_RELEVANT
  )
