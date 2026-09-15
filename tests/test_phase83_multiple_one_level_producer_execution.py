from copy import copy
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
  derive_goal_from_repository_with_one_level_producers,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase83ProducerSeedStatement:
  name: str


@dataclass(frozen=True)
class Phase83ProducerAStatement:
  value: str


@dataclass(frozen=True)
class Phase83ProducerBStatement:
  value: str


@dataclass(frozen=True)
class Phase83ProducerGoalStatement:
  value: str


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


def _seed_step(
  name,
):
  return ProofStep(
    conclusion=Phase83ProducerSeedStatement(
      name=name,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )


def _repository_with_steps(
  steps,
):
  repository = ProofRepository()

  for index, step in enumerate(
    steps
  ):
    repository.register(
      ProofRepositoryEntry(
        key=(
          "phase83.multiple.seed."
          f"{index}"
        ),
        step=step,
        phase="83",
        theorem=(
          "multiple one-level "
          "producer execution"
        ),
      )
    )

  return repository


def _producer_a_rule():
  return InferenceRule(
    name="phase83_producer_a",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          Phase83ProducerSeedStatement
        ),
        statement_pattern=(
          Phase83ProducerSeedStatement(
            name="seed-a",
          )
        ),
      ),
    ),
    conclusion_builder=(
      lambda premises: (
        Phase83ProducerAStatement(
          value="ready",
        )
      )
    ),
  )


def _producer_b_rule():
  return InferenceRule(
    name="phase83_producer_b",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          Phase83ProducerSeedStatement
        ),
        statement_pattern=(
          Phase83ProducerSeedStatement(
            name="seed-b",
          )
        ),
      ),
    ),
    conclusion_builder=(
      lambda premises: (
        Phase83ProducerBStatement(
          value="ready",
        )
      )
    ),
  )


def _depth_two_producer_b_rule():
  return InferenceRule(
    name="phase83_depth_two_producer_b",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Phase83ProducerAStatement
        ),
        statement_pattern=(
          Phase83ProducerAStatement(
            value="ready",
          )
        ),
      ),
    ),
    conclusion_builder=(
      lambda premises: (
        Phase83ProducerBStatement(
          value="ready",
        )
      )
    ),
  )


def _final_rule():
  return InferenceRule(
    name="phase83_multiple_final",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Phase83ProducerAStatement
        ),
        statement_pattern=(
          Phase83ProducerAStatement(
            value="ready",
          )
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Phase83ProducerBStatement
        ),
        statement_pattern=(
          Phase83ProducerBStatement(
            value="ready",
          )
        ),
      ),
    ),
    conclusion_builder=(
      lambda premises: (
        Phase83ProducerGoalStatement(
          value="complete",
        )
      )
    ),
  )


def _catalog(
  final_rule,
  producer_a_rule,
  producer_b_rule,
):
  catalog = InferenceRuleCatalog()

  _register_rule(
    catalog,
    "phase83.multiple.final",
    final_rule,
    Phase83ProducerGoalStatement,
  )

  _register_rule(
    catalog,
    "phase83.multiple.producer-a",
    producer_a_rule,
    Phase83ProducerAStatement,
  )

  _register_rule(
    catalog,
    "phase83.multiple.producer-b",
    producer_b_rule,
    Phase83ProducerBStatement,
  )

  return catalog


