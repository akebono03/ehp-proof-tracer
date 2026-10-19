import pytest

from test_phase93_representative_explanation import (
  build_phase93_5_data,
)
from test_phase95_calculation_candidate_aggregate_provenance import (
  build_phase95_17_data,
)
from test_phase95_minimal_calculation_result import (
  build_phase95_2_candidate,
)
from toda_calculation_result import (
  TodaCalculationCandidate,
  TodaCalculationResult,
  TodaCalculationStatus,
)
from toda_group_query import TodaGroupQuery
from toda_presentation import (
  TodaCalculationPresentationCandidate,
  TodaCalculationPresentationResult,
  build_toda_calculation_presentation_result,
)


def test_phase96_2_candidate_preserves_source_candidate_identity():
  data = build_phase93_5_data()

  source_candidate = (
    TodaCalculationCandidate(
      group_result=data[
        "group_result"
      ],
      explanation=data[
        "explanation"
      ],
    )
  )

  candidate = (
    TodaCalculationPresentationCandidate(
      source_candidate=(
        source_candidate
      ),
    )
  )

  assert (
    candidate.source_candidate
    is source_candidate
  )


def test_phase96_2_candidate_exposes_existing_structured_inputs_by_identity():
  data = build_phase93_5_data()

  source_candidate = (
    TodaCalculationCandidate(
      group_result=data[
        "group_result"
      ],
      explanation=data[
        "explanation"
      ],
    )
  )

  candidate = (
    TodaCalculationPresentationCandidate(
      source_candidate=(
        source_candidate
      ),
    )
  )

  assert (
    candidate.group_result
    is source_candidate.group_result
  )
  assert (
    candidate.explanation
    is source_candidate.explanation
  )
  assert (
    candidate.ehp_result
    is source_candidate
    .explanation
    .ehp_result
  )
  assert (
    candidate.exactness_provenance
    is source_candidate
    .explanation
    .exactness_provenance
  )
  assert (
    candidate.dependency_result
    is source_candidate
    .explanation
    .dependency_result
  )
  assert (
    candidate.recursive_provenance
    is source_candidate
    .explanation
    .recursive_provenance
  )
  assert candidate.goal_source is None


def test_phase96_2_candidate_preserves_aggregate_goal_source_identity():
  data = build_phase95_17_data()

  source_candidate = (
    TodaCalculationCandidate(
      group_result=data[
        "group_result"
      ],
      explanation=data[
        "explanation"
      ],
      goal_source=(
        data[
          "goal_candidate"
        ].source
      ),
    )
  )

  candidate = (
    TodaCalculationPresentationCandidate(
      source_candidate=(
        source_candidate
      ),
    )
  )

  assert (
    candidate.goal_source
    is source_candidate.goal_source
  )
  assert (
    candidate
    .goal_source
    .source_entry
    is data[
      "entry"
    ]
  )


def test_phase96_2_result_preserves_source_result_identity_and_summary():
  data = build_phase93_5_data()

  source_candidate = (
    TodaCalculationCandidate(
      group_result=data[
        "group_result"
      ],
      explanation=data[
        "explanation"
      ],
    )
  )

  source_result = (
    TodaCalculationResult(
      query=TodaGroupQuery(
        n=5,
        k=4,
      ),
      candidates=(
        source_candidate,
      ),
    )
  )

  result = (
    build_toda_calculation_presentation_result(
      source_result
    )
  )

  assert isinstance(
    result,
    TodaCalculationPresentationResult,
  )
  assert (
    result.source_result
    is source_result
  )
  assert (
    result.query
    is source_result.query
  )
  assert (
    result.target
    == source_result.target
  )
  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )


