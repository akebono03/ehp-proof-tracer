from functools import lru_cache

from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
)
from toda_calculation_report import (
  build_toda_calculation_report_result,
)
from toda_calculation_result import (
  TodaCalculationStatus,
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


@lru_cache(maxsize=1)
def build_phase97_5_data():
  data = build_phase95_20_data()

  repository = data[
    "repository"
  ]

  before = repository.entries()

  results = {
    key: build_toda_calculation_report_result(
      repository,
      data[
        "queries"
      ][
        key
      ],
    )
    for key in REPRESENTATIVE_KEYS
  }

  after = repository.entries()

  return {
    "data": data,
    "repository": repository,
    "before": before,
    "results": results,
    "after": after,
  }


def get_phase97_5_single_report_candidate(
  result,
):
  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert len(
    result.candidates
  ) == 1

  return result.candidates[
    0
  ]


def test_phase97_5_all_representative_targets_run_through_top_level_api():
  actual = build_phase97_5_data()

  results = actual[
    "results"
  ]

  assert tuple(
    results.keys()
  ) == REPRESENTATIVE_KEYS

  assert all(
    result.status
    is TodaCalculationStatus.FOUND
    for result in results.values()
  )

  assert all(
    len(
      result.candidates
    ) == 1
    for result in results.values()
  )


def test_phase97_5_all_results_preserve_calculation_candidate_identity():
  actual = build_phase97_5_data()

  for key in REPRESENTATIVE_KEYS:
    result = actual[
      "results"
    ][
      key
    ]

    report_candidate = (
      get_phase97_5_single_report_candidate(
        result
      )
    )

    assert (
      report_candidate.source_candidate
      is result
      .calculation_result
      .candidates[
        0
      ]
    )

    assert (
      report_candidate
      .presentation
      .source_candidate
      is report_candidate
      .source_candidate
    )


def test_phase97_5_all_reports_are_human_readable_full_reports():
  actual = build_phase97_5_data()

  for key in REPRESENTATIVE_KEYS:
    report = (
      get_phase97_5_single_report_candidate(
        actual[
          "results"
        ][
          key
        ]
      ).report
    )

    assert report.startswith(
      "# $\\pi_"
    )
    assert "## Result" in report
    assert "## Source" in report
    assert "## Proof flow" in report
    assert (
      "## Readable proof narrative"
      in report
    )


def test_phase97_5_representative_group_semantics_survive_top_level_api():
  actual = build_phase97_5_data()

  pi7_4 = (
    get_phase97_5_single_report_candidate(
      actual[
        "results"
      ][
        "pi7_4"
      ]
    ).presentation
  )

  assert (
    pi7_4
    .group
    .group_structure
    .kind
    is TodaGroupStructureKind.DIRECT_SUM
  )

  assert tuple(
    generator.order.kind
    for generator in (
      pi7_4
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
      pi7_4
      .group
      .generators
    )
  ) == (
    None,
    4,
  )

  pi10_4 = (
    get_phase97_5_single_report_candidate(
      actual[
        "results"
      ][
        "pi10_4"
      ]
    ).presentation
  )

  assert (
    pi10_4
    .group
    .group_structure
    .kind
    is TodaGroupStructureKind.FINITE_CYCLIC
  )
  assert (
    pi10_4
    .group
    .generators[
      0
    ].order.value
    == 8
  )

  pi9_2 = (
    get_phase97_5_single_report_candidate(
      actual[
        "results"
      ][
        "pi9_2"
      ]
    ).presentation
  )

  assert (
    pi9_2
    .group
    .group_structure
    .kind
    is TodaGroupStructureKind.ZERO
  )
  assert (
    pi9_2
    .group
    .generators
    == ()
  )


def test_phase97_5_representative_goal_source_provenance_survives_top_level_api():
  actual = build_phase97_5_data()

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
      expected_phase,
      expected_theorem,
      expected_branch,
    ),
  ) in expected.items():
    source = (
      get_phase97_5_single_report_candidate(
        actual[
          "results"
        ][
          key
        ]
      )
      .presentation
      .source
      .goal_source
    )

    assert source is not None
    assert (
      source
      .repository_source
      .phase
      == expected_phase
    )
    assert (
      source
      .repository_source
      .theorem
      == expected_theorem
    )
    assert (
      source.branch_name
      == expected_branch
    )


def test_phase97_5_actual_pi9_5_preserves_ehp_exactness_and_root_identity():
  actual = build_phase97_5_data()

  report_candidate = (
    get_phase97_5_single_report_candidate(
      actual[
        "results"
      ][
        "pi9_5"
      ]
    )
  )

  source_candidate = (
    report_candidate.source_candidate
  )

  presentation = (
    report_candidate.presentation
  )

  root_step = (
    source_candidate
    .group_result
    .proof_step
  )

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


def test_phase97_5_nested_and_sigma_branches_survive_top_level_api():
  actual = build_phase97_5_data()

  pi11_5 = (
    get_phase97_5_single_report_candidate(
      actual[
        "results"
      ][
        "pi11_5"
      ]
    )
  )

  assert (
    pi11_5
    .presentation
    .group
    .generators[
      0
    ].order.value
    == 2
  )
  assert (
    pi11_5
    .presentation
    .source
    .goal_source
    .branch_name
    == (
      "nu_squared_finite_dimensional."
      "pi11_5_group_relation"
    )
  )

  pi12_5 = (
    get_phase97_5_single_report_candidate(
      actual[
        "results"
      ][
        "pi12_5"
      ]
    )
  )

  assert (
    pi12_5
    .presentation
    .group
    .generators[
      0
    ].order.value
    == 2
  )
  assert (
    pi12_5
    .presentation
    .source
    .goal_source
    .branch_name
    == "pi12_5_group_relation"
  )


def test_phase97_5_top_level_validation_does_not_mutate_repository():
  actual = build_phase97_5_data()

  before = actual[
    "before"
  ]
  after = actual[
    "after"
  ]

  assert after == before

  assert all(
    current is original
    for current, original in zip(
      after,
      before,
    )
  )
