import pytest

from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_relevance import (
  extract_toda_group_proof_narrative_exactness_component_terms,
  is_toda_group_proof_narrative_exactness_component_directly_relevant,
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


def _relevance_data(
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


def test_phase143_26_pi6_3_order_component_is_directly_relevant():
  relevant_groups, components = _relevance_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  assert len(
    components
  ) == 1
  assert is_toda_group_proof_narrative_exactness_component_directly_relevant(
    relevant_groups,
    components[
      0
    ],
  )


def test_phase143_26_pi6_3_group_structure_component_is_directly_relevant():
  relevant_groups, components = _relevance_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert len(
    components
  ) == 1
  assert is_toda_group_proof_narrative_exactness_component_directly_relevant(
    relevant_groups,
    components[
      0
    ],
  )


def test_phase143_26_pi8_5_group_structure_component_is_not_directly_relevant():
  relevant_groups, components = _relevance_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert components
  assert all(
    not is_toda_group_proof_narrative_exactness_component_directly_relevant(
      relevant_groups,
      component,
    )
    for component in components
  )


def test_phase143_26_pi16_9_definition_component_is_not_directly_relevant():
  relevant_groups, components = _relevance_data(
    9,
    7,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
  )

  assert relevant_groups == ()
  assert components
  assert all(
    not is_toda_group_proof_narrative_exactness_component_directly_relevant(
      relevant_groups,
      component,
    )
    for component in components
  )


def test_phase143_26_component_terms_are_unique_and_ordered():
  _relevant_groups, components = _relevance_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  terms = (
    extract_toda_group_proof_narrative_exactness_component_terms(
      components[
        0
      ]
    )
  )

  assert terms == (
    TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=3,
    ),
    TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=5,
    ),
    TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=2,
    ),
    TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=3,
    ),
    TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=5,
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
def test_phase143_26_four_targets_classify_safely(
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

    results = tuple(
      is_toda_group_proof_narrative_exactness_component_directly_relevant(
        relevant_groups,
        component,
      )
      for component in components
    )

    assert all(
      isinstance(
        result,
        bool,
      )
      for result in results
    )
