from dataclasses import dataclass
from functools import lru_cache

from proof import (
  InferenceRule,
  PremisePattern,
)
from proof_repository import ProofRepository
from repository_inference import (
  BoundedProducerSearchStatus,
  diagnose_depth_two_producer_search_failure,
  diagnose_direct_producer_failure,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase88UnsafeGoal:
  value: str


@dataclass(frozen=True)
class Phase88UnsafeIntermediate:
  value: str


@dataclass(frozen=True)
class Phase88UnsafeTarget:
  value: str


def _register(
  catalog,
  key,
  rule,
  conclusion_type,
  *,
  fixed_point_safe,
  goal_compatibility=None,
):
  catalog.register(
    InferenceRuleCatalogEntry(
      key=key,
      rule=rule,
      conclusion_type=conclusion_type,
      fixed_point_safe=fixed_point_safe,
      goal_compatibility=goal_compatibility,
    )
  )


def _target_rule(
  name,
):
  return InferenceRule(
    name=name,
  )


def _target_compatibility(
  expected_value,
):
  return (
    lambda goal:
    isinstance(
      goal,
      Phase88UnsafeTarget,
    )
    and goal.value
    == expected_value
  )


@lru_cache(maxsize=1)
def build_phase88_13_direct_data():
  goal = Phase88UnsafeGoal(
    value="goal",
  )
  requested_target = Phase88UnsafeTarget(
    value="iota17",
  )

  final_rule = InferenceRule(
    name="phase88 direct final",
    premise_patterns=(
      PremisePattern(
        statement_type=Phase88UnsafeTarget,
        statement_pattern=requested_target,
      ),
    ),
  )

  target_rules = (
    _target_rule(
      "phase88 unsafe iota5"
    ),
    _target_rule(
      "phase88 unsafe iota9"
    ),
    _target_rule(
      "phase88 unsafe iota17"
    ),
  )

  catalog = InferenceRuleCatalog()

  _register(
    catalog,
    "phase88.direct.final",
    final_rule,
    Phase88UnsafeGoal,
    fixed_point_safe=True,
  )

  for key, rule, value in zip(
    (
      "phase88.direct.iota5",
      "phase88.direct.iota9",
      "phase88.direct.iota17",
    ),
    target_rules,
    (
      "iota5",
      "iota9",
      "iota17",
    ),
  ):
    _register(
      catalog,
      key,
      rule,
      Phase88UnsafeTarget,
      fixed_point_safe=False,
      goal_compatibility=(
        _target_compatibility(
          value
        )
      ),
    )

  return {
    "repository": ProofRepository(),
    "goal": goal,
    "requested_target": requested_target,
    "final_rule": final_rule,
    "target_rules": target_rules,
    "catalog": catalog,
  }


@lru_cache(maxsize=1)
def build_phase88_13_nested_data():
  goal = Phase88UnsafeGoal(
    value="goal",
  )
  intermediate = Phase88UnsafeIntermediate(
    value="mid",
  )
  requested_target = Phase88UnsafeTarget(
    value="iota17",
  )

  final_rule = InferenceRule(
    name="phase88 nested final",
    premise_patterns=(
      PremisePattern(
        statement_type=(
          Phase88UnsafeIntermediate
        ),
        statement_pattern=intermediate,
      ),
    ),
  )

  intermediate_rule = InferenceRule(
    name="phase88 nested intermediate",
    premise_patterns=(
      PremisePattern(
        statement_type=Phase88UnsafeTarget,
        statement_pattern=requested_target,
      ),
    ),
  )

  target_rules = (
    _target_rule(
      "phase88 nested unsafe iota5"
    ),
    _target_rule(
      "phase88 nested unsafe iota9"
    ),
    _target_rule(
      "phase88 nested unsafe iota17"
    ),
  )

  catalog = InferenceRuleCatalog()

  _register(
    catalog,
    "phase88.nested.final",
    final_rule,
    Phase88UnsafeGoal,
    fixed_point_safe=True,
  )

  _register(
    catalog,
    "phase88.nested.intermediate",
    intermediate_rule,
    Phase88UnsafeIntermediate,
    fixed_point_safe=True,
  )

  for key, rule, value in zip(
    (
      "phase88.nested.iota5",
      "phase88.nested.iota9",
      "phase88.nested.iota17",
    ),
    target_rules,
    (
      "iota5",
      "iota9",
      "iota17",
    ),
  ):
    _register(
      catalog,
      key,
      rule,
      Phase88UnsafeTarget,
      fixed_point_safe=False,
      goal_compatibility=(
        _target_compatibility(
          value
        )
      ),
    )

  return {
    "repository": ProofRepository(),
    "goal": goal,
    "intermediate": intermediate,
    "requested_target": requested_target,
    "final_rule": final_rule,
    "intermediate_rule": intermediate_rule,
    "target_rules": target_rules,
    "catalog": catalog,
  }


def test_phase88_13_direct_unsafe_diagnostic_keeps_only_compatible_instance():
  data = build_phase88_13_direct_data()

  diagnostic = diagnose_direct_producer_failure(
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

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus
    .UNSAFE_PRODUCER
  )
  assert diagnostic.producer_candidates == ()
  assert (
    diagnostic.unsafe_producer_candidates
    == (
      data[
        "target_rules"
      ][2],
    )
  )


def test_phase88_13_direct_unsafe_diagnostic_preserves_requested_context():
  data = build_phase88_13_direct_data()

  diagnostic = diagnose_direct_producer_failure(
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

  assert diagnostic is not None
  assert diagnostic.requesting_rule is data[
    "final_rule"
  ]
  assert diagnostic.premise_index == 0
  assert (
    diagnostic.premise_pattern
    is data[
      "final_rule"
    ].premise_patterns[0]
  )
  assert diagnostic.current_depth == 0
  assert diagnostic.required_next_depth == 1


def test_phase88_13_nested_unsafe_diagnostic_keeps_only_compatible_instance():
  data = build_phase88_13_nested_data()

  diagnostic = (
    diagnose_depth_two_producer_search_failure(
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
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus
    .UNSAFE_PRODUCER
  )
  assert diagnostic.producer_candidates == ()
  assert (
    diagnostic.unsafe_producer_candidates
    == (
      data[
        "target_rules"
      ][2],
    )
  )


def test_phase88_13_nested_unsafe_diagnostic_preserves_depth_context():
  data = build_phase88_13_nested_data()

  diagnostic = (
    diagnose_depth_two_producer_search_failure(
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
  )

  assert diagnostic is not None
  assert diagnostic.requesting_rule is data[
    "intermediate_rule"
  ]
  assert diagnostic.premise_index == 0
  assert (
    diagnostic.premise_pattern
    is data[
      "intermediate_rule"
    ].premise_patterns[0]
  )
  assert diagnostic.current_depth == 1
  assert diagnostic.required_next_depth == 2
  assert diagnostic.ancestor_rules == (
    data[
      "final_rule"
    ],
    data[
      "intermediate_rule"
    ],
  )


def test_phase88_13_unrelated_unsafe_instances_are_not_reported():
  direct = build_phase88_13_direct_data()
  nested = build_phase88_13_nested_data()

  direct_diagnostic = (
    diagnose_direct_producer_failure(
      direct[
        "repository"
      ],
      direct[
        "catalog"
      ],
      direct[
        "goal"
      ],
    )
  )

  nested_diagnostic = (
    diagnose_depth_two_producer_search_failure(
      nested[
        "repository"
      ],
      nested[
        "catalog"
      ],
      nested[
        "goal"
      ],
      max_depth=2,
    )
  )

  assert direct_diagnostic is not None
  assert nested_diagnostic is not None

  unrelated_direct = direct[
    "target_rules"
  ][:2]

  unrelated_nested = nested[
    "target_rules"
  ][:2]

  assert all(
    rule
    not in direct_diagnostic
    .unsafe_producer_candidates
    for rule in unrelated_direct
  )

  assert all(
    rule
    not in nested_diagnostic
    .unsafe_producer_candidates
    for rule in unrelated_nested
  )
