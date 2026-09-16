from dataclasses import dataclass
from functools import lru_cache

from proof import (
  InferenceRule,
  PremisePattern,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  BoundedProducerSearchStatus,
  build_depth_two_producer_search_report,
  execute_depth_two_producer_search,
  find_missing_premise_producer_lookups,
  repository_available_steps,
  select_unique_depth_two_producer_chain,
  detect_missing_premises,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
  find_premise_producer_rules,
)
from test_phase76_delta_iota17 import (
  build_phase76_4_data,
)
from test_phase88_goal_side_compatibility import (
  build_phase88_7_data,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
)


@dataclass(frozen=True)
class Phase88EndToEndGoal:
  delta_statement: object


@lru_cache(maxsize=1)
def build_phase88_17_data():
  phase76 = build_phase76_4_data()
  phase88 = build_phase88_7_data()

  requested_statement = phase76[
    "expected_final"
  ]

  goal = Phase88EndToEndGoal(
    delta_statement=requested_statement,
  )

  final_rule = InferenceRule(
    name=(
      "phase88 concrete-goal "
      "end-to-end final"
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaDeltaImageUpToSignStatement
        ),
        statement_pattern=(
          requested_statement
        ),
      ),
    ),
    conclusion_builder=(
      lambda premises:
      Phase88EndToEndGoal(
        delta_statement=(
          premises[0].conclusion
        ),
      )
    ),
  )

  catalog = InferenceRuleCatalog()

  for entry in phase88[
    "entries"
  ]:
    catalog.register(
      entry
    )

  final_entry = InferenceRuleCatalogEntry(
    key="phase88.end-to-end.final",
    rule=final_rule,
    conclusion_type=Phase88EndToEndGoal,
    fixed_point_safe=True,
    goal_compatibility=(
      lambda candidate_goal:
      candidate_goal == goal
    ),
  )
  catalog.register(
    final_entry
  )

  repository = ProofRepository()

  for index, step in enumerate(
    phase76[
      "initial_steps"
    ]
  ):
    repository.register(
      ProofRepositoryEntry(
        key=(
          "phase88.end-to-end."
          f"seed-{index}"
        ),
        step=step,
      )
    )

  initial_steps = (
    repository_available_steps(
      repository
    )
  )

  final_availability = (
    detect_missing_premises(
      final_rule,
      initial_steps,
    )
  )

  producer_lookups = (
    find_missing_premise_producer_lookups(
      final_availability,
      catalog,
    )
  )

  type_only_rules = (
    find_premise_producer_rules(
      catalog,
      final_rule.premise_patterns[0],
      requested_statement=None,
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

  report = (
    build_depth_two_producer_search_report(
      repository,
      catalog,
      goal,
      max_depth=2,
    )
  )

  execution = (
    execute_depth_two_producer_search(
      repository,
      catalog,
      goal,
      max_depth=2,
    )
  )

  return {
    "phase76": phase76,
    "phase88": phase88,
    "requested_statement": (
      requested_statement
    ),
    "goal": goal,
    "final_rule": final_rule,
    "final_entry": final_entry,
    "catalog": catalog,
    "repository": repository,
    "initial_steps": initial_steps,
    "final_availability": (
      final_availability
    ),
    "producer_lookups": (
      producer_lookups
    ),
    "type_only_rules": (
      type_only_rules
    ),
    "search_result": search_result,
    "report": report,
    "execution": execution,
  }


def test_phase88_17_realistic_collision_is_visible_before_concrete_filtering():
  data = build_phase88_17_data()

  assert data[
    "type_only_rules"
  ] == data[
    "phase88"
  ][
    "rules"
  ]


def test_phase88_17_concrete_requested_statement_eliminates_false_ambiguity():
  data = build_phase88_17_data()

  assert len(
    data[
      "producer_lookups"
    ]
  ) == 1

  lookup = data[
    "producer_lookups"
  ][0]

  assert (
    lookup.requested_statement
    == data[
      "requested_statement"
    ]
  )

  assert lookup.producer_rules == (
    data[
      "phase88"
    ][
      "rules"
    ][2],
  )


def test_phase88_17_selection_preserves_concrete_iota17_path():
  data = build_phase88_17_data()

  result = data[
    "search_result"
  ]

  assert result is not None
  assert result.goal == data[
    "goal"
  ]
  assert result.final_rule is data[
    "final_rule"
  ]
  assert len(
    result.producer_nodes
  ) == 1

  node = result.producer_nodes[
    0
  ]

  assert node.producer_rule is data[
    "phase88"
  ][
    "rules"
  ][2]

  assert (
    node.requested_statement
    == data[
      "requested_statement"
    ]
  )


def test_phase88_17_report_is_successful_without_retry():
  data = build_phase88_17_data()

  report = data[
    "report"
  ]

  assert report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )
  assert report.diagnostic is None
  assert report.search_result is not None
  assert (
    report.search_result
    .producer_nodes[0]
    .producer_rule
    is data[
      "phase88"
    ][
      "rules"
    ][2]
  )


def test_phase88_17_execution_derives_concrete_goal():
  data = build_phase88_17_data()

  execution = data[
    "execution"
  ]

  assert execution.report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  inference_result = (
    execution.repository_inference_result
  )

  assert inference_result is not None
  assert inference_result.goal_step is not None
  assert (
    inference_result.goal_step.conclusion
    == data[
      "goal"
    ]
  )


def test_phase88_17_execution_provenance_uses_selected_iota17_rule():
  data = build_phase88_17_data()

  inference_result = (
    data[
      "execution"
    ].repository_inference_result
  )

  assert inference_result is not None

  producer_step = next(
    step
    for step in (
      inference_result
      .inference_result
      .steps
    )
    if (
      step.conclusion
      == data[
        "requested_statement"
      ]
    )
  )

  assert producer_step.inference_rule is (
    data[
      "phase88"
    ][
      "rules"
    ][2]
  )

  goal_step = inference_result.goal_step

  assert goal_step is not None
  assert goal_step.inference_rule is data[
    "final_rule"
  ]
  assert producer_step in goal_step.premises


def test_phase88_17_unrelated_collision_rules_are_not_selected():
  data = build_phase88_17_data()

  selected_rules = tuple(
    node.producer_rule
    for node in (
      data[
        "search_result"
      ].producer_nodes
    )
  )

  assert data[
    "phase88"
  ][
    "rules"
  ][0] not in selected_rules

  assert data[
    "phase88"
  ][
    "rules"
  ][1] not in selected_rules


def test_phase88_17_execution_does_not_mutate_repository():
  data = build_phase88_17_data()

  assert (
    repository_available_steps(
      data[
        "repository"
      ]
    )
    == data[
      "initial_steps"
    ]
  )

  assert all(
    step.conclusion
    != data[
      "requested_statement"
    ]
    for step in data[
      "initial_steps"
    ]
  )

  assert all(
    step.conclusion
    != data[
      "goal"
    ]
    for step in data[
      "initial_steps"
    ]
  )