def test_phase96_2_builder_preserves_candidate_identity_in_order():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  first = build_phase95_2_candidate(
    "phase96.first",
    query,
  )
  second = build_phase95_2_candidate(
    "phase96.second",
    query,
  )

  source_result = (
    TodaCalculationResult(
      query=query,
      candidates=(
        first,
        second,
      ),
    )
  )

  result = (
    build_toda_calculation_presentation_result(
      source_result
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.MULTIPLE_RESULTS
  )
  assert tuple(
    candidate.source_candidate
    for candidate in (
      result.candidates
    )
  ) == (
    first,
    second,
  )
  assert (
    result.candidates[
      0
    ].source_candidate
    is first
  )
  assert (
    result.candidates[
      1
    ].source_candidate
    is second
  )


def test_phase96_2_not_found_result_has_empty_presentation_candidates():
  source_result = (
    TodaCalculationResult(
      query=TodaGroupQuery(
        n=4,
        k=6,
      ),
      candidates=(),
    )
  )

  result = (
    build_toda_calculation_presentation_result(
      source_result
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.NOT_FOUND
  )
  assert result.candidates == ()


def test_phase96_2_candidate_rejects_non_calculation_candidate():
  with pytest.raises(
    TypeError,
    match=(
      "source_candidate must be "
      "a TodaCalculationCandidate"
    ),
  ):
    TodaCalculationPresentationCandidate(
      source_candidate=(
        "not-a-calculation-candidate"
      ),
    )


def test_phase96_2_result_rejects_non_source_result():
  with pytest.raises(
    TypeError,
    match=(
      "source_result must be "
      "a TodaCalculationResult"
    ),
  ):
    TodaCalculationPresentationResult(
      source_result=(
        "not-a-calculation-result"
      ),
      candidates=(),
    )


def test_phase96_2_result_rejects_non_tuple_candidates():
  source_result = (
    TodaCalculationResult(
      query=TodaGroupQuery(
        n=4,
        k=6,
      ),
      candidates=(),
    )
  )

  with pytest.raises(
    TypeError,
    match=(
      "candidates must be a tuple"
    ),
  ):
    TodaCalculationPresentationResult(
      source_result=source_result,
      candidates=[],
    )


def test_phase96_2_result_rejects_non_presentation_candidate_member():
  source_result = (
    TodaCalculationResult(
      query=TodaGroupQuery(
        n=4,
        k=6,
      ),
      candidates=(),
    )
  )

  with pytest.raises(
    TypeError,
    match=(
      "candidates must contain only "
      "TodaCalculationPresentationCandidate "
      "objects"
    ),
  ):
    TodaCalculationPresentationResult(
      source_result=source_result,
      candidates=(
        "not-a-presentation-candidate",
      ),
    )


def test_phase96_2_result_rejects_candidate_count_mismatch():
  data = build_phase93_5_data()

  source_candidate = (
    TodaCalculationCandidate(
      group_result=data[
        "group_result"
      ],
      explanation=data[
        "explanation"
      ],
    )
  )

  source_result = (
    TodaCalculationResult(
      query=TodaGroupQuery(
        n=5,
        k=4,
      ),
      candidates=(
        source_candidate,
      ),
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "presentation candidates must match "
      "source_result candidates"
    ),
  ):
    TodaCalculationPresentationResult(
      source_result=source_result,
      candidates=(),
    )


def test_phase96_2_result_rejects_candidate_identity_mismatch():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  first = build_phase95_2_candidate(
    "phase96.first",
    query,
  )
  second = build_phase95_2_candidate(
    "phase96.second",
    query,
  )

  source_result = (
    TodaCalculationResult(
      query=query,
      candidates=(
        first,
      ),
    )
  )

  wrong_candidate = (
    TodaCalculationPresentationCandidate(
      source_candidate=second,
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "presentation candidate identity "
      "must match source_result candidate "
      "identity in order"
    ),
  ):
    TodaCalculationPresentationResult(
      source_result=source_result,
      candidates=(
        wrong_candidate,
      ),
    )


def test_phase96_2_builder_rejects_non_calculation_result():
  with pytest.raises(
    TypeError,
    match=(
      "calculation_result must be "
      "a TodaCalculationResult"
    ),
  ):
    build_toda_calculation_presentation_result(
      "not-a-calculation-result"
    )
