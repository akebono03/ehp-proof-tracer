import pytest

from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
)
from toda_calculation_report import (
  build_toda_found_calculation_report_result,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_query import TodaGroupQuery


def test_phase97_3_aggregate_found_runs_calculation_to_report_end_to_end():
  data = build_phase95_20_data()

  query = TodaGroupQuery(
    n=5,
    k=4,
  )

  result = (
    build_toda_found_calculation_report_result(
      data[
        "repository"
      ],
      query,
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert (
    result.query
    is query
  )
  assert len(
    result.candidates
  ) == 1

  report_candidate = (
    result.candidates[
      0
    ]
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
  assert (
    "# $\\pi_{9}^{5}$"
    in report_candidate.report
  )
  assert (
    "## Result"
    in report_candidate.report
  )
  assert (
    "## Source"
    in report_candidate.report
  )
  assert (
    "## Proof flow"
    in report_candidate.report
  )
  assert (
    "## Readable proof narrative"
    in report_candidate.report
  )


def test_phase97_3_aggregate_found_preserves_goal_source_provenance():
  data = build_phase95_20_data()

  result = (
    build_toda_found_calculation_report_result(
      data[
        "repository"
      ],
      TodaGroupQuery(
        n=5,
        k=4,
      ),
    )
  )

  source_candidate = (
    result.candidates[
      0
    ].source_candidate
  )

  assert (
    source_candidate.goal_source
    is not None
  )
  assert (
    source_candidate
    .goal_source
    .source_entry
    is data[
      "phase68_entry"
    ]
  )
  assert (
    source_candidate
    .goal_source
    .branch_name
    == "pi9_5_group_relation"
  )

  source_presentation = (
    result.candidates[
      0
    ].presentation.source
  )

  assert (
    source_presentation
    .goal_source
    .repository_source
    .source_entry
    is data[
      "phase68_entry"
    ]
  )
  assert (
    source_presentation
    .goal_source
    .branch_name
    == "pi9_5_group_relation"
  )


def test_phase97_3_direct_found_preserves_direct_result_without_goal_source():
  data = build_phase65_9_data()

  repository = ProofRepository()

  direct_entry = ProofRepositoryEntry(
    key="phase97.direct.pi7_4",
    step=data[
      "pi7_4_step"
    ],
    phase="65",
    theorem=(
      "Toda Proposition 5.6 direct"
    ),
  )

  repository.register(
    direct_entry
  )

  result = (
    build_toda_found_calculation_report_result(
      repository,
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )
  )

  source_candidate = (
    result.candidates[
      0
    ].source_candidate
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert (
    source_candidate
    .group_result
    .source_entry
    is direct_entry
  )
  assert (
    source_candidate.goal_source
    is None
  )
  assert (
    result.candidates[
      0
    ].presentation
    .source
    .goal_source
    is None
  )
  assert (
    r"\pi_{7}^{4} \cong "
    in result.candidates[
      0
    ].report
  )


def test_phase97_3_found_api_does_not_mutate_repository():
  data = build_phase95_20_data()

  repository = data[
    "repository"
  ]

  before = repository.entries()

  build_toda_found_calculation_report_result(
    repository,
    TodaGroupQuery(
      n=5,
      k=4,
    ),
  )

  after = repository.entries()

  assert after == before
  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )


def test_phase97_3_not_found_is_rejected_without_fake_report():
  repository = ProofRepository()

  with pytest.raises(
    ValueError,
    match=(
      "calculation result must have "
      "status FOUND"
    ),
  ):
    build_toda_found_calculation_report_result(
      repository,
      TodaGroupQuery(
        n=9,
        k=7,
      ),
    )


def test_phase97_3_multiple_results_are_rejected_without_silent_selection():
  data = build_phase65_9_data()

  repository = ProofRepository()

  first_entry = ProofRepositoryEntry(
    key="phase97.direct.first",
    step=data[
      "pi7_4_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 first",
  )

  second_entry = ProofRepositoryEntry(
    key="phase97.direct.second",
    step=data[
      "pi7_4_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 second",
  )

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  with pytest.raises(
    ValueError,
    match=(
      "calculation result must have "
      "status FOUND"
    ),
  ):
    build_toda_found_calculation_report_result(
      repository,
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )
