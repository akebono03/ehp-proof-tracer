from dataclasses import dataclass
from functools import lru_cache

from proof import (
  InferenceRule,
  PatternVariable,
  PremisePattern,
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  BoundedProducerSearchNode,
  BoundedProducerSearchStatus,
  build_depth_two_producer_search_report,
  diagnose_depth_two_producer_execution_failure,
  select_unique_depth_two_producer_chain,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase88KnownStatement:
  value: object


@dataclass(frozen=True)
class Phase88TargetStatement:
  value: object


@dataclass(frozen=True)
class Phase88GoalStatement:
  value: object


@lru_cache(maxsize=1)
def build_phase88_15_data():
  variable = PatternVariable(
    name="phase88.execution.value",
  )

  known_pattern = PremisePattern(
    statement_type=Phase88KnownStatement,
    statement_pattern=Phase88KnownStatement(
      value=variable,
    ),
  )

  target_pattern = PremisePattern(
    statement_type=Phase88TargetStatement,
    statement_pattern=Phase88TargetStatement(
      value=variable,
    ),
  )

  final_rule = InferenceRule(
    name="phase88 concrete execution final",
    premise_patterns=(
      known_pattern,
      target_pattern,
    ),
    conclusion_builder=(
      lambda premises:
      Phase88GoalStatement(
        value=premises[0].conclusion.value,
      )
    ),
  )

  producer_rule = InferenceRule(
    name="phase88 wrong concrete producer",
    conclusion_builder=(
      lambda premises:
      Phase88TargetStatement(
        value="wrong",
      )
    ),
  )

  known_step = ProofStep(
    conclusion=Phase88KnownStatement(
      value="wanted",
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  repository = ProofRepository()
  repository.register(
    ProofRepositoryEntry(
      key="phase88.known",
      step=known_step,
    )
  )

  goal = Phase88GoalStatement(
    value="wanted",
  )
  requested_statement = (
    Phase88TargetStatement(
      value="wanted",
    )
  )

  catalog = InferenceRuleCatalog()
  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase88.final",
      rule=final_rule,
      conclusion_type=Phase88GoalStatement,
      fixed_point_safe=True,
      goal_compatibility=(
        lambda candidate_goal:
        candidate_goal == goal
      ),
    )
  )
  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase88.producer",
      rule=producer_rule,
      conclusion_type=Phase88TargetStatement,
      fixed_point_safe=True,
      goal_compatibility=(
        lambda candidate_goal:
        candidate_goal
        == requested_statement
      ),
    )
  )

  search_result = (
    select_unique_depth_two_producer_chain(
      repository,
      catalog,
      goal,
      max_depth=2,
    )
  )

  return {
    "variable": variable,
    "known_pattern": known_pattern,
    "target_pattern": target_pattern,
    "final_rule": final_rule,
    "producer_rule": producer_rule,
    "known_step": known_step,
    "repository": repository,
    "goal": goal,
    "requested_statement": (
      requested_statement
    ),
    "catalog": catalog,
    "search_result": search_result,
  }


def test_phase88_15_selected_node_preserves_concrete_requested_statement():
  data = build_phase88_15_data()

  assert data[
    "search_result"
  ] is not None

  node = data[
    "search_result"
  ].producer_nodes[0]

  assert (
    node.requested_statement
    == data[
      "requested_statement"
    ]
  )


def test_phase88_15_selected_node_preserves_original_premise_pattern():
  data = build_phase88_15_data()

  node = data[
    "search_result"
  ].producer_nodes[0]

  assert (
    node.premise_pattern
    is data[
      "target_pattern"
    ]
  )


def test_phase88_15_wrong_concrete_output_is_rejected_at_producer_node():
  data = build_phase88_15_data()

  diagnostic = (
    diagnose_depth_two_producer_execution_failure(
      data[
        "repository"
      ],
      data[
        "search_result"
      ],
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus
    .PRODUCER_OUTPUT_NOT_USABLE
  )
  assert diagnostic.requesting_rule is data[
    "final_rule"
  ]
  assert diagnostic.premise_index == 1
  assert (
    diagnostic.producer_candidates
    == (
      data[
        "producer_rule"
      ],
    )
  )


def test_phase88_15_report_classifies_wrong_instance_as_output_not_usable():
  data = build_phase88_15_data()

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
    max_depth=2,
  )

  assert report.status is (
    BoundedProducerSearchStatus
    .PRODUCER_OUTPUT_NOT_USABLE
  )
  assert report.search_result is not None
  assert report.diagnostic is not None
  assert (
    report.search_result
    .producer_nodes[0]
    .requested_statement
    == data[
      "requested_statement"
    ]
  )


def test_phase88_15_node_default_preserves_backward_compatibility():
  data = build_phase88_15_data()

  node = BoundedProducerSearchNode(
    requesting_rule=data[
      "final_rule"
    ],
    premise_index=1,
    premise_pattern=data[
      "target_pattern"
    ],
    producer_rule=data[
      "producer_rule"
    ],
    producer_availability=(
      data[
        "search_result"
      ].producer_nodes[
        0
      ].producer_availability
    ),
    depths=(
      1,
    ),
  )

  assert (
    node.requested_statement
    is None
  )
