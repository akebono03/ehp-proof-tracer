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


REPRESENTATIVE_KEYS = (
  "pi7_4",
  "pi9_5",
  "pi10_4",
  "pi11_5",
  "pi9_2",
  "pi12_5",
)


def build_phase96_8_presentations():
  data = build_phase95_20_data()

  repository_entries = (
    data[
      "repository"
    ].entries()
  )

  candidates = {
    key: get_single_candidate(
      data[
        "results"
      ][
        key
      ]
    )
    for key in REPRESENTATIVE_KEYS
  }

  presentations = {
    key: build_toda_end_to_end_candidate_presentation(
      candidate,
      repository_entries,
    )
    for key, candidate in candidates.items()
  }

  return {
    "data": data,
    "repository_entries": (
      repository_entries
    ),
    "candidates": candidates,
    "presentations": presentations,
  }


def test_phase96_8_all_representative_targets_build_end_to_end_presentations():
  actual = (
    build_phase96_8_presentations()
  )

  assert tuple(
    actual[
      "presentations"
    ].keys()
  ) == REPRESENTATIVE_KEYS

  assert all(
    isinstance(
      presentation,
      TodaEndToEndCandidatePresentation,
    )
    for presentation in (
      actual[
        "presentations"
      ].values()
    )
  )


def test_phase96_8_all_representative_presentations_preserve_candidate_identity():
  actual = (
    build_phase96_8_presentations()
  )

  assert all(
    (
      actual[
        "presentations"
      ][
        key
      ].source_candidate
      is actual[
        "candidates"
      ][
        key
      ]
    )
    for key in REPRESENTATIVE_KEYS
  )


def test_phase96_8_all_representative_targets_preserve_target_dimensions():
  actual = (
    build_phase96_8_presentations()
  )

  expected_dimensions = {
    "pi7_4": (
      7,
      4,
    ),
    "pi9_5": (
      9,
      5,
    ),
    "pi10_4": (
      10,
      4,
    ),
    "pi11_5": (
      11,
      5,
    ),
    "pi9_2": (
      9,
      2,
    ),
    "pi12_5": (
      12,
      5,
    ),
  }

  for (
    key,
    (
      group_dimension,
      sphere_dimension,
    ),
  ) in expected_dimensions.items():
    target = (
      actual[
        "presentations"
      ][
        key
      ]
      .group
      .target
    )

    assert (
      target.group_dimension
      == group_dimension
    )
    assert (
      target.sphere_dimension
      == sphere_dimension
    )


def test_phase96_8_pi7_4_preserves_direct_sum_and_mixed_generator_orders():
  actual = (
    build_phase96_8_presentations()
  )

  presentation = (
    actual[
      "presentations"
    ][
      "pi7_4"
    ]
  )

  assert (
    presentation
    .group
    .group_structure
    .kind
    is TodaGroupStructureKind.DIRECT_SUM
  )

  assert len(
    presentation
    .group
    .group_structure
    .summands
  ) == 2

  assert (
    presentation
    .group
    .group_structure
    .summands[
      0
    ].kind
    is TodaGroupStructureKind.FREE_CYCLIC
  )

  assert (
    presentation
    .group
    .group_structure
    .summands[
      1
    ].kind
    is TodaGroupStructureKind.FINITE_CYCLIC
  )

  assert tuple(
    generator.order.kind
    for generator in (
      presentation
      .group
      .generators
    )
  ) == (
    TodaGeneratorOrderKind.INFINITE,
    TodaGeneratorOrderKind.FINITE,
  )

  assert tuple(
    generator.order.value
    for generator in (
      presentation
      .group
      .generators
    )
  ) == (
    None,
    4,
  )


def test_phase96_8_pi10_4_preserves_order_eight_finite_cyclic_group():
  actual = (
    build_phase96_8_presentations()
  )

  presentation = (
    actual[
      "presentations"
    ][
      "pi10_4"
    ]
  )

  assert (
    presentation
    .group
    .group_structure
    .kind
    is TodaGroupStructureKind.FINITE_CYCLIC
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
    == 8
  )


def test_phase96_8_pi11_5_preserves_nested_branch_order_two_result():
  actual = (
    build_phase96_8_presentations()
  )

  presentation = (
    actual[
      "presentations"
    ][
      "pi11_5"
    ]
  )

  assert (
    presentation
    .group
    .group_structure
    .kind
    is TodaGroupStructureKind.FINITE_CYCLIC
  )

  assert (
    presentation
    .group
    .generators[
      0
    ].order.value
    == 2
  )

  assert (
    presentation
    .source
    .goal_source
    .branch_name
    == (
      "nu_squared_finite_dimensional."
      "pi11_5_group_relation"
    )
  )


