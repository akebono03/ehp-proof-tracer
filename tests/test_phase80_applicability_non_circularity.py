from proof import (
  ProofRule,
  ProofStep,
  find_inference_match,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  derive_goal_from_repository,
  repository_available_steps,
)
from test_phase80_actual_proof_integration import (
  build_phase80_5_data,
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
  visited = set()
  active = set()

  def visit(
    current,
  ):
    current_id = id(
      current
    )

    if current_id in active:
      return False

    if current_id in visited:
      return True

    active.add(
      current_id
    )

    for premise in current.premises:
      if not visit(
        premise
      ):
        return False

    active.remove(
      current_id
    )
    visited.add(
      current_id
    )

    return True

  return visit(
    step
  )


def test_phase80_6_goal_is_absent_from_initial_repository_steps_and_ancestors():
  data = build_phase80_5_data()

  initial_steps = (
    repository_available_steps(
      data[
        "repository"
      ]
    )
  )

  assert all(
    step.conclusion
    != data[
      "goal"
    ]
    for step in initial_steps
  )

  for step in initial_steps:
    assert all(
      ancestor.conclusion
      != data[
        "goal"
      ]
      for ancestor in (
        _collect_ancestors(
          step
        )
      )
    )


def test_phase80_6_derived_goal_is_inference_and_not_given():
  data = build_phase80_5_data()

  result = (
    derive_goal_from_repository(
      data[
        "repository"
      ],
      (
        data[
          "final_rule"
        ],
      ),
      data[
        "goal"
      ],
    )
  )

  assert result.goal_step is not None
  assert (
    result.goal_step.rule
    == ProofRule.INFERENCE
  )
  assert (
    result.goal_step.rule
    != ProofRule.GIVEN
  )


def test_phase80_6_missing_bracket_sum_premise_rejects_final_rule():
  data = build_phase80_5_data()

  match = find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "composition_step"
      ],
    ),
  )

  assert match is None


def test_phase80_6_missing_composition_premise_rejects_final_rule():
  data = build_phase80_5_data()

  match = find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "bracket_sum_step"
      ],
    ),
  )

  assert match is None


def test_phase80_6_given_bracket_sum_shortcut_rejects_final_rule():
  data = build_phase80_5_data()

  given_bracket_sum_step = ProofStep(
    conclusion=(
      data[
        "bracket_sum_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    data[
      "final_rule"
    ],
    (
      given_bracket_sum_step,
      data[
        "composition_step"
      ],
    ),
  )

  assert match is None


def test_phase80_6_given_composition_shortcut_rejects_final_rule():
  data = build_phase80_5_data()

  given_composition_step = ProofStep(
    conclusion=(
      data[
        "composition_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "bracket_sum_step"
      ],
      given_composition_step,
    ),
  )

  assert match is None


def test_phase80_6_repository_metadata_does_not_change_actual_applicability():
  data = build_phase80_5_data()

  repository = ProofRepository()

  repository.register(
    ProofRepositoryEntry(
      key="alias.phase80.bracket",
      step=(
        data[
          "bracket_sum_step"
        ]
      ),
      phase="999",
      theorem=(
        "Unrelated bracket metadata"
      ),
    )
  )

  repository.register(
    ProofRepositoryEntry(
      key="alias.phase80.composition",
      step=(
        data[
          "composition_step"
        ]
      ),
      phase="1000",
      theorem=(
        "Unrelated composition metadata"
      ),
    )
  )

  result = (
    derive_goal_from_repository(
      repository,
      (
        data[
          "final_rule"
        ],
      ),
      data[
        "goal"
      ],
    )
  )

  assert result.goal_step is not None
  assert (
    result.goal_step.conclusion
    == data[
      "goal"
    ]
  )
  assert result.goal_step.premises == (
    data[
      "bracket_sum_step"
    ],
    data[
      "composition_step"
    ],
  )


def test_phase80_6_derived_goal_is_not_its_own_ancestor():
  data = build_phase80_5_data()

  result = (
    derive_goal_from_repository(
      data[
        "repository"
      ],
      (
        data[
          "final_rule"
        ],
      ),
      data[
        "goal"
      ],
    )
  )

  goal_step = result.goal_step

  assert goal_step is not None

  ancestors = _collect_ancestors(
    goal_step
  )

  assert all(
    ancestor is not goal_step
    for ancestor in ancestors
  )


def test_phase80_6_derived_goal_conclusion_is_absent_from_ancestors():
  data = build_phase80_5_data()

  result = (
    derive_goal_from_repository(
      data[
        "repository"
      ],
      (
        data[
          "final_rule"
        ],
      ),
      data[
        "goal"
      ],
    )
  )

  goal_step = result.goal_step

  assert goal_step is not None

  ancestors = _collect_ancestors(
    goal_step
  )

  assert all(
    ancestor.conclusion
    != goal_step.conclusion
    for ancestor in ancestors
  )


def test_phase80_6_repository_assisted_derived_graph_is_acyclic():
  data = build_phase80_5_data()

  result = (
    derive_goal_from_repository(
      data[
        "repository"
      ],
      (
        data[
          "final_rule"
        ],
      ),
      data[
        "goal"
      ],
    )
  )

  assert result.goal_step is not None
  assert _proof_graph_is_acyclic(
    result.goal_step
  )
