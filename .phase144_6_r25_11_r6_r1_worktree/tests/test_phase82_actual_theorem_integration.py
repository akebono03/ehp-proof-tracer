from functools import lru_cache

from proof import (
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  derive_goal_from_repository_with_one_level_producers,
  repository_available_steps,
)
from test_phase82_two_step_forward_execution import (
  build_phase82_4_data,
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


def _proof_graph_is_acyclic(
  step,
):
  visiting = set()
  visited = set()

  def visit(
    current,
  ):
    current_id = id(
      current
    )

    if current_id in visiting:
      return False

    if current_id in visited:
      return True

    visiting.add(
      current_id
    )

    for premise in current.premises:
      if not visit(
        premise
      ):
        return False

    visiting.remove(
      current_id
    )

    visited.add(
      current_id
    )

    return True

  return visit(
    step
  )


def _collect_initial_ancestors(
  steps,
):
  ancestors = []
  seen = set()

  for step in steps:
    for ancestor in _collect_ancestors(
      step
    ):
      ancestor_id = id(
        ancestor
      )

      if ancestor_id in seen:
        continue

      seen.add(
        ancestor_id
      )

      ancestors.append(
        ancestor
      )

  return tuple(
    ancestors
  )


def _given_replacement(
  step,
):
  return ProofStep(
    conclusion=step.conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )


def _build_repository(
  bracket_sum_step,
  suspension_bridge_step,
  sigma_definition_step,
):
  repository = ProofRepository()

  repository.register(
    ProofRepositoryEntry(
      key=(
        "phase82.actual."
        "bracket_sum"
      ),
      step=bracket_sum_step,
      phase="82",
      theorem=(
        "Toda Lemma 5.16 "
        "actual two-step integration"
      ),
    )
  )

  repository.register(
    ProofRepositoryEntry(
      key=(
        "phase82.actual."
        "suspension_bridge"
      ),
      step=suspension_bridge_step,
      phase="82",
      theorem=(
        "Toda Lemma 5.16 "
        "actual two-step integration"
      ),
    )
  )

  repository.register(
    ProofRepositoryEntry(
      key=(
        "phase82.actual."
        "sigma_definition"
      ),
      step=sigma_definition_step,
      phase="82",
      theorem=(
        "Toda Lemma 5.16 "
        "actual two-step integration"
      ),
    )
  )

  return repository


@lru_cache(maxsize=1)
def build_phase82_5_data():
  phase82_4 = (
    build_phase82_4_data()
  )

  phase82_3 = phase82_4[
    "phase82_3"
  ]

  phase77 = phase82_4[
    "phase77"
  ]

  initial_steps = phase82_4[
    "initial_steps"
  ]

  intermediate_step = phase82_4[
    "intermediate_step"
  ]

  final_step = phase82_4[
    "result"
  ].goal_step

  assert intermediate_step is not None
  assert final_step is not None

  final_ancestors = (
    _collect_ancestors(
      final_step
    )
  )

  intermediate_ancestors = (
    _collect_ancestors(
      intermediate_step
    )
  )

  initial_ancestors = (
    _collect_initial_ancestors(
      initial_steps
    )
  )

  return {
    "phase82_4": phase82_4,
    "phase82_3": phase82_3,
    "phase77": phase77,
    "repository": phase82_4[
      "repository"
    ],
    "catalog": phase82_4[
      "catalog"
    ],
    "goal": phase82_4[
      "goal"
    ],
    "initial_steps": initial_steps,
    "initial_ancestors": (
      initial_ancestors
    ),
    "intermediate_step": (
      intermediate_step
    ),
    "intermediate_ancestors": (
      intermediate_ancestors
    ),
    "final_step": final_step,
    "final_ancestors": (
      final_ancestors
    ),
  }


def test_phase82_5_actual_goal_is_absent_from_initial_repository():
  data = build_phase82_5_data()

  assert all(
    step.conclusion
    != data[
      "goal"
    ]
    for step in data[
      "initial_steps"
    ]
  )


def test_phase82_5_intermediate_is_absent_from_initial_repository():
  data = build_phase82_5_data()

  intermediate_conclusion = (
    data[
      "phase77"
    ][
      "composition_step"
    ].conclusion
  )

  assert all(
    step.conclusion
    != intermediate_conclusion
    for step in data[
      "initial_steps"
    ]
  )


def test_phase82_5_goal_is_absent_from_initial_ancestry():
  data = build_phase82_5_data()

  assert all(
    ancestor.conclusion
    != data[
      "goal"
    ]
    for ancestor in data[
      "initial_ancestors"
    ]
  )


def test_phase82_5_intermediate_is_absent_from_initial_ancestry():
  data = build_phase82_5_data()

  intermediate_conclusion = (
    data[
      "intermediate_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != intermediate_conclusion
    for ancestor in data[
      "initial_ancestors"
    ]
  )


def test_phase82_5_new_intermediate_is_not_original_phase77_step():
  data = build_phase82_5_data()

  assert (
    data[
      "intermediate_step"
    ]
    is not data[
      "phase77"
    ][
      "composition_step"
    ]
  )


def test_phase82_5_new_final_is_not_original_phase77_step():
  data = build_phase82_5_data()

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


def test_phase82_5_intermediate_reuses_exact_existing_rule():
  data = build_phase82_5_data()

  assert (
    data[
      "intermediate_step"
    ].inference_rule
    is data[
      "phase82_3"
    ][
      "producer_rule"
    ]
  )


def test_phase82_5_final_reuses_exact_existing_rule():
  data = build_phase82_5_data()

  assert (
    data[
      "final_step"
    ].inference_rule
    is data[
      "phase82_3"
    ][
      "final_rule"
    ]
  )


def test_phase82_5_intermediate_is_inference_not_given():
  data = build_phase82_5_data()

  assert (
    data[
      "intermediate_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "intermediate_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase82_5_final_is_inference_not_given():
  data = build_phase82_5_data()

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase82_5_final_direct_premises_are_exact():
  data = build_phase82_5_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "phase77"
      ][
        "bracket_sum_step"
      ],
      data[
        "intermediate_step"
      ],
    )
  )


def test_phase82_5_intermediate_direct_premises_are_exact():
  data = build_phase82_5_data()

  assert (
    data[
      "intermediate_step"
    ].premises
    == data[
      "phase77"
    ][
      "composition_step"
    ].premises
  )

  for (
    derived_premise,
    original_premise,
  ) in zip(
    data[
      "intermediate_step"
    ].premises,
    data[
      "phase77"
    ][
      "composition_step"
    ].premises,
  ):
    assert (
      derived_premise
      is original_premise
    )


def test_phase82_5_final_reaches_new_intermediate():
  data = build_phase82_5_data()

  assert any(
    ancestor
    is data[
      "intermediate_step"
    ]
    for ancestor in data[
      "final_ancestors"
    ]
  )


def test_phase82_5_final_reaches_all_actual_repository_seeds():
  data = build_phase82_5_data()

  for initial_step in data[
    "initial_steps"
  ]:
    assert any(
      ancestor
      is initial_step
      for ancestor in data[
        "final_ancestors"
      ]
    )


def test_phase82_5_intermediate_does_not_depend_on_new_final():
  data = build_phase82_5_data()

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor in data[
      "intermediate_ancestors"
    ]
  )


