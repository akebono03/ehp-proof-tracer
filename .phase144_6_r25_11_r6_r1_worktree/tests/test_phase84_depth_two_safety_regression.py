from copy import copy
from dataclasses import dataclass, replace

from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
)
from proof_repository import ProofRepository
from repository_inference import (
  derive_goal_from_repository_with_depth_two_producers,
  repository_available_steps,
  select_unique_depth_two_producer_chain,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from test_phase84_bounded_depth_two_execution import (
  Phase84ExecutionGoalStatement,
  Phase84ExecutionIntermediateStatement,
  Phase84ExecutionSharedStatement,
  build_phase84_5_data,
)


@dataclass(frozen=True)
class Phase84SafetyAStatement:
  pass


@dataclass(frozen=True)
class Phase84SafetyBStatement:
  pass


@dataclass(frozen=True)
class Phase84SafetyCStatement:
  pass


@dataclass(frozen=True)
class Phase84SafetyGoalStatement:
  pass


def _register_rule(
  catalog,
  key,
  rule,
  conclusion_type,
  fixed_point_safe=True,
):
  catalog.register(
    InferenceRuleCatalogEntry(
      key=key,
      rule=rule,
      conclusion_type=conclusion_type,
      fixed_point_safe=fixed_point_safe,
    )
  )


def _base_catalog(
  data,
  shared_rules,
  final_rules=None,
  shared_safe=True,
):
  catalog = InferenceRuleCatalog()

  if final_rules is None:
    final_rules = (
      data[
        "final_rule"
      ],
    )

  for index, final_rule in enumerate(
    final_rules
  ):
    _register_rule(
      catalog,
      f"phase84.safety.final-{index}",
      final_rule,
      Phase84ExecutionGoalStatement,
    )

  _register_rule(
    catalog,
    "phase84.safety.intermediate",
    data[
      "intermediate_rule"
    ],
    Phase84ExecutionIntermediateStatement,
  )

  for index, shared_rule in enumerate(
    shared_rules
  ):
    _register_rule(
      catalog,
      f"phase84.safety.shared-{index}",
      shared_rule,
      Phase84ExecutionSharedStatement,
      fixed_point_safe=shared_safe,
    )

  return catalog


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
      lambda premises: conclusion_type()
    ),
  )


def _empty_safety_repository():
  return ProofRepository()


def test_phase84_7_missing_direct_producer_stops_selection():
  data = build_phase84_5_data()

  catalog = _base_catalog(
    data,
    (),
  )

  assert (
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      catalog,
      data[
        "goal"
      ],
    )
    is None
  )

  result = (
    derive_goal_from_repository_with_depth_two_producers(
      data[
        "repository"
      ],
      catalog,
      data[
        "goal"
      ],
    )
  )

  assert result.goal_step is None


def test_phase84_7_unsafe_producer_is_not_selected():
  data = build_phase84_5_data()

  catalog = _base_catalog(
    data,
    (
      data[
        "shared_rule"
      ],
    ),
    shared_safe=False,
  )

  assert (
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      catalog,
      data[
        "goal"
      ],
    )
    is None
  )


def test_phase84_7_distinct_direct_producer_ambiguity_stops():
  data = build_phase84_5_data()

  second_shared_rule = copy(
    data[
      "shared_rule"
    ]
  )

  assert (
    second_shared_rule
    is not data[
      "shared_rule"
    ]
  )

  catalog = _base_catalog(
    data,
    (
      data[
        "shared_rule"
      ],
      second_shared_rule,
    ),
  )

  assert (
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      catalog,
      data[
        "goal"
      ],
    )
    is None
  )


def test_phase84_7_distinct_final_rule_ambiguity_stops():
  data = build_phase84_5_data()

  second_final_rule = copy(
    data[
      "final_rule"
    ]
  )

  catalog = _base_catalog(
    data,
    (
      data[
        "shared_rule"
      ],
    ),
    final_rules=(
      data[
        "final_rule"
      ],
      second_final_rule,
    ),
  )

  assert (
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      catalog,
      data[
        "goal"
      ],
    )
    is None
  )


def test_phase84_7_distinct_nested_producer_ambiguity_stops():
  data = build_phase84_5_data()

  final_rule = InferenceRule(
    name="phase84 nested ambiguity final",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Phase84ExecutionIntermediateStatement
        ),
      ),
    ),
    conclusion_builder=(
      lambda premises: (
        Phase84ExecutionGoalStatement(
          name=(
            premises[
              0
            ].conclusion.name
          ),
        )
      )
    ),
  )

  second_shared_rule = copy(
    data[
      "shared_rule"
    ]
  )

  catalog = _base_catalog(
    data,
    (
      data[
        "shared_rule"
      ],
      second_shared_rule,
    ),
    final_rules=(
      final_rule,
    ),
  )

  assert (
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      catalog,
      data[
        "goal"
      ],
    )
    is None
  )


