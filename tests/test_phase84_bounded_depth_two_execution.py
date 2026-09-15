from dataclasses import dataclass
from functools import lru_cache

from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  derive_goal_from_repository_with_depth_two_producers,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase84ExecutionSeedAStatement:
  name: str


@dataclass(frozen=True)
class Phase84ExecutionSeedBStatement:
  name: str


@dataclass(frozen=True)
class Phase84ExecutionSharedStatement:
  name: str


@dataclass(frozen=True)
class Phase84ExecutionIntermediateStatement:
  name: str


@dataclass(frozen=True)
class Phase84ExecutionGoalStatement:
  name: str


def _shared_producer_rule():
  def build_conclusion(
    premises,
  ):
    return Phase84ExecutionSharedStatement(
      name=premises[
        0
      ].conclusion.name,
    )

  return InferenceRule(
    name="phase84 shared producer",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          Phase84ExecutionSeedAStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
  )


def _intermediate_producer_rule():
  def build_conclusion(
    premises,
  ):
    return (
      Phase84ExecutionIntermediateStatement(
        name=(
          premises[
            0
          ].conclusion.name
          + premises[
            1
          ].conclusion.name
        ),
      )
    )

  return InferenceRule(
    name="phase84 intermediate producer",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Phase84ExecutionSharedStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          Phase84ExecutionSeedBStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
  )


def _final_rule():
  def build_conclusion(
    premises,
  ):
    return Phase84ExecutionGoalStatement(
      name=premises[
        1
      ].conclusion.name,
    )

  return InferenceRule(
    name="phase84 final rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Phase84ExecutionSharedStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Phase84ExecutionIntermediateStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
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
def build_phase84_5_data():
  seed_a_step = ProofStep(
    conclusion=(
      Phase84ExecutionSeedAStatement(
        name="A",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  seed_b_step = ProofStep(
    conclusion=(
      Phase84ExecutionSeedBStatement(
        name="B",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  repository = ProofRepository()

  for key, step in (
    (
      "phase84.execution.seed-a",
      seed_a_step,
    ),
    (
      "phase84.execution.seed-b",
      seed_b_step,
    ),
  ):
    repository.register(
      ProofRepositoryEntry(
        key=key,
        step=step,
        phase="84",
        theorem=(
          "bounded depth-two execution"
        ),
      )
    )

  shared_rule = _shared_producer_rule()
  intermediate_rule = (
    _intermediate_producer_rule()
  )
  final_rule = _final_rule()

  catalog = InferenceRuleCatalog()

  _register_rule(
    catalog,
    "phase84.execution.final",
    final_rule,
    Phase84ExecutionGoalStatement,
  )

  _register_rule(
    catalog,
    "phase84.execution.shared",
    shared_rule,
    Phase84ExecutionSharedStatement,
  )

  _register_rule(
    catalog,
    "phase84.execution.intermediate",
    intermediate_rule,
    Phase84ExecutionIntermediateStatement,
  )

  goal = Phase84ExecutionGoalStatement(
    name="AB",
  )

  initial_steps = repository_available_steps(
    repository
  )

  result = (
    derive_goal_from_repository_with_depth_two_producers(
      repository,
      catalog,
      goal,
    )
  )

  shared_step = next(
    step
    for step in result.inference_result.steps
    if isinstance(
      step.conclusion,
      Phase84ExecutionSharedStatement,
    )
  )

  intermediate_step = next(
    step
    for step in result.inference_result.steps
    if isinstance(
      step.conclusion,
      Phase84ExecutionIntermediateStatement,
    )
  )

  final_step = result.goal_step

  assert final_step is not None

  return {
    "repository": repository,
    "catalog": catalog,
    "goal": goal,
    "initial_steps": initial_steps,
    "seed_a_step": seed_a_step,
    "seed_b_step": seed_b_step,
    "shared_rule": shared_rule,
    "intermediate_rule": intermediate_rule,
    "final_rule": final_rule,
    "result": result,
    "shared_step": shared_step,
    "intermediate_step": intermediate_step,
    "final_step": final_step,
  }


def test_phase84_5_goal_is_not_initially_available():
  data = build_phase84_5_data()

  assert all(
    step.conclusion
    != data[
      "goal"
    ]
    for step in data[
      "initial_steps"
    ]
  )


def test_phase84_5_executes_shared_producer_first():
  data = build_phase84_5_data()

  step = data[
    "shared_step"
  ]

  assert step.premises == (
    data[
      "seed_a_step"
    ],
  )

  assert (
    step.inference_rule
    is data[
      "shared_rule"
    ]
  )


def test_phase84_5_intermediate_uses_generated_shared_step():
  data = build_phase84_5_data()

  step = data[
    "intermediate_step"
  ]

  assert step.premises == (
    data[
      "shared_step"
    ],
    data[
      "seed_b_step"
    ],
  )

  assert (
    step.inference_rule
    is data[
      "intermediate_rule"
    ]
  )


def test_phase84_5_derives_requested_goal():
  data = build_phase84_5_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "goal"
    ]
  )


def test_phase84_5_final_uses_both_generated_premises():
  data = build_phase84_5_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "shared_step"
      ],
      data[
        "intermediate_step"
      ],
    )
  )


def test_phase84_5_final_preserves_rule_identity():
  data = build_phase84_5_data()

  assert (
    data[
      "final_step"
    ].inference_rule
    is data[
      "final_rule"
    ]
  )


def test_phase84_5_shared_producer_executes_once():
  data = build_phase84_5_data()

  shared_steps = tuple(
    step
    for step in data[
      "result"
    ].inference_result.steps
    if isinstance(
      step.conclusion,
      Phase84ExecutionSharedStatement,
    )
  )

  assert shared_steps == (
    data[
      "shared_step"
    ],
  )


def test_phase84_5_all_new_steps_are_inferences():
  data = build_phase84_5_data()

  assert all(
    step.rule == ProofRule.INFERENCE
    for step in (
      data[
        "shared_step"
      ],
      data[
        "intermediate_step"
      ],
      data[
        "final_step"
      ],
    )
  )


def test_phase84_5_repository_remains_unchanged():
  data = build_phase84_5_data()

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


def test_phase84_5_generated_steps_are_not_registered():
  data = build_phase84_5_data()

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
        "shared_step"
      ],
      data[
        "intermediate_step"
      ],
      data[
        "final_step"
      ],
    )
  )
