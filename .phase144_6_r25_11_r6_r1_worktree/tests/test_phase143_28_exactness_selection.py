import pytest

from homotopy_groups import (
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_E_MAP,
  EHP_H_MAP,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_exactness_components import (
  TodaGroupProofNarrativeExactnessMethodComponent,
  build_toda_group_proof_narrative_exactness_method_components,
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


def _selection_data(
  n,
  k,
  role,
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

  argument_index = next(
    index
    for index, argument in enumerate(
      arguments
    )
    if argument.role is role
  )
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
    relevant_groups,
    components,
  )


def test_phase143_28_pi6_3_order_selects_unique_primary_component():
  relevant_groups, components = _selection_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  selected = (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )

  assert len(
    components
  ) == 1
  assert selected is components[
    0
  ]


def test_phase143_28_pi6_3_group_structure_selects_unique_primary_component():
  relevant_groups, components = _selection_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  selected = (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )

  assert len(
    components
  ) == 1
  assert selected is components[
    0
  ]


def test_phase143_28_pi8_5_group_structure_has_no_primary_component():
  relevant_groups, components = _selection_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert components
  assert (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
    is None
  )


def test_phase143_28_pi16_9_definition_has_no_primary_component():
  relevant_groups, components = _selection_data(
    9,
    7,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
  )

  assert components
  assert relevant_groups == ()
  assert (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
    is None
  )


def test_phase143_28_multiple_directly_relevant_components_are_ambiguous():
  relevant_group = TodaPrimaryGroup(
    group_dimension=2,
    sphere_dimension=2,
  )
  left_group = TodaPrimaryGroup(
    group_dimension=1,
    sphere_dimension=1,
  )
  right_group = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )
  other_left_group = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=4,
  )
  other_right_group = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )

  first_window = TodaEHPExactnessWindow(
    source_term=left_group,
    middle_term=relevant_group,
    target_term=right_group,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )
  second_window = TodaEHPExactnessWindow(
    source_term=other_left_group,
    middle_term=relevant_group,
    target_term=other_right_group,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )

  (
    _presentation,
    blocks,
    _sidecar,
    _arguments,
  ) = _method_evidence_data(
    3,
    3,
  )
  exactness_blocks = tuple(
    block
    for block in blocks
    if block.steps
    and any(
      proof_step.conclusion.__class__.__name__
      == "TodaProp42ExactnessStatement"
      for proof_step in block.steps
    )
  )

  first_component = (
    TodaGroupProofNarrativeExactnessMethodComponent(
      windows=(
        first_window,
      ),
      evidence_blocks=(
        exactness_blocks[
          0
        ],
      ),
    )
  )
  second_component = (
    TodaGroupProofNarrativeExactnessMethodComponent(
      windows=(
        second_window,
      ),
      evidence_blocks=(
        exactness_blocks[
          0
        ],
      ),
    )
  )

  assert (
    select_toda_group_proof_narrative_primary_exactness_component(
      (
        relevant_group,
      ),
      (
        first_component,
        second_component,
      ),
    )
    is None
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
def test_phase143_28_four_targets_select_safely(
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

  for argument_index, argument in enumerate(
    arguments
  ):
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
    selected = (
      select_toda_group_proof_narrative_primary_exactness_component(
        relevant_groups,
        components,
      )
    )

    assert (
      selected is None
      or selected in components
    )


def test_phase143_28_rejects_non_tuple_components():
  with pytest.raises(
    TypeError,
    match="components must be a tuple",
  ):
    select_toda_group_proof_narrative_primary_exactness_component(
      (),
      [],
    )
