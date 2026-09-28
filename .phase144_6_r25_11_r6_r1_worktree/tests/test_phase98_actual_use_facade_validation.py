from functools import lru_cache

from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
)
from toda_calculation_facade import (
  build_toda_report,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_presentation import (
  TodaGeneratorOrderKind,
  TodaGroupStructureKind,
)


REPRESENTATIVE_INPUTS = {
  "pi7_4": (
    4,
    3,
  ),
  "pi9_5": (
    5,
    4,
  ),
  "pi10_4": (
    4,
    6,
  ),
  "pi11_5": (
    5,
    6,
  ),
  "pi9_2": (
    2,
    7,
  ),
  "pi12_5": (
    5,
    7,
  ),
}


@lru_cache(maxsize=1)
def build_phase98_3_data():
  data = build_phase95_20_data()

  repository = data[
    "repository"
  ]

  before = repository.entries()

  results = {
    key: build_toda_report(
      repository,
      n=n,
      k=k,
    )
    for (
      key,
      (
        n,
        k,
      ),
    ) in REPRESENTATIVE_INPUTS.items()
  }

  after = repository.entries()

  return {
    "data": data,
    "repository": repository,
    "before": before,
    "results": results,
    "after": after,
  }


def get_phase98_3_single_report_candidate(
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


def test_phase98_3_all_representative_targets_run_through_raw_n_k_facade():
  actual = build_phase98_3_data()

  results = actual[
    "results"
  ]

  assert tuple(
    results.keys()
  ) == tuple(
    REPRESENTATIVE_INPUTS.keys()
  )

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


def test_phase98_3_facade_constructs_expected_queries_from_raw_n_k():
  actual = build_phase98_3_data()

  for (
    key,
    (
      n,
      k,
    ),
  ) in REPRESENTATIVE_INPUTS.items():
    result = actual[
      "results"
    ][
      key
    ]

    assert result.query.n == n
    assert result.query.k == k
    assert (
      result.target.group_dimension
      == n + k
    )
    assert (
      result.target.sphere_dimension
      == n
    )


def test_phase98_3_facade_preserves_calculation_candidate_identity():
  actual = build_phase98_3_data()

  for key in REPRESENTATIVE_INPUTS:
    result = actual[
      "results"
    ][
      key
    ]

    report_candidate = (
      get_phase98_3_single_report_candidate(
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


def test_phase98_3_facade_preserves_human_readable_full_reports():
  actual = build_phase98_3_data()

  for key in REPRESENTATIVE_INPUTS:
    report = (
      get_phase98_3_single_report_candidate(
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


def test_phase98_3_facade_preserves_representative_group_semantics():
  actual = build_phase98_3_data()

  pi7_4 = (
    get_phase98_3_single_report_candidate(
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
    get_phase98_3_single_report_candidate(
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
    get_phase98_3_single_report_candidate(
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


def test_phase98_3_facade_preserves_goal_source_provenance():
  actual = build_phase98_3_data()

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
      get_phase98_3_single_report_candidate(
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


def test_phase98_3_facade_preserves_pi9_5_ehp_exactness_and_root_identity():
  actual = build_phase98_3_data()

  report_candidate = (
    get_phase98_3_single_report_candidate(
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


def test_phase98_3_facade_preserves_nested_and_sigma_branches():
  actual = build_phase98_3_data()

  pi11_5 = (
    get_phase98_3_single_report_candidate(
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
    get_phase98_3_single_report_candidate(
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


def test_phase98_3_facade_validation_does_not_mutate_repository():
  actual = build_phase98_3_data()

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