@lru_cache(maxsize=1)
def build_phase83_4_data():
  seed_a = _seed_step(
    "seed-a"
  )
  seed_b = _seed_step(
    "seed-b"
  )

  repository = _repository_with_steps(
    (
      seed_a,
      seed_b,
    )
  )

  final_rule = _final_rule()
  producer_a_rule = _producer_a_rule()
  producer_b_rule = _producer_b_rule()

  catalog = _catalog(
    final_rule,
    producer_a_rule,
    producer_b_rule,
  )

  initial_steps = (
    repository_available_steps(
      repository
    )
  )

  goal = Phase83ProducerGoalStatement(
    value="complete",
  )

  result = (
    derive_goal_from_repository_with_one_level_producers(
      repository,
      catalog,
      goal,
    )
  )

  producer_a_step = next(
    step
    for step in result.inference_result.steps
    if isinstance(
      step.conclusion,
      Phase83ProducerAStatement,
    )
  )

  producer_b_step = next(
    step
    for step in result.inference_result.steps
    if isinstance(
      step.conclusion,
      Phase83ProducerBStatement,
    )
  )

  return {
    "repository": repository,
    "catalog": catalog,
    "goal": goal,
    "seed_a": seed_a,
    "seed_b": seed_b,
    "initial_steps": initial_steps,
    "result": result,
    "producer_a_step": producer_a_step,
    "producer_b_step": producer_b_step,
  }


def test_phase83_4_goal_is_not_initially_available():
  data = build_phase83_4_data()

  assert all(
    step.conclusion
    != data[
      "goal"
    ]
    for step in data[
      "initial_steps"
    ]
  )


def test_phase83_4_both_intermediates_are_not_initially_available():
  data = build_phase83_4_data()

  assert all(
    not isinstance(
      step.conclusion,
      (
        Phase83ProducerAStatement,
        Phase83ProducerBStatement,
      ),
    )
    for step in data[
      "initial_steps"
    ]
  )


def test_phase83_4_executes_both_unique_producers():
  data = build_phase83_4_data()

  assert (
    data[
      "producer_a_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "producer_b_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase83_4_producers_use_only_repository_seeds():
  data = build_phase83_4_data()

  assert (
    data[
      "producer_a_step"
    ].premises
    == (
      data[
        "seed_a"
      ],
    )
  )

  assert (
    data[
      "producer_b_step"
    ].premises
    == (
      data[
        "seed_b"
      ],
    )
  )


def test_phase83_4_final_rule_retries_after_both_producers():
  data = build_phase83_4_data()

  assert (
    data[
      "result"
    ].goal_step
    is not None
  )

  assert (
    data[
      "result"
    ].goal_step.conclusion
    == data[
      "goal"
    ]
  )


def test_phase83_4_final_step_uses_both_generated_intermediates():
  data = build_phase83_4_data()

  assert (
    data[
      "result"
    ].goal_step.premises
    == (
      data[
        "producer_a_step"
      ],
      data[
        "producer_b_step"
      ],
    )
  )


def test_phase83_4_repository_remains_unchanged():
  data = build_phase83_4_data()

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


def test_phase83_4_partial_ambiguity_prevents_all_producer_execution():
  data = build_phase83_4_data()

  final_rule = _final_rule()
  producer_a_rule = _producer_a_rule()
  producer_b_rule = _producer_b_rule()

  catalog = _catalog(
    final_rule,
    producer_a_rule,
    producer_b_rule,
  )

  _register_rule(
    catalog,
    "phase83.multiple.producer-b-second",
    copy(
      producer_b_rule
    ),
    Phase83ProducerBStatement,
  )

  result = (
    derive_goal_from_repository_with_one_level_producers(
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

  assert all(
    not isinstance(
      step.conclusion,
      (
        Phase83ProducerAStatement,
        Phase83ProducerBStatement,
      ),
    )
    for step in result.inference_result.steps
  )


def test_phase83_4_does_not_follow_depth_two_producer_dependency():
  data = build_phase83_4_data()

  final_rule = _final_rule()

  catalog = _catalog(
    final_rule,
    _producer_a_rule(),
    _depth_two_producer_b_rule(),
  )

  result = (
    derive_goal_from_repository_with_one_level_producers(
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

  assert any(
    isinstance(
      step.conclusion,
      Phase83ProducerAStatement,
    )
    for step in result.inference_result.steps
  )

  assert all(
    not isinstance(
      step.conclusion,
      Phase83ProducerBStatement,
    )
    for step in result.inference_result.steps
  )