def test_phase96_8_pi9_2_preserves_zero_group_semantics():
  actual = (
    build_phase96_8_presentations()
  )

  presentation = (
    actual[
      "presentations"
    ][
      "pi9_2"
    ]
  )

  assert (
    presentation
    .group
    .group_structure
    .kind
    is TodaGroupStructureKind.ZERO
  )

  assert (
    presentation
    .group
    .generators
    == ()
  )

  assert (
    presentation
    .source
    .goal_source
    .branch_name
    == "pi9_2_zero"
  )


def test_phase96_8_pi12_5_preserves_order_two_sigma_branch():
  actual = (
    build_phase96_8_presentations()
  )

  candidate = (
    actual[
      "candidates"
    ][
      "pi12_5"
    ]
  )

  presentation = (
    actual[
      "presentations"
    ][
      "pi12_5"
    ]
  )

  assert (
    presentation
    .group
    .group_structure
    .kind
    is TodaGroupStructureKind.FINITE_CYCLIC
  )

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
    ].order.value
    == 2
  )


def test_phase96_8_representative_goal_sources_preserve_theorem_phase_and_branch():
  actual = (
    build_phase96_8_presentations()
  )

  expected = {
    "pi7_4": (
      "65",
      "Toda Proposition 5.6",
      "pi7_4_group_relation",
    ),
    "pi9_5": (
      "68",
      "Toda Proposition 5.8",
      "pi9_5_group_relation",
    ),
    "pi10_4": (
      "73",
      "Toda Proposition 5.11",
      "pi10_4_group_relation",
    ),
    "pi11_5": (
      "73",
      "Toda Proposition 5.11",
      (
        "nu_squared_finite_dimensional."
        "pi11_5_group_relation"
      ),
    ),
    "pi9_2": (
      "75",
      "Toda Proposition 5.15",
      "pi9_2_zero",
    ),
    "pi12_5": (
      "75",
      "Toda Proposition 5.15",
      "pi12_5_group_relation",
    ),
  }

  for (
    key,
    (
      phase,
      theorem,
      branch_name,
    ),
  ) in expected.items():
    source = (
      actual[
        "presentations"
      ][
        key
      ]
      .source
      .goal_source
    )

    assert (
      source
      .repository_source
      .phase
      == phase
    )
    assert (
      source
      .repository_source
      .theorem
      == theorem
    )
    assert (
      source.branch_name
      == branch_name
    )


def test_phase96_8_all_representative_results_keep_result_and_goal_sources_distinct():
  actual = (
    build_phase96_8_presentations()
  )

  assert all(
    (
      actual[
        "presentations"
      ][
        key
      ]
      .source
      .result_source
      .source_entry
      is not actual[
        "presentations"
      ][
        key
      ]
      .source
      .goal_source
      .repository_source
      .source_entry
    )
    for key in REPRESENTATIVE_KEYS
  )


def test_phase96_8_all_representative_views_share_group_proof_root():
  actual = (
    build_phase96_8_presentations()
  )

  for key in REPRESENTATIVE_KEYS:
    candidate = (
      actual[
        "candidates"
      ][
        key
      ]
    )
    presentation = (
      actual[
        "presentations"
      ][
        key
      ]
    )

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

    assert (
      presentation
      .proof_flow
      .nodes[
        -1
      ]
      is presentation
      .proof_flow
      .root
    )


def test_phase96_8_all_representative_flows_are_dependency_first_for_acyclic_actual_proofs():
  actual = (
    build_phase96_8_presentations()
  )

  for key in REPRESENTATIVE_KEYS:
    presentation = (
      actual[
        "presentations"
      ][
        key
      ]
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


def test_phase96_8_ehp_and_exactness_presence_matches_each_source_explanation():
  actual = (
    build_phase96_8_presentations()
  )

  for key in REPRESENTATIVE_KEYS:
    candidate = (
      actual[
        "candidates"
      ][
        key
      ]
    )
    presentation = (
      actual[
        "presentations"
      ][
        key
      ]
    )

    if (
      candidate
      .explanation
      .ehp_result
      is None
    ):
      assert (
        presentation.ehp
        is None
      )
      assert (
        presentation.exactness
        is None
      )
      continue

    assert (
      presentation.ehp
      is not None
    )
    assert (
      presentation.exactness
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


def test_phase96_8_expansion_does_not_mutate_repository():
  data = build_phase95_20_data()

  before = (
    data[
      "repository"
    ].entries()
  )

  for key in REPRESENTATIVE_KEYS:
    candidate = get_single_candidate(
      data[
        "results"
      ][
        key
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
