import pytest

from homotopy_groups import (
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _components_for_argument(
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

  evidence = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )

  return (
    build_toda_group_proof_narrative_exactness_method_components(
      evidence
    )
  )


def test_phase143_22_pi6_3_order_exactness_is_one_component():
  components = _components_for_argument(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  assert len(
    components
  ) == 1
  assert len(
    components[
      0
    ].windows
  ) >= 2


def test_phase143_22_pi6_3_component_windows_are_structurally_adjacent():
  component = _components_for_argument(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )[
    0
  ]

  for left, right in zip(
    component.windows,
    component.windows[
      1:
    ],
  ):
    assert (
      left.middle_term
      == right.source_term
    )
    assert (
      left.target_term
      == right.middle_term
    )
    assert (
      left.second_map
      == right.first_map
    )


def test_phase143_22_connects_windows_by_terms_and_map():
  a = TodaPrimaryGroup(
    group_dimension=1,
    sphere_dimension=1,
  )
  b = TodaPrimaryGroup(
    group_dimension=2,
    sphere_dimension=2,
  )
  c = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )
  d = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=4,
  )

  left = TodaEHPExactnessWindow(
    source_term=a,
    middle_term=b,
    target_term=c,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )
  right = TodaEHPExactnessWindow(
    source_term=b,
    middle_term=c,
    target_term=d,
    first_map=EHP_H_MAP,
    second_map=EHP_DELTA_MAP,
  )

  assert (
    left.middle_term
    == right.source_term
  )
  assert (
    left.target_term
    == right.middle_term
  )
  assert (
    left.second_map
    == right.first_map
  )


def test_phase143_22_does_not_connect_on_terms_without_map_match():
  a = TodaPrimaryGroup(
    group_dimension=1,
    sphere_dimension=1,
  )
  b = TodaPrimaryGroup(
    group_dimension=2,
    sphere_dimension=2,
  )
  c = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )
  d = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=4,
  )

  left = TodaEHPExactnessWindow(
    source_term=a,
    middle_term=b,
    target_term=c,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )
  right = TodaEHPExactnessWindow(
    source_term=b,
    middle_term=c,
    target_term=d,
    first_map=EHP_DELTA_MAP,
    second_map=EHP_E_MAP,
  )

  assert (
    left.middle_term
    == right.source_term
  )
  assert (
    left.target_term
    == right.middle_term
  )
  assert (
    left.second_map
    != right.first_map
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
def test_phase143_22_four_targets_build_components_safely(
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

    assert isinstance(
      components,
      tuple,
    )
    assert all(
      component.windows
      for component in components
    )
