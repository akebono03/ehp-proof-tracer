import pytest

from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  Relation,
  RelationType,
)
from test_phase90_known_group_lookup import (
  make_generator,
)
from toda_calculation_goal import (
  TodaCalculationGoalCandidate,
  TodaCalculationGoalDiscoveryResult,
  TodaCalculationGoalDiscoveryStatus,
)
from toda_group_query import TodaGroupQuery


def make_phase95_5_finite_goal(
  query,
  name="nu4_squared",
):
  return Relation(
    lhs=query.target,
    rhs=FiniteCyclicGroup(
      order=8,
      generator=make_generator(
        name=name,
        family="nu^2",
        index=query.n,
        dimension=(
          query.n
          + query.k
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )


def test_phase95_5_candidate_preserves_target_and_goal():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )
  goal = make_phase95_5_finite_goal(
    query
  )

  candidate = (
    TodaCalculationGoalCandidate(
      target=query.target,
      goal=goal,
    )
  )

  assert (
    candidate.target
    == query.target
  )
  assert candidate.goal is goal


def test_phase95_5_candidate_accepts_zero_group_goal():
  query = TodaGroupQuery(
    n=2,
    k=7,
  )
  goal = (
    TodaPrimaryGroupZeroStatement(
      group=query.target,
    )
  )

  candidate = (
    TodaCalculationGoalCandidate(
      target=query.target,
      goal=goal,
    )
  )

  assert candidate.goal is goal


def test_phase95_5_candidate_rejects_wrong_target_goal():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )
  wrong_query = TodaGroupQuery(
    n=5,
    k=6,
  )
  goal = make_phase95_5_finite_goal(
    wrong_query,
    name="nu5_squared",
  )

  with pytest.raises(
    ValueError,
    match=(
      "goal must be a normalizable "
      "Toda group result statement "
      "for target"
    ),
  ):
    TodaCalculationGoalCandidate(
      target=query.target,
      goal=goal,
    )


def test_phase95_5_candidate_rejects_non_group_result_statement():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  goal = Relation(
    lhs=query.target,
    rhs=8,
    relation_type=RelationType.ORDER,
  )

  with pytest.raises(
    ValueError,
    match=(
      "goal must be a normalizable "
      "Toda group result statement "
      "for target"
    ),
  ):
    TodaCalculationGoalCandidate(
      target=query.target,
      goal=goal,
    )


def test_phase95_5_candidate_rejects_non_target():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )
  goal = make_phase95_5_finite_goal(
    query
  )

  with pytest.raises(
    TypeError,
    match=(
      "target must be "
      "a TodaPrimaryGroup"
    ),
  ):
    TodaCalculationGoalCandidate(
      target="not-a-target",
      goal=goal,
    )


def test_phase95_5_discovery_result_reports_no_candidates():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  result = (
    TodaCalculationGoalDiscoveryResult(
      query=query,
      candidates=(),
    )
  )

  assert result.query is query
  assert result.target == query.target
  assert (
    result.status
    is (
      TodaCalculationGoalDiscoveryStatus
      .NO_CANDIDATES
    )
  )
  assert result.candidates == ()


def test_phase95_5_discovery_result_reports_unique_candidate():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )
  candidate = (
    TodaCalculationGoalCandidate(
      target=query.target,
      goal=make_phase95_5_finite_goal(
        query
      ),
    )
  )

  result = (
    TodaCalculationGoalDiscoveryResult(
      query=query,
      candidates=(
        candidate,
      ),
    )
  )

  assert (
    result.status
    is (
      TodaCalculationGoalDiscoveryStatus
      .UNIQUE_CANDIDATE
    )
  )


def test_phase95_5_discovery_result_reports_multiple_candidates_in_order():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  first = (
    TodaCalculationGoalCandidate(
      target=query.target,
      goal=make_phase95_5_finite_goal(
        query,
        name="first",
      ),
    )
  )
  second = (
    TodaCalculationGoalCandidate(
      target=query.target,
      goal=make_phase95_5_finite_goal(
        query,
        name="second",
      ),
    )
  )

  result = (
    TodaCalculationGoalDiscoveryResult(
      query=query,
      candidates=(
        first,
        second,
      ),
    )
  )

  assert (
    result.status
    is (
      TodaCalculationGoalDiscoveryStatus
      .MULTIPLE_CANDIDATES
    )
  )
  assert (
    result.candidates
    == (
      first,
      second,
    )
  )


def test_phase95_5_discovery_result_rejects_candidate_for_other_query():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )
  other_query = TodaGroupQuery(
    n=5,
    k=6,
  )

  candidate = (
    TodaCalculationGoalCandidate(
      target=other_query.target,
      goal=make_phase95_5_finite_goal(
        other_query
      ),
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "candidate target must match "
      "query target"
    ),
  ):
    TodaCalculationGoalDiscoveryResult(
      query=query,
      candidates=(
        candidate,
      ),
    )


def test_phase95_5_discovery_result_rejects_non_query():
  with pytest.raises(
    TypeError,
    match=(
      "query must be "
      "a TodaGroupQuery"
    ),
  ):
    TodaCalculationGoalDiscoveryResult(
      query="not-a-query",
      candidates=(),
    )


def test_phase95_5_discovery_result_rejects_non_tuple_candidates():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  with pytest.raises(
    TypeError,
    match="candidates must be a tuple",
  ):
    TodaCalculationGoalDiscoveryResult(
      query=query,
      candidates=[],
    )


def test_phase95_5_discovery_result_rejects_non_candidate_member():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  with pytest.raises(
    TypeError,
    match=(
      "candidates must contain only "
      "TodaCalculationGoalCandidate "
      "objects"
    ),
  ):
    TodaCalculationGoalDiscoveryResult(
      query=query,
      candidates=(
        "not-a-candidate",
      ),
    )
