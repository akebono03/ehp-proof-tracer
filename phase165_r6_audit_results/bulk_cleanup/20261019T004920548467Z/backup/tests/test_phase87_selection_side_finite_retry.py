from dataclasses import dataclass
from functools import lru_cache

import pytest

from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
)
from proof_repository import ProofRepository
from repository_inference import (
  FiniteProducerRetryPolicy,
  repository_available_steps,
  select_unique_depth_two_producer_chain,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase87SelectionAStatement:
  pass


@dataclass(frozen=True)
class Phase87SelectionBStatement:
  pass


@dataclass(frozen=True)
class Phase87SelectionCStatement:
  pass


@dataclass(frozen=True)
class Phase87SelectionGoalStatement:
  pass


def _single_premise_rule(
  name,
  premise_type,
  conclusion_type,
):
  return InferenceRule(
    name=name,
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=premise_type,
      ),
    ),
    conclusion_builder=(
      lambda premises:
      conclusion_type()
    ),
  )


def _no_premise_rule(
  name,
  conclusion_type,
):
  return InferenceRule(
    name=name,
    premise_patterns=(),
    conclusion_builder=(
      lambda premises:
      conclusion_type()
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
def build_phase87_3_data():
  repository = ProofRepository()

  final_rule = _single_premise_rule(
    "phase87 selection final",
    Phase87SelectionAStatement,
    Phase87SelectionGoalStatement,
  )

  first_a_rule = _single_premise_rule(
    "phase87 selection first a",
    Phase87SelectionBStatement,
    Phase87SelectionAStatement,
  )

  second_a_rule = _no_premise_rule(
    "phase87 selection second a",
    Phase87SelectionAStatement,
  )

  b_rule = _single_premise_rule(
    "phase87 selection b",
    Phase87SelectionCStatement,
    Phase87SelectionBStatement,
  )

  c_rule = _no_premise_rule(
    "phase87 selection c",
    Phase87SelectionCStatement,
  )

  catalog = InferenceRuleCatalog()

  for key, rule, conclusion_type in (
    (
      "phase87.selection.final",
      final_rule,
      Phase87SelectionGoalStatement,
    ),
    (
      "phase87.selection.first-a",
      first_a_rule,
      Phase87SelectionAStatement,
    ),
    (
      "phase87.selection.second-a",
      second_a_rule,
      Phase87SelectionAStatement,
    ),
    (
      "phase87.selection.b",
      b_rule,
      Phase87SelectionBStatement,
    ),
    (
      "phase87.selection.c",
      c_rule,
      Phase87SelectionCStatement,
    ),
  ):
    _register_rule(
      catalog,
      key,
      rule,
      conclusion_type,
    )

  return {
    "repository": repository,
    "catalog": catalog,
    "goal": Phase87SelectionGoalStatement(),
    "final_rule": final_rule,
    "first_a_rule": first_a_rule,
    "second_a_rule": second_a_rule,
    "b_rule": b_rule,
    "c_rule": c_rule,
  }


def test_phase87_3_without_retry_policy_preserves_unique_producer_semantics():
  data = build_phase87_3_data()

  result = select_unique_depth_two_producer_chain(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=2,
  )

  assert result is None


def test_phase87_3_one_attempt_stops_after_first_selection_failure():
  data = build_phase87_3_data()

  result = select_unique_depth_two_producer_chain(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=2,
    retry_policy=FiniteProducerRetryPolicy(
      max_attempts=1,
    ),
  )

  assert result is None


def test_phase87_3_two_attempts_select_second_candidate_after_first_fails():
  data = build_phase87_3_data()

  result = select_unique_depth_two_producer_chain(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=2,
    retry_policy=FiniteProducerRetryPolicy(
      max_attempts=2,
    ),
  )

  assert result is not None
  assert result.max_depth == 2

  assert tuple(
    node.producer_rule
    for node in result.producer_nodes
  ) == (
    data[
      "second_a_rule"
    ],
  )

  assert result.producer_nodes[
    0
  ].depths == (
    1,
  )

  assert result.producer_nodes[
    0
  ].dependencies == ()


def test_phase87_3_failed_first_candidate_does_not_leak_into_selected_path():
  data = build_phase87_3_data()

  result = select_unique_depth_two_producer_chain(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=2,
    retry_policy=FiniteProducerRetryPolicy(
      max_attempts=2,
    ),
  )

  assert result is not None

  selected_rules = tuple(
    node.producer_rule
    for node in result.producer_nodes
  )

  assert data[
    "first_a_rule"
  ] not in selected_rules
  assert data[
    "b_rule"
  ] not in selected_rules
  assert data[
    "c_rule"
  ] not in selected_rules


def test_phase87_3_retry_uses_catalog_registration_order():
  data = build_phase87_3_data()

  one_attempt = (
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
      max_depth=2,
      retry_policy=FiniteProducerRetryPolicy(
        max_attempts=1,
      ),
    )
  )

  two_attempts = (
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
      max_depth=2,
      retry_policy=FiniteProducerRetryPolicy(
        max_attempts=2,
      ),
    )
  )

  assert one_attempt is None
  assert two_attempts is not None
  assert tuple(
    node.producer_rule
    for node in two_attempts.producer_nodes
  ) == (
    data[
      "second_a_rule"
    ],
  )


def test_phase87_3_retry_selection_preserves_repository():
  data = build_phase87_3_data()

  initial_steps = repository_available_steps(
    data[
      "repository"
    ]
  )

  result = select_unique_depth_two_producer_chain(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=2,
    retry_policy=FiniteProducerRetryPolicy(
      max_attempts=2,
    ),
  )

  assert result is not None

  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == initial_steps


@pytest.mark.parametrize(
  "invalid_retry_policy",
  (
    1,
    "retry",
    object(),
  ),
)
def test_phase87_3_selection_rejects_invalid_retry_policy(
  invalid_retry_policy,
):
  data = build_phase87_3_data()

  with pytest.raises(
    TypeError,
    match=(
      "retry_policy must be a "
      "FiniteProducerRetryPolicy or None"
    ),
  ):
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
      retry_policy=invalid_retry_policy,
    )
