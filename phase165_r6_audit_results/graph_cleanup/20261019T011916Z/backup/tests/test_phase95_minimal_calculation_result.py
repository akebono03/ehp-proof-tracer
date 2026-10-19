import pytest

from homotopy_groups import FiniteCyclicGroup
from proof import (
  ProofRule,
  Relation,
  RelationType,
)
from test_phase90_known_group_lookup import (
  make_entry,
  make_generator,
)
from test_phase93_representative_explanation import (
  build_phase93_5_data,
)
from toda_calculation_result import (
  TodaCalculationCandidate,
  TodaCalculationResult,
  TodaCalculationStatus,
)
from toda_explanation import (
  build_toda_representative_explanation,
)
from toda_group_query import TodaGroupQuery
from toda_group_result import (
  normalize_toda_group_result,
)


def build_phase95_2_candidate(
  key,
  query,
):
  relation = Relation(
    lhs=query.target,
    rhs=FiniteCyclicGroup(
      order=8,
      generator=make_generator(
        name="nu4_squared",
        family="nu^2",
        index=4,
        dimension=10,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  entry = make_entry(
    key=key,
    conclusion=relation,
    rule=ProofRule.GIVEN,
  )

  group_result = (
    normalize_toda_group_result(
      entry
    )
  )

  explanation = (
    build_toda_representative_explanation(
      group_result
    )
  )

  return TodaCalculationCandidate(
    group_result=group_result,
    explanation=explanation,
  )


def test_phase95_2_candidate_preserves_group_result_identity():
  data = build_phase93_5_data()

  candidate = TodaCalculationCandidate(
    group_result=data[
      "group_result"
    ],
    explanation=data[
      "explanation"
    ],
  )

  assert (
    candidate.group_result
    is data[
      "group_result"
    ]
  )
  assert (
    candidate.explanation
    is data[
      "explanation"
    ]
  )
  assert (
    candidate.explanation.group_result
    is candidate.group_result
  )


def test_phase95_2_not_found_result_has_empty_candidates():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  result = TodaCalculationResult(
    query=query,
    candidates=(),
  )

  assert result.query is query
  assert (
    result.status
    is TodaCalculationStatus.NOT_FOUND
  )
  assert result.candidates == ()
  assert result.target == query.target


def test_phase95_2_found_result_preserves_actual_representative_identity():
  data = build_phase93_5_data()

  query = TodaGroupQuery(
    n=5,
    k=4,
  )

  candidate = TodaCalculationCandidate(
    group_result=data[
      "group_result"
    ],
    explanation=data[
      "explanation"
    ],
  )

  result = TodaCalculationResult(
    query=query,
    candidates=(
      candidate,
    ),
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert (
    result.candidates[
      0
    ]
    is candidate
  )
  assert (
    result.candidates[
      0
    ].group_result
    is data[
      "group_result"
    ]
  )
  assert (
    result.candidates[
      0
    ].explanation
    is data[
      "explanation"
    ]
  )
  assert (
    result.candidates[
      0
    ].explanation
    .recursive_provenance
    .root_step
    is data[
      "group_result"
    ].proof_step
  )


def test_phase95_2_multiple_results_preserve_candidate_order():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  first = build_phase95_2_candidate(
    "phase95.first",
    query,
  )
  second = build_phase95_2_candidate(
    "phase95.second",
    query,
  )

  result = TodaCalculationResult(
    query=query,
    candidates=(
      first,
      second,
    ),
  )

  assert (
    result.status
    is TodaCalculationStatus.MULTIPLE_RESULTS
  )
  assert (
    result.candidates
    == (
      first,
      second,
    )
  )
  assert (
    result.candidates[
      0
    ].group_result.source_entry.key
    == "phase95.first"
  )
  assert (
    result.candidates[
      1
    ].group_result.source_entry.key
    == "phase95.second"
  )


def test_phase95_2_candidate_rejects_mismatched_explanation_identity():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  first = build_phase95_2_candidate(
    "phase95.first",
    query,
  )
  second = build_phase95_2_candidate(
    "phase95.second",
    query,
  )

  with pytest.raises(
    ValueError,
    match=(
      "explanation.group_result must be "
      "group_result"
    ),
  ):
    TodaCalculationCandidate(
      group_result=first.group_result,
      explanation=second.explanation,
    )


def test_phase95_2_result_rejects_candidate_for_wrong_target():
  result_query = TodaGroupQuery(
    n=5,
    k=4,
  )
  other_query = TodaGroupQuery(
    n=4,
    k=6,
  )

  candidate = build_phase95_2_candidate(
    "phase95.other",
    other_query,
  )

  with pytest.raises(
    ValueError,
    match=(
      "candidate target must match "
      "query target"
    ),
  ):
    TodaCalculationResult(
      query=result_query,
      candidates=(
        candidate,
      ),
    )


def test_phase95_2_candidate_rejects_non_group_result():
  data = build_phase93_5_data()

  with pytest.raises(
    TypeError,
    match=(
      "group_result must be "
      "a TodaGroupResult"
    ),
  ):
    TodaCalculationCandidate(
      group_result="not-a-group-result",
      explanation=data[
        "explanation"
      ],
    )


def test_phase95_2_candidate_rejects_non_explanation():
  data = build_phase93_5_data()

  with pytest.raises(
    TypeError,
    match=(
      "explanation must be "
      "a TodaRepresentativeExplanationResult"
    ),
  ):
    TodaCalculationCandidate(
      group_result=data[
        "group_result"
      ],
      explanation="not-an-explanation",
    )


def test_phase95_2_result_rejects_non_query():
  with pytest.raises(
    TypeError,
    match="query must be a TodaGroupQuery",
  ):
    TodaCalculationResult(
      query="not-a-query",
      candidates=(),
    )


def test_phase95_2_result_rejects_non_tuple_candidates():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  with pytest.raises(
    TypeError,
    match="candidates must be a tuple",
  ):
    TodaCalculationResult(
      query=query,
      candidates=[],
    )


def test_phase95_2_result_rejects_non_candidate_member():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  with pytest.raises(
    TypeError,
    match=(
      "candidates must contain only "
      "TodaCalculationCandidate objects"
    ),
  ):
    TodaCalculationResult(
      query=query,
      candidates=(
        "not-a-candidate",
      ),
    )
