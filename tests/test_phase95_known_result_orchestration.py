import pytest

from homotopy_groups import FiniteCyclicGroup
from proof import (
  ProofRule,
  Relation,
  RelationType,
)
from proof_repository import ProofRepository
from test_phase90_known_group_lookup import (
  make_entry,
  make_generator,
)
from test_phase92_actual_ehp_extraction import (
  build_phase92_3_data,
)
from toda_calculation import (
  build_known_toda_calculation_result,
)
from toda_calculation_result import (
  TodaCalculationResult,
  TodaCalculationStatus,
)
from toda_group_query import TodaGroupQuery


def test_phase95_3_lookup_miss_returns_not_found_without_candidates():
  repository = ProofRepository()
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  initial_entries = repository.entries()

  result = (
    build_known_toda_calculation_result(
      repository,
      query,
    )
  )

  assert isinstance(
    result,
    TodaCalculationResult,
  )
  assert result.query is query
  assert (
    result.status
    is TodaCalculationStatus.NOT_FOUND
  )
  assert result.candidates == ()
  assert (
    repository.entries()
    == initial_entries
  )


def test_phase95_3_actual_pi9_5_builds_found_calculation_result():
  data = build_phase92_3_data()

  repository = ProofRepository()
  repository.register(
    data[
      "entry"
    ]
  )

  query = TodaGroupQuery(
    n=5,
    k=4,
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      query,
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert len(
    result.candidates
  ) == 1

  candidate = result.candidates[
    0
  ]

  assert (
    candidate.group_result.source_entry
    is data[
      "entry"
    ]
  )
  assert (
    candidate.group_result.proof_step
    is data[
      "entry"
    ].step
  )
  assert (
    candidate.explanation.group_result
    is candidate.group_result
  )
  assert (
    candidate.explanation
    .recursive_provenance
    .root_step
    is candidate.group_result.proof_step
  )


def test_phase95_3_actual_pi9_5_integrates_ehp_explanation():
  data = build_phase92_3_data()

  repository = ProofRepository()
  repository.register(
    data[
      "entry"
    ]
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=5,
        k=4,
      ),
    )
  )

  candidate = result.candidates[
    0
  ]

  assert (
    candidate.explanation.ehp_result
    is not None
  )
  assert (
    candidate.explanation
    .ehp_result
    .target
    == candidate.group_result.target
  )
  assert (
    candidate.explanation
    .exactness_provenance
    .ehp_result
    is candidate.explanation.ehp_result
  )


def test_phase95_3_multiple_known_results_preserve_registration_order():
  repository = ProofRepository()
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

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

  first_entry = make_entry(
    key="phase95.first",
    conclusion=relation,
    rule=ProofRule.GIVEN,
  )
  second_entry = make_entry(
    key="phase95.second",
    conclusion=relation,
    rule=ProofRule.INFERENCE,
  )

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      query,
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.MULTIPLE_RESULTS
  )
  assert tuple(
    candidate.group_result.source_entry
    for candidate in result.candidates
  ) == (
    first_entry,
    second_entry,
  )


def test_phase95_3_multiple_results_do_not_select_single_candidate():
  repository = ProofRepository()
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

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

  first_entry = make_entry(
    key="phase95.first",
    conclusion=relation,
  )
  second_entry = make_entry(
    key="phase95.second",
    conclusion=relation,
  )

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      query,
    )
  )

  assert len(
    result.candidates
  ) == 2
  assert (
    result.candidates[
      0
    ].group_result.source_entry
    is first_entry
  )
  assert (
    result.candidates[
      1
    ].group_result.source_entry
    is second_entry
  )


def test_phase95_3_orchestration_does_not_mutate_repository():
  data = build_phase92_3_data()

  repository = ProofRepository()
  repository.register(
    data[
      "entry"
    ]
  )

  initial_entries = (
    repository.entries()
  )

  build_known_toda_calculation_result(
    repository,
    TodaGroupQuery(
      n=5,
      k=4,
    ),
  )

  final_entries = (
    repository.entries()
  )

  assert (
    final_entries
    == initial_entries
  )
  assert all(
    actual is expected
    for actual, expected in zip(
      final_entries,
      initial_entries,
    )
  )


def test_phase95_3_rejects_non_repository_via_existing_lookup_validation():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  with pytest.raises(
    TypeError,
    match=(
      "repository must be "
      "a ProofRepository"
    ),
  ):
    build_known_toda_calculation_result(
      "not-a-repository",
      query,
    )


def test_phase95_3_rejects_non_query_via_existing_lookup_validation():
  repository = ProofRepository()

  with pytest.raises(
    TypeError,
    match=(
      "query must be "
      "a TodaGroupQuery"
    ),
  ):
    build_known_toda_calculation_result(
      repository,
      "not-a-query",
    )
