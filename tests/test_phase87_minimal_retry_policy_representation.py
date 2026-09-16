from dataclasses import dataclass
from functools import lru_cache

import pytest

from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
  ProofStep,
  derive_inference_round_result,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  BoundedProducerSearchStatus,
  FiniteProducerRetryPolicy,
  build_depth_two_producer_search_report,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase87RetrySeedStatement:
  pass


@dataclass(frozen=True)
class Phase87RetryPremiseStatement:
  pass


@dataclass(frozen=True)
class Phase87RetryGoalStatement:
  pass


def _producer_rule(
  name,
  *,
  applicable,
):
  def guard(
    premises,
    bindings,
  ):
    return applicable

  return InferenceRule(
    name=name,
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=Phase87RetrySeedStatement,
      ),
    ),
    conclusion_builder=(
      lambda premises:
      Phase87RetryPremiseStatement()
    ),
    match_guard=guard,
  )


def _final_rule():
  return InferenceRule(
    name="phase87 retry final",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Phase87RetryPremiseStatement,
      ),
    ),
    conclusion_builder=(
      lambda premises:
      Phase87RetryGoalStatement()
    ),
  )


def _register_rule(
  catalog,
  key,
  rule,
  conclusion_type,
):
  catalog.register(
    InferenceRuleCatalogEntry(
      key=key,
      rule=rule,
      conclusion_type=conclusion_type,
      fixed_point_safe=True,
    )
  )


@lru_cache(maxsize=1)
def build_phase87_2_data():
  seed_step = ProofStep(
    conclusion=Phase87RetrySeedStatement(),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  repository = ProofRepository()

  repository.register(
    ProofRepositoryEntry(
      key="phase87.retry.seed",
      step=seed_step,
      phase="87",
      theorem=(
        "minimal producer retry policy"
      ),
    )
  )

  first_producer_rule = _producer_rule(
    "phase87 retry first producer",
    applicable=False,
  )
  second_producer_rule = _producer_rule(
    "phase87 retry second producer",
    applicable=True,
  )
  final_rule = _final_rule()

  catalog = InferenceRuleCatalog()

  _register_rule(
    catalog,
    "phase87.retry.first-producer",
    first_producer_rule,
    Phase87RetryPremiseStatement,
  )
  _register_rule(
    catalog,
    "phase87.retry.second-producer",
    second_producer_rule,
    Phase87RetryPremiseStatement,
  )
  _register_rule(
    catalog,
    "phase87.retry.final",
    final_rule,
    Phase87RetryGoalStatement,
  )

  return {
    "repository": repository,
    "catalog": catalog,
    "goal": Phase87RetryGoalStatement(),
    "seed_step": seed_step,
    "first_producer_rule": first_producer_rule,
    "second_producer_rule": second_producer_rule,
    "final_rule": final_rule,
    "retry_policy": FiniteProducerRetryPolicy(
      max_attempts=2,
    ),
  }


def test_phase87_2_retry_policy_accepts_positive_attempt_bound():
  policy = FiniteProducerRetryPolicy(
    max_attempts=2,
  )

  assert policy.max_attempts == 2


@pytest.mark.parametrize(
  "invalid_max_attempts",
  (
    True,
    False,
    1.0,
    "2",
    None,
  ),
)
def test_phase87_2_retry_policy_rejects_non_integer_attempt_bound(
  invalid_max_attempts,
):
  with pytest.raises(
    TypeError,
    match="max_attempts must be an int",
  ):
    FiniteProducerRetryPolicy(
      max_attempts=invalid_max_attempts,
    )


@pytest.mark.parametrize(
  "invalid_max_attempts",
  (
    0,
    -1,
  ),
)
def test_phase87_2_retry_policy_rejects_non_positive_attempt_bound(
  invalid_max_attempts,
):
  with pytest.raises(
    ValueError,
    match="max_attempts must be positive",
  ):
    FiniteProducerRetryPolicy(
      max_attempts=invalid_max_attempts,
    )


def test_phase87_2_fixture_has_explicit_two_attempt_policy():
  data = build_phase87_2_data()

  assert data[
    "retry_policy"
  ].max_attempts == 2


def test_phase87_2_fixture_preserves_catalog_candidate_order():
  data = build_phase87_2_data()

  report = build_depth_two_producer_search_report(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  assert report.status is (
    BoundedProducerSearchStatus
    .AMBIGUOUS_PRODUCER
  )
  assert report.search_result is None
  assert report.diagnostic is not None

  assert report.diagnostic.producer_candidates == (
    data[
      "first_producer_rule"
    ],
    data[
      "second_producer_rule"
    ],
  )


def test_phase87_2_first_candidate_is_not_applicable():
  data = build_phase87_2_data()

  initial_steps = repository_available_steps(
    data[
      "repository"
    ]
  )

  result = derive_inference_round_result(
    (
      data[
        "first_producer_rule"
      ],
    ),
    initial_steps,
  )

  assert not result.matches
  assert result.new_steps == ()


def test_phase87_2_second_candidate_is_applicable():
  data = build_phase87_2_data()

  initial_steps = repository_available_steps(
    data[
      "repository"
    ]
  )

  result = derive_inference_round_result(
    (
      data[
        "second_producer_rule"
      ],
    ),
    initial_steps,
  )

  assert result.matches
  assert len(
    result.new_steps
  ) == 1
  assert isinstance(
    result.new_steps[
      0
    ].conclusion,
    Phase87RetryPremiseStatement,
  )


def test_phase87_2_current_search_still_stops_at_ambiguity():
  data = build_phase87_2_data()

  report = build_depth_two_producer_search_report(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  assert report.status is (
    BoundedProducerSearchStatus
    .AMBIGUOUS_PRODUCER
  )
  assert report.search_result is None
  assert report.diagnostic is not None

  assert report.diagnostic.producer_candidates == (
    data[
      "first_producer_rule"
    ],
    data[
      "second_producer_rule"
    ],
  )


def test_phase87_2_fixture_and_search_do_not_mutate_repository():
  data = build_phase87_2_data()

  initial_steps = repository_available_steps(
    data[
      "repository"
    ]
  )

  report = build_depth_two_producer_search_report(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  assert report.status is (
    BoundedProducerSearchStatus
    .AMBIGUOUS_PRODUCER
  )

  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == initial_steps
