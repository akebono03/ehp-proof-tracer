from dataclasses import dataclass

import pytest

from proof import (
  InferenceRule,
  InferenceTerminationReason,
  PremisePattern,
  ProofRule,
  ProofStep,
  run_inference_until_stable_with_history,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  repository_available_steps,
)


@dataclass(frozen=True)
class Phase80BridgeStatement:
  value: str


@dataclass(frozen=True)
class Phase80DerivedStatement:
  value: str


def make_step(
  value,
):
  return ProofStep(
    conclusion=Phase80BridgeStatement(
      value=value,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )


def test_phase80_2_empty_repository_returns_empty_available_steps():
  repository = ProofRepository()

  assert (
    repository_available_steps(
      repository
    )
    == ()
  )


def test_phase80_2_repository_entries_preserve_registration_order():
  repository = ProofRepository()

  first_entry = ProofRepositoryEntry(
    key="phase80.first",
    step=make_step(
      "A"
    ),
  )

  second_entry = ProofRepositoryEntry(
    key="phase80.second",
    step=make_step(
      "B"
    ),
  )

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  assert repository.entries() == (
    first_entry,
    second_entry,
  )


def test_phase80_2_available_steps_preserve_registration_order_and_identity():
  repository = ProofRepository()

  first_step = make_step(
    "A"
  )
  second_step = make_step(
    "B"
  )

  repository.register(
    ProofRepositoryEntry(
      key="phase80.first",
      step=first_step,
    )
  )
  repository.register(
    ProofRepositoryEntry(
      key="phase80.second",
      step=second_step,
    )
  )

  available_steps = (
    repository_available_steps(
      repository
    )
  )

  assert available_steps == (
    first_step,
    second_step,
  )
  assert available_steps[0] is first_step
  assert available_steps[1] is second_step


def test_phase80_2_same_step_alias_is_deduplicated_by_identity():
  repository = ProofRepository()

  shared_step = make_step(
    "A"
  )

  repository.register(
    ProofRepositoryEntry(
      key="phase80.original",
      step=shared_step,
      phase="80",
    )
  )
  repository.register(
    ProofRepositoryEntry(
      key="phase80.alias",
      step=shared_step,
      phase="999",
    )
  )

  available_steps = (
    repository_available_steps(
      repository
    )
  )

  assert available_steps == (
    shared_step,
  )
  assert available_steps[0] is shared_step


def test_phase80_2_same_conclusion_distinct_proofs_are_preserved():
  repository = ProofRepository()

  shared_conclusion = (
    Phase80BridgeStatement(
      value="A",
    )
  )

  first_step = ProofStep(
    conclusion=shared_conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )
  second_step = ProofStep(
    conclusion=shared_conclusion,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  repository.register(
    ProofRepositoryEntry(
      key="phase80.first",
      step=first_step,
    )
  )
  repository.register(
    ProofRepositoryEntry(
      key="phase80.second",
      step=second_step,
    )
  )

  available_steps = (
    repository_available_steps(
      repository
    )
  )

  assert available_steps == (
    first_step,
    second_step,
  )
  assert available_steps[0] is first_step
  assert available_steps[1] is second_step


def test_phase80_2_available_steps_feed_existing_inference_runner_unchanged():
  repository = ProofRepository()

  source_step = make_step(
    "source"
  )

  repository.register(
    ProofRepositoryEntry(
      key="phase80.source",
      step=source_step,
    )
  )

  rule = InferenceRule(
    name="phase80_bridge_test",
    premise_patterns=(
      PremisePattern(
        statement_type=(
          Phase80BridgeStatement
        ),
      ),
    ),
    conclusion_builder=(
      lambda premises: (
        Phase80DerivedStatement(
          value=(
            premises[0]
            .conclusion
            .value
          ),
        )
      )
    ),
  )

  available_steps = (
    repository_available_steps(
      repository
    )
  )

  result = (
    run_inference_until_stable_with_history(
      (rule,),
      available_steps,
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )
  assert result.steps[0] is source_step
  assert any(
    step.conclusion
    == Phase80DerivedStatement(
      value="source",
    )
    for step in result.steps
  )


def test_phase80_2_repository_available_steps_rejects_non_repository():
  with pytest.raises(
    TypeError,
    match=(
      "repository must be "
      "a ProofRepository"
    ),
  ):
    repository_available_steps(
      "not-a-repository"
    )
