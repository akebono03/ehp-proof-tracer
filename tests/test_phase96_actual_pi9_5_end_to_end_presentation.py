import pytest

from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
  get_single_candidate,
)
from toda_end_to_end_presentation import (
  TodaEndToEndCandidatePresentation,
  build_toda_end_to_end_candidate_presentation,
)
from toda_presentation import (
  TodaGeneratorOrderKind,
  TodaGroupStructureKind,
)


def build_phase96_7_actual_pi9_5_presentation():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  presentation = (
    build_toda_end_to_end_candidate_presentation(
      candidate,
      data[
        "repository"
      ].entries(),
    )
  )

  return {
    "data": data,
    "candidate": candidate,
    "presentation": presentation,
  }


def test_phase96_7_actual_pi9_5_builds_end_to_end_presentation():
  actual = (
    build_phase96_7_actual_pi9_5_presentation()
  )

  presentation = actual[
    "presentation"
  ]

  assert isinstance(
    presentation,
    TodaEndToEndCandidatePresentation,
  )
  assert (
    presentation.source_candidate
    is actual[
      "candidate"
    ]
  )


def test_phase96_7_actual_pi9_5_preserves_calculation_candidate_identity():
  actual = (
    build_phase96_7_actual_pi9_5_presentation()
  )

  presentation = actual[
    "presentation"
  ]

  assert (
    presentation
    .calculation_candidate
    .source_candidate
    is actual[
      "candidate"
    ]
  )


def test_phase96_7_actual_pi9_5_integrates_target_group_generator_and_order():
  actual = (
    build_phase96_7_actual_pi9_5_presentation()
  )

  candidate = actual[
    "candidate"
  ]
  presentation = actual[
    "presentation"
  ]

  assert (
    presentation
    .group
    .source_group_result
    is candidate.group_result
  )

  assert (
    presentation
    .group
    .target
    .group_dimension
    == 9
  )
  assert (
    presentation
    .group
    .target
    .sphere_dimension
    == 5
  )

  assert (
    presentation
    .group
    .group_structure
    .kind
    is TodaGroupStructureKind.FINITE_CYCLIC
  )

  assert len(
    presentation
    .group
    .generators
  ) == 1

  assert (
    presentation
    .group
    .generators[
      0
    ].source_generator
    is candidate
    .group_result
    .generators[
      0
    ]
  )

  assert (
    presentation
    .group
    .generators[
      0
    ].order.kind
    is TodaGeneratorOrderKind.FINITE
  )
  assert (
    presentation
    .group
    .generators[
      0
    ].order.value
    == 2
  )


def test_phase96_7_actual_pi9_5_integrates_actual_ehp_chain():
  actual = (
    build_phase96_7_actual_pi9_5_presentation()
  )

  candidate = actual[
    "candidate"
  ]
  presentation = actual[
    "presentation"
  ]

  assert (
    presentation.ehp
    is not None
  )
  assert (
    presentation
    .ehp
    .source_result
    is candidate
    .explanation
    .ehp_result
  )

  assert tuple(
    map_presentation.source_map
    for map_presentation in (
      presentation.ehp.maps
    )
  ) == (
    EHP_DELTA_MAP,
    EHP_E_MAP,
    EHP_H_MAP,
    EHP_DELTA_MAP,
  )


def test_phase96_7_actual_pi9_5_integrates_exactness_with_shared_ehp_presentation():
  actual = (
    build_phase96_7_actual_pi9_5_presentation()
  )

  candidate = actual[
    "candidate"
  ]
  presentation = actual[
    "presentation"
  ]

  assert (
    presentation.exactness
    is not None
  )
  assert (
    presentation
    .exactness
    .source_provenance
    is candidate
    .explanation
    .exactness_provenance
  )
  assert (
    presentation
    .exactness
    .sequence
    is presentation.ehp
  )
  assert len(
    presentation
    .exactness
    .uses
  ) == 3


def test_phase96_7_actual_pi9_5_preserves_hopf_zero_exactness_consumer():
  actual = (
    build_phase96_7_actual_pi9_5_presentation()
  )

  data = actual[
    "data"
  ]
  presentation = actual[
    "presentation"
  ]

  assert any(
    consumer
    is data[
      "phase68"
    ][
      "phase68_6"
    ][
      "hopf_zero_step"
    ]
    for consumer in (
      presentation
      .exactness
      .uses[
        2
      ]
      .consumer_steps
    )
  )


