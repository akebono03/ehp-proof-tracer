from functools import lru_cache

from proof import ProofRule
from repository_inference import (
  derive_goal_from_repository_with_depth_two_producers,
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
def build_phase84_6_data():
  phase84_3 = build_phase84_3_data()
  phase77 = phase84_3[
    "phase77"
  ]
  phase77_5a = phase77[
    "data"
  ][
    "phase77_5a"
  ]

  result = (
    derive_goal_from_repository_with_depth_two_producers(
      phase84_3[
        "repository"
      ],
      phase84_3[
        "catalog"
      ],
      phase84_3[
        "goal"
      ],
    )
  )

  bracket_sum_step = next(
    step
    for step in result.inference_result.steps
    if isinstance(
      step.conclusion,
      Toda36Lemma516BracketSumContainmentStatement,
    )
  )

  composition_step = next(
    step
    for step in result.inference_result.steps
    if isinstance(
      step.conclusion,
      TodaLemma516ScaledCompositionBridgeStatement,
    )
  )

  final_step = result.goal_step

  assert final_step is not None

  return {
    "phase84_3": phase84_3,
    "phase77": phase77,
    "phase77_5a": phase77_5a,
    "repository": phase84_3[
      "repository"
    ],
    "initial_steps": phase84_3[
      "initial_steps"
    ],
    "goal": phase84_3[
      "goal"
    ],
    "result": result,
    "bracket_sum_step": (
      bracket_sum_step
    ),
    "composition_step": (
      composition_step
    ),
    "final_step": final_step,
    "ancestors": _collect_ancestors(
      final_step
    ),
  }


def test_phase84_6_actual_intermediates_are_not_initially_available():
  data = build_phase84_6_data()

  missing_conclusions = (
    data[
      "phase77"
    ][
      "bracket_sum_step"
    ].conclusion,
    data[
      "phase77"
    ][
      "composition_step"
    ].conclusion,
    data[
      "goal"
    ],
  )

  assert all(
    step.conclusion
    not in missing_conclusions
    for step in data[
      "initial_steps"
    ]
  )


def test_phase84_6_derives_new_actual_bracket_sum():
  data = build_phase84_6_data()

  step = data[
    "bracket_sum_step"
  ]

  assert (
    step.conclusion
    == data[
      "phase77"
    ][
      "bracket_sum_step"
    ].conclusion
  )

  assert (
    step
    is not data[
      "phase77"
    ][
      "bracket_sum_step"
    ]
  )


def test_phase84_6_bracket_sum_uses_actual_term_steps():
  data = build_phase84_6_data()

  assert (
    data[
      "bracket_sum_step"
    ].premises
    == (
      data[
        "phase77_5a"
      ][
        "first_term_step"
      ],
      data[
        "phase77_5a"
      ][
        "second_term_step"
      ],
    )
  )


def test_phase84_6_bracket_sum_preserves_rule_identity():
  data = build_phase84_6_data()

  assert (
    data[
      "bracket_sum_step"
    ].inference_rule
    is data[
      "phase84_3"
    ][
      "bracket_sum_rule"
    ]
  )


def test_phase84_6_derives_new_actual_composition_bridge():
  data = build_phase84_6_data()

  step = data[
    "composition_step"
  ]

  assert (
    step.conclusion
    == data[
      "phase77"
    ][
      "composition_step"
    ].conclusion
  )

  assert (
    step
    is not data[
      "phase77"
    ][
      "composition_step"
    ]
  )


def test_phase84_6_composition_uses_generated_bracket_sum():
  data = build_phase84_6_data()

  assert (
    data[
      "composition_step"
    ].premises
    == (
      data[
        "bracket_sum_step"
      ],
      data[
        "phase77"
      ][
        "suspension_bridge_step"
      ],
      data[
        "phase77"
      ][
        "sigma_definition_step"
      ],
    )
  )


def test_phase84_6_composition_preserves_rule_identity():
  data = build_phase84_6_data()

  assert (
    data[
      "composition_step"
    ].inference_rule
    is data[
      "phase84_3"
    ][
      "composition_rule"
    ]
  )


def test_phase84_6_derives_actual_toda_lemma516_goal():
  data = build_phase84_6_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaLemma516BracketSumContainmentStatement,
  )

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "goal"
    ]
  )

  assert (
    data[
      "final_step"
    ]
    is not data[
      "phase77"
    ][
      "final_step"
    ]
  )


def test_phase84_6_final_uses_both_generated_steps():
  data = build_phase84_6_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "bracket_sum_step"
      ],
      data[
        "composition_step"
      ],
    )
  )


def test_phase84_6_final_and_composition_share_bracket_sum_object():
  data = build_phase84_6_data()

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
  )

  assert (
    data[
      "final_step"
    ].premises[
      0
    ]
    is data[
      "bracket_sum_step"
    ]
  )


def test_phase84_6_final_preserves_rule_identity():
  data = build_phase84_6_data()

  assert (
    data[
      "final_step"
    ].inference_rule
    is data[
      "phase84_3"
    ][
      "final_rule"
    ]
  )


def test_phase84_6_shared_bracket_sum_is_generated_once():
  data = build_phase84_6_data()

  bracket_sum_steps = tuple(
    step
    for step in data[
      "result"
    ].inference_result.steps
    if isinstance(
      step.conclusion,
      Toda36Lemma516BracketSumContainmentStatement,
    )
  )

  assert bracket_sum_steps == (
    data[
      "bracket_sum_step"
    ],
  )


def test_phase84_6_all_new_steps_are_inferences():
  data = build_phase84_6_data()

  assert all(
    step.rule == ProofRule.INFERENCE
    for step in (
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


def test_phase84_6_final_reaches_all_initial_repository_steps():
  data = build_phase84_6_data()

  assert all(
    any(
      ancestor is initial_step
      for ancestor in data[
        "ancestors"
      ]
    )
    for initial_step in data[
      "initial_steps"
    ]
  )


def test_phase84_6_repository_remains_unchanged():
  data = build_phase84_6_data()

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


def test_phase84_6_generated_steps_are_not_registered():
  data = build_phase84_6_data()

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
