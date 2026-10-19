from functools import lru_cache

from proof import ProofRule
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  derive_goal_from_repository_with_one_level_producers,
  detect_goal_rule_missing_premises,
  find_missing_premise_producer_lookups,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from test_phase77_theorem36_bracket_sum import (
  build_phase77_5a_data,
)
from toda_rules import (
  Toda36Lemma516BracketSumContainmentStatement,
  Toda36Lemma516FirstBracketTermStatement,
  Toda36Lemma516SecondBracketTermStatement,
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
def build_phase83_5_data():
  phase77 = build_phase77_5a_data()
  phase77_4 = phase77[
    "phase77_4"
  ]

  bridge_step = phase77_4[
    "bridge_step"
  ]
  setup_step = phase77_4[
    "setup_step"
  ]
  original_first_step = phase77[
    "first_term_step"
  ]
  original_second_step = phase77[
    "second_term_step"
  ]
  original_goal_step = phase77[
    "bracket_sum_step"
  ]

  first_rule = (
    original_first_step.inference_rule
  )
  second_rule = (
    original_second_step.inference_rule
  )
  final_rule = (
    original_goal_step.inference_rule
  )

  assert first_rule is not None
  assert second_rule is not None
  assert final_rule is not None

  repository = ProofRepository()

  repository.register(
    ProofRepositoryEntry(
      key="phase83.actual.theorem36-bridge",
      step=bridge_step,
      phase="83",
      theorem=(
        "Toda Lemma 5.16 actual "
        "multiple-producer integration"
      ),
    )
  )

  repository.register(
    ProofRepositoryEntry(
      key="phase83.actual.typed-setup",
      step=setup_step,
      phase="83",
      theorem=(
        "Toda Lemma 5.16 actual "
        "multiple-producer integration"
      ),
    )
  )

  catalog = InferenceRuleCatalog()

  _register_rule(
    catalog,
    "phase83.actual.bracket-sum-final",
    final_rule,
    Toda36Lemma516BracketSumContainmentStatement,
  )

  _register_rule(
    catalog,
    "phase83.actual.first-term-producer",
    first_rule,
    Toda36Lemma516FirstBracketTermStatement,
  )

  _register_rule(
    catalog,
    "phase83.actual.second-term-producer",
    second_rule,
    Toda36Lemma516SecondBracketTermStatement,
  )

  goal = original_goal_step.conclusion

  initial_steps = (
    repository_available_steps(
      repository
    )
  )

  detections = (
    detect_goal_rule_missing_premises(
      repository,
      catalog,
      goal,
    )
  )

  lookups = (
    find_missing_premise_producer_lookups(
      detections[
        0
      ],
      catalog,
    )
  )

  result = (
    derive_goal_from_repository_with_one_level_producers(
      repository,
      catalog,
      goal,
    )
  )

  first_step = next(
    step
    for step in result.inference_result.steps
    if isinstance(
      step.conclusion,
      Toda36Lemma516FirstBracketTermStatement,
    )
  )

  second_step = next(
    step
    for step in result.inference_result.steps
    if isinstance(
      step.conclusion,
      Toda36Lemma516SecondBracketTermStatement,
    )
  )

  final_step = result.goal_step

  assert final_step is not None

  return {
    "phase77": phase77,
    "repository": repository,
    "catalog": catalog,
    "goal": goal,
    "bridge_step": bridge_step,
    "setup_step": setup_step,
    "original_first_step": original_first_step,
    "original_second_step": original_second_step,
    "original_goal_step": original_goal_step,
    "first_rule": first_rule,
    "second_rule": second_rule,
    "final_rule": final_rule,
    "initial_steps": initial_steps,
    "detections": detections,
    "lookups": lookups,
    "result": result,
    "first_step": first_step,
    "second_step": second_step,
    "final_step": final_step,
    "ancestors": _collect_ancestors(
      final_step
    ),
  }


def test_phase83_5_actual_goal_is_not_initially_available():
  data = build_phase83_5_data()

  assert all(
    step.conclusion
    != data[
      "goal"
    ]
    for step in data[
      "initial_steps"
    ]
  )


def test_phase83_5_both_direct_premises_are_initially_missing():
  data = build_phase83_5_data()

  assert len(
    data[
      "detections"
    ]
  ) == 1

  assert (
    data[
      "detections"
    ][
      0
    ].missing_indices
    == (
      0,
      1,
    )
  )


def test_phase83_5_each_missing_premise_has_one_actual_producer():
  data = build_phase83_5_data()

  assert tuple(
    lookup.producer_rules
    for lookup in data[
      "lookups"
    ]
  ) == (
    (
      data[
        "first_rule"
      ],
    ),
    (
      data[
        "second_rule"
      ],
    ),
  )


def test_phase83_5_derives_both_actual_sibling_branches():
  data = build_phase83_5_data()

  assert (
    data[
      "first_step"
    ].conclusion
    == data[
      "original_first_step"
    ].conclusion
  )

  assert (
    data[
      "second_step"
    ].conclusion
    == data[
      "original_second_step"
    ].conclusion
  )


def test_phase83_5_actual_producers_use_only_repository_steps():
  data = build_phase83_5_data()

  expected_premises = (
    data[
      "bridge_step"
    ],
    data[
      "setup_step"
    ],
  )

  assert (
    data[
      "first_step"
    ].premises
    == expected_premises
  )

  assert (
    data[
      "second_step"
    ].premises
    == expected_premises
  )


def test_phase83_5_actual_producer_rule_identity_is_preserved():
  data = build_phase83_5_data()

  assert (
    data[
      "first_step"
    ].inference_rule
    is data[
      "first_rule"
    ]
  )

  assert (
    data[
      "second_step"
    ].inference_rule
    is data[
      "second_rule"
    ]
  )


def test_phase83_5_derives_actual_bracket_sum_goal():
  data = build_phase83_5_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    Toda36Lemma516BracketSumContainmentStatement,
  )

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "goal"
    ]
  )


def test_phase83_5_final_step_uses_both_generated_branches():
  data = build_phase83_5_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "first_step"
      ],
      data[
        "second_step"
      ],
    )
  )


def test_phase83_5_final_rule_identity_is_preserved():
  data = build_phase83_5_data()

  assert (
    data[
      "final_step"
    ].inference_rule
    is data[
      "final_rule"
    ]
  )


def test_phase83_5_all_new_steps_are_inferences():
  data = build_phase83_5_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in (
      data[
        "first_step"
      ],
      data[
        "second_step"
      ],
      data[
        "final_step"
      ],
    )
  )


def test_phase83_5_final_is_not_its_own_ancestor():
  data = build_phase83_5_data()

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor in data[
      "ancestors"
    ]
  )


def test_phase83_5_final_conclusion_is_absent_from_ancestors():
  data = build_phase83_5_data()

  assert all(
    ancestor.conclusion
    != data[
      "final_step"
    ].conclusion
    for ancestor in data[
      "ancestors"
    ]
  )


def test_phase83_5_repository_remains_unchanged():
  data = build_phase83_5_data()

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


def test_phase83_5_generated_steps_are_not_registered():
  data = build_phase83_5_data()

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
        "first_step"
      ],
      data[
        "second_step"
      ],
      data[
        "final_step"
      ],
    )
  )
