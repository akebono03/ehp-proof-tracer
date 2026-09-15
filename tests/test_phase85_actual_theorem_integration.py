from functools import lru_cache

from proof import ProofRule
from repository_inference import (
  BoundedProducerSearchStatus,
  execute_depth_two_producer_search,
  repository_available_steps,
)
from test_phase84_producer_premise_availability import (
  build_phase84_3_data,
)
from toda_rules import (
  Toda36Lemma516BracketSumContainmentStatement,
  TodaLemma516BracketSumContainmentStatement,
  TodaLemma516ScaledCompositionBridgeStatement,
)


def _collect_ancestors(
  step,
):
  ancestors = []
  seen = set()
  stack = list(
    step.premises
  )

  while stack:
    current = stack.pop()
    current_id = id(
      current
    )

    if current_id in seen:
      continue

    seen.add(
      current_id
    )
    ancestors.append(
      current
    )
    stack.extend(
      current.premises
    )

  return tuple(
    ancestors
  )


@lru_cache(maxsize=1)
def build_phase85_8_data():
  phase84_3 = build_phase84_3_data()

  repository = phase84_3[
    "repository"
  ]
  catalog = phase84_3[
    "catalog"
  ]
  goal = phase84_3[
    "goal"
  ]
  initial_steps = repository_available_steps(
    repository
  )

  result = execute_depth_two_producer_search(
    repository,
    catalog,
    goal,
  )

  assert result.report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  search_result = result.report.search_result

  assert search_result is not None

  repository_result = (
    result.repository_inference_result
  )

  assert repository_result is not None

  final_step = repository_result.goal_step

  assert final_step is not None

  bracket_sum_step = next(
    step
    for step
    in repository_result.inference_result.steps
    if isinstance(
      step.conclusion,
      Toda36Lemma516BracketSumContainmentStatement,
    )
  )

  composition_step = next(
    step
    for step
    in repository_result.inference_result.steps
    if isinstance(
      step.conclusion,
      TodaLemma516ScaledCompositionBridgeStatement,
    )
  )

  bracket_sum_node = next(
    node
    for node
    in search_result.producer_nodes
    if (
      node.producer_rule
      is phase84_3[
        "bracket_sum_rule"
      ]
    )
  )

  composition_node = next(
    node
    for node
    in search_result.producer_nodes
    if (
      node.producer_rule
      is phase84_3[
        "composition_rule"
      ]
    )
  )

  return {
    "phase84_3": phase84_3,
    "repository": repository,
    "catalog": catalog,
    "goal": goal,
    "initial_steps": initial_steps,
    "result": result,
    "report": result.report,
    "search_result": search_result,
    "repository_result": repository_result,
    "bracket_sum_node": bracket_sum_node,
    "composition_node": composition_node,
    "bracket_sum_step": bracket_sum_step,
    "composition_step": composition_step,
    "final_step": final_step,
    "ancestors": _collect_ancestors(
      final_step
    ),
  }


def test_phase85_8_actual_goal_is_not_initially_available():
  data = build_phase85_8_data()

  assert all(
    step.conclusion
    != data[
      "goal"
    ]
    for step
    in data[
      "initial_steps"
    ]
  )


def test_phase85_8_integrated_report_is_successful():
  data = build_phase85_8_data()

  assert data[
    "report"
  ].status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  assert data[
    "report"
  ].diagnostic is None

  assert (
    data[
      "report"
    ].search_result
    is data[
      "search_result"
    ]
  )


def test_phase85_8_integrated_search_selects_actual_rules():
  data = build_phase85_8_data()

  assert (
    data[
      "search_result"
    ].final_rule
    is data[
      "phase84_3"
    ][
      "final_rule"
    ]
  )

  assert tuple(
    node.producer_rule
    for node
    in data[
      "search_result"
    ].producer_nodes
  ) == (
    data[
      "phase84_3"
    ][
      "bracket_sum_rule"
    ],
    data[
      "phase84_3"
    ][
      "composition_rule"
    ],
  )


def test_phase85_8_actual_shared_dependency_is_preserved():
  data = build_phase85_8_data()

  bracket_sum_node = data[
    "bracket_sum_node"
  ]
  composition_node = data[
    "composition_node"
  ]

  assert bracket_sum_node.depths == (
    1,
    2,
  )

  assert bracket_sum_node.is_shared

  assert composition_node.dependencies == (
    bracket_sum_node,
  )


def test_phase85_8_derives_actual_bracket_sum():
  data = build_phase85_8_data()

  step = data[
    "bracket_sum_step"
  ]

  assert isinstance(
    step.conclusion,
    Toda36Lemma516BracketSumContainmentStatement,
  )

  assert step.rule == ProofRule.INFERENCE

  assert (
    step.inference_rule
    is data[
      "phase84_3"
    ][
      "bracket_sum_rule"
    ]
  )


def test_phase85_8_derives_actual_composition_bridge():
  data = build_phase85_8_data()

  step = data[
    "composition_step"
  ]

  assert isinstance(
    step.conclusion,
    TodaLemma516ScaledCompositionBridgeStatement,
  )

  assert step.rule == ProofRule.INFERENCE

  assert (
    step.inference_rule
    is data[
      "phase84_3"
    ][
      "composition_rule"
    ]
  )


def test_phase85_8_derives_actual_toda_lemma516_goal():
  data = build_phase85_8_data()

  step = data[
    "final_step"
  ]

  assert isinstance(
    step.conclusion,
    TodaLemma516BracketSumContainmentStatement,
  )

  assert step.conclusion == data[
    "goal"
  ]

  assert step.rule == ProofRule.INFERENCE

  assert (
    step.inference_rule
    is data[
      "phase84_3"
    ][
      "final_rule"
    ]
  )


def test_phase85_8_final_uses_both_generated_actual_steps():
  data = build_phase85_8_data()

  assert data[
    "final_step"
  ].premises == (
    data[
      "bracket_sum_step"
    ],
    data[
      "composition_step"
    ],
  )


def test_phase85_8_shared_bracket_sum_proof_step_is_reused():
  data = build_phase85_8_data()

  assert (
    data[
      "final_step"
    ].premises[
      0
    ]
    is data[
      "composition_step"
    ].premises[
      0
    ]
    is data[
      "bracket_sum_step"
    ]
  )


def test_phase85_8_final_reaches_all_initial_repository_steps():
  data = build_phase85_8_data()

  assert all(
    any(
      ancestor is initial_step
      for ancestor
      in data[
        "ancestors"
      ]
    )
    for initial_step
    in data[
      "initial_steps"
    ]
  )


def test_phase85_8_repository_remains_unchanged():
  data = build_phase85_8_data()

  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == data[
    "initial_steps"
  ]


def test_phase85_8_generated_steps_are_not_registered():
  data = build_phase85_8_data()

  repository_steps = (
    repository_available_steps(
      data[
        "repository"
      ]
    )
  )

  assert all(
    generated_step
    not in repository_steps
    for generated_step in (
      data[
        "bracket_sum_step"
      ],
      data[
        "composition_step"
      ],
      data[
        "final_step"
      ],
    )
  )