def test_phase82_5_final_is_not_its_own_ancestor():
  data = build_phase82_5_data()

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor in data[
      "final_ancestors"
    ]
  )


def test_phase82_5_final_conclusion_is_absent_from_ancestors():
  data = build_phase82_5_data()

  final_conclusion = (
    data[
      "final_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != final_conclusion
    for ancestor in data[
      "final_ancestors"
    ]
  )


def test_phase82_5_intermediate_conclusion_is_absent_from_its_ancestors():
  data = build_phase82_5_data()

  intermediate_conclusion = (
    data[
      "intermediate_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != intermediate_conclusion
    for ancestor in data[
      "intermediate_ancestors"
    ]
  )


def test_phase82_5_actual_two_step_graph_is_acyclic():
  data = build_phase82_5_data()

  assert (
    _proof_graph_is_acyclic(
      data[
        "final_step"
      ]
    )
  )


def test_phase82_5_repository_remains_unchanged():
  data = build_phase82_5_data()

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


def test_phase82_5_new_intermediate_is_not_registered():
  data = build_phase82_5_data()

  assert all(
    step
    is not data[
      "intermediate_step"
    ]
    for step in repository_available_steps(
      data[
        "repository"
      ]
    )
  )


def test_phase82_5_new_final_is_not_registered():
  data = build_phase82_5_data()

  assert all(
    step
    is not data[
      "final_step"
    ]
    for step in repository_available_steps(
      data[
        "repository"
      ]
    )
  )


def test_phase82_5_given_bracket_sum_shortcut_is_rejected():
  data = build_phase82_5_data()

  phase77 = data[
    "phase77"
  ]

  repository = _build_repository(
    _given_replacement(
      phase77[
        "bracket_sum_step"
      ]
    ),
    phase77[
      "suspension_bridge_step"
    ],
    phase77[
      "sigma_definition_step"
    ],
  )

  result = (
    derive_goal_from_repository_with_one_level_producers(
      repository,
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
    )
  )

  assert (
    result.goal_step
    is None
  )

  assert all(
    step.conclusion
    != phase77[
      "composition_step"
    ].conclusion
    for step in result.inference_result.steps
  )


def test_phase82_5_given_suspension_bridge_shortcut_is_rejected():
  data = build_phase82_5_data()

  phase77 = data[
    "phase77"
  ]

  repository = _build_repository(
    phase77[
      "bracket_sum_step"
    ],
    _given_replacement(
      phase77[
        "suspension_bridge_step"
      ]
    ),
    phase77[
      "sigma_definition_step"
    ],
  )

  result = (
    derive_goal_from_repository_with_one_level_producers(
      repository,
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
    )
  )

  assert (
    result.goal_step
    is None
  )

  assert all(
    step.conclusion
    != phase77[
      "composition_step"
    ].conclusion
    for step in result.inference_result.steps
  )


def test_phase82_5_given_sigma_definition_shortcut_is_rejected():
  data = build_phase82_5_data()

  phase77 = data[
    "phase77"
  ]

  repository = _build_repository(
    phase77[
      "bracket_sum_step"
    ],
    phase77[
      "suspension_bridge_step"
    ],
    _given_replacement(
      phase77[
        "sigma_definition_step"
      ]
    ),
  )

  result = (
    derive_goal_from_repository_with_one_level_producers(
      repository,
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
    )
  )

  assert (
    result.goal_step
    is None
  )

  assert all(
    step.conclusion
    != phase77[
      "composition_step"
    ].conclusion
    for step in result.inference_result.steps
  )