def test_phase96_7_actual_pi9_5_integrates_flat_dependency_presentation():
  actual = (
    build_phase96_7_actual_pi9_5_presentation()
  )

  candidate = actual[
    "candidate"
  ]
  presentation = actual[
    "presentation"
  ]

  assert (
    presentation
    .dependencies
    .source_result
    is candidate
    .explanation
    .dependency_result
  )

  assert (
    presentation
    .dependencies
    .root
    .source_step
    is candidate
    .group_result
    .proof_step
  )

  assert len(
    presentation
    .dependencies
    .dependencies
  ) == len(
    candidate
    .explanation
    .dependency_result
    .dependencies
  )


def test_phase96_7_actual_pi9_5_integrates_dependency_first_proof_flow():
  actual = (
    build_phase96_7_actual_pi9_5_presentation()
  )

  candidate = actual[
    "candidate"
  ]
  presentation = actual[
    "presentation"
  ]

  assert (
    presentation
    .proof_flow
    .source_provenance
    is candidate
    .explanation
    .recursive_provenance
  )

  assert (
    presentation
    .proof_flow
    .nodes[
      -1
    ].step.source_step
    is candidate
    .group_result
    .proof_step
  )

  position_by_step_id = {
    id(node.step.source_step): index
    for index, node in enumerate(
      presentation
      .proof_flow
      .nodes
    )
  }

  assert all(
    (
      position_by_step_id[
        id(
          edge
          .premise
          .step
          .source_step
        )
      ]
      < position_by_step_id[
        id(
          edge
          .parent
          .step
          .source_step
        )
      ]
    )
    for edge in (
      presentation
      .proof_flow
      .edges
    )
  )


def test_phase96_7_actual_pi9_5_integrates_calculation_source_metadata():
  actual = (
    build_phase96_7_actual_pi9_5_presentation()
  )

  data = actual[
    "data"
  ]
  presentation = actual[
    "presentation"
  ]

  assert (
    presentation
    .source
    .goal_source
    .repository_source
    .source_entry
    is data[
      "phase68_entry"
    ]
  )

  assert (
    presentation
    .source
    .goal_source
    .repository_source
    .phase
    == "68"
  )

  assert (
    presentation
    .source
    .goal_source
    .repository_source
    .theorem
    == "Toda Proposition 5.8"
  )

  assert (
    presentation
    .source
    .goal_source
    .branch_name
    == "pi9_5_group_relation"
  )


def test_phase96_7_actual_pi9_5_result_source_and_goal_source_remain_distinct():
  actual = (
    build_phase96_7_actual_pi9_5_presentation()
  )

  presentation = actual[
    "presentation"
  ]

  assert (
    presentation
    .source
    .result_source
    .source_entry
    is presentation
    .source_candidate
    .group_result
    .source_entry
  )

  assert (
    presentation
    .source
    .result_source
    .source_entry
    is not presentation
    .source
    .goal_source
    .repository_source
    .source_entry
  )


def test_phase96_7_actual_pi9_5_all_major_views_share_same_group_root():
  actual = (
    build_phase96_7_actual_pi9_5_presentation()
  )

  candidate = actual[
    "candidate"
  ]
  presentation = actual[
    "presentation"
  ]

  root_step = (
    candidate
    .group_result
    .proof_step
  )

  assert (
    presentation
    .dependencies
    .root
    .source_step
    is root_step
  )

  assert (
    presentation
    .proof_flow
    .root
    .step
    .source_step
    is root_step
  )


def test_phase96_7_actual_pi9_5_presentation_does_not_mutate_repository():
  data = build_phase95_20_data()

  before = (
    data[
      "repository"
    ].entries()
  )

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  build_toda_end_to_end_candidate_presentation(
    candidate,
    before,
  )

  after = (
    data[
      "repository"
    ].entries()
  )

  assert after == before
  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )


def test_phase96_7_builder_rejects_non_candidate():
  with pytest.raises(
    TypeError,
    match=(
      "candidate must be "
      "a TodaCalculationCandidate"
    ),
  ):
    build_toda_end_to_end_candidate_presentation(
      "not-a-candidate"
    )


def test_phase96_7_builder_rejects_non_tuple_repository_entries():
  actual = (
    build_phase96_7_actual_pi9_5_presentation()
  )

  with pytest.raises(
    TypeError,
    match=(
      "repository_entries must be a tuple"
    ),
  ):
    build_toda_end_to_end_candidate_presentation(
      actual[
        "candidate"
      ],
      [],
    )