def test_phase84_7_alias_duplicate_preserves_unique_chain():
  data = build_phase84_5_data()

  catalog = _base_catalog(
    data,
    (
      data[
        "shared_rule"
      ],
      data[
        "shared_rule"
      ],
    ),
  )

  search_result = (
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      catalog,
      data[
        "goal"
      ],
    )
  )

  assert search_result is not None

  assert len(
    search_result.producer_nodes
  ) == 2

  result = (
    derive_goal_from_repository_with_depth_two_producers(
      data[
        "repository"
      ],
      catalog,
      data[
        "goal"
      ],
    )
  )

  assert result.goal_step is not None

  shared_steps = tuple(
    step
    for step in result.inference_result.steps
    if isinstance(
      step.conclusion,
      Phase84ExecutionSharedStatement,
    )
  )

  assert len(
    shared_steps
  ) == 1


def test_phase84_7_cycle_shaped_catalog_stops():
  repository = _empty_safety_repository()

  final_rule = _single_premise_rule(
    "phase84 cycle final",
    Phase84SafetyAStatement,
    Phase84SafetyGoalStatement,
  )
  a_rule = _single_premise_rule(
    "phase84 cycle a",
    Phase84SafetyBStatement,
    Phase84SafetyAStatement,
  )
  b_rule = _single_premise_rule(
    "phase84 cycle b",
    Phase84SafetyAStatement,
    Phase84SafetyBStatement,
  )

  catalog = InferenceRuleCatalog()

  for key, rule, conclusion_type in (
    (
      "phase84.cycle.final",
      final_rule,
      Phase84SafetyGoalStatement,
    ),
    (
      "phase84.cycle.a",
      a_rule,
      Phase84SafetyAStatement,
    ),
    (
      "phase84.cycle.b",
      b_rule,
      Phase84SafetyBStatement,
    ),
  ):
    _register_rule(
      catalog,
      key,
      rule,
      conclusion_type,
    )

  goal = Phase84SafetyGoalStatement()

  assert (
    select_unique_depth_two_producer_chain(
      repository,
      catalog,
      goal,
    )
    is None
  )

  result = (
    derive_goal_from_repository_with_depth_two_producers(
      repository,
      catalog,
      goal,
    )
  )

  assert result.goal_step is None
  assert result.inference_result.steps == ()


def test_phase84_7_depth_three_requirement_stops_at_limit():
  repository = _empty_safety_repository()

  final_rule = _single_premise_rule(
    "phase84 depth final",
    Phase84SafetyAStatement,
    Phase84SafetyGoalStatement,
  )
  a_rule = _single_premise_rule(
    "phase84 depth a",
    Phase84SafetyBStatement,
    Phase84SafetyAStatement,
  )
  b_rule = _single_premise_rule(
    "phase84 depth b",
    Phase84SafetyCStatement,
    Phase84SafetyBStatement,
  )
  c_rule = InferenceRule(
    name="phase84 depth c",
    premise_patterns=(),
    conclusion_builder=(
      lambda premises: (
        Phase84SafetyCStatement()
      )
    ),
  )

  catalog = InferenceRuleCatalog()

  for key, rule, conclusion_type in (
    (
      "phase84.depth.final",
      final_rule,
      Phase84SafetyGoalStatement,
    ),
    (
      "phase84.depth.a",
      a_rule,
      Phase84SafetyAStatement,
    ),
    (
      "phase84.depth.b",
      b_rule,
      Phase84SafetyBStatement,
    ),
    (
      "phase84.depth.c",
      c_rule,
      Phase84SafetyCStatement,
    ),
  ):
    _register_rule(
      catalog,
      key,
      rule,
      conclusion_type,
    )

  goal = Phase84SafetyGoalStatement()

  assert (
    select_unique_depth_two_producer_chain(
      repository,
      catalog,
      goal,
    )
    is None
  )

  result = (
    derive_goal_from_repository_with_depth_two_producers(
      repository,
      catalog,
      goal,
    )
  )

  assert result.goal_step is None
  assert result.inference_result.steps == ()


def test_phase84_7_partial_execution_does_not_create_goal():
  data = build_phase84_5_data()

  blocked_shared_rule = replace(
    data[
      "shared_rule"
    ],
    name="phase84 blocked shared producer",
    match_guard=(
      lambda premises, bindings: False
    ),
  )

  catalog = _base_catalog(
    data,
    (
      blocked_shared_rule,
    ),
  )

  search_result = (
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      catalog,
      data[
        "goal"
      ],
    )
  )

  assert search_result is not None

  result = (
    derive_goal_from_repository_with_depth_two_producers(
      data[
        "repository"
      ],
      catalog,
      data[
        "goal"
      ],
    )
  )

  assert result.goal_step is None

  assert (
    result.inference_result.steps
    == data[
      "initial_steps"
    ]
  )


def test_phase84_7_failed_searches_do_not_mutate_repository():
  data = build_phase84_5_data()

  catalog = _base_catalog(
    data,
    (),
  )

  initial_steps = repository_available_steps(
    data[
      "repository"
    ]
  )

  derive_goal_from_repository_with_depth_two_producers(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  assert (
    repository_available_steps(
      data[
        "repository"
      ]
    )
    == initial_steps
  )
