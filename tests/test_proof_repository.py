from dataclasses import dataclass

import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)


@dataclass(frozen=True)
class BaseStatement:
  value: str


@dataclass(frozen=True)
class ChildStatement(
  BaseStatement,
):
  pass


def make_step(
  conclusion,
  premises=(),
  rule=ProofRule.GIVEN,
):
  return ProofStep(
    conclusion=conclusion,
    premises=premises,
    rule=rule,
  )


def test_repository_entry_accepts_minimum_valid_data():
  step = make_step(
    BaseStatement(
      value="A",
    )
  )

  entry = ProofRepositoryEntry(
    key="phase79.a",
    step=step,
  )

  assert entry.key == "phase79.a"
  assert entry.step is step
  assert entry.phase is None
  assert entry.theorem is None


def test_repository_entry_rejects_empty_key():
  step = make_step(
    BaseStatement(
      value="A",
    )
  )

  with pytest.raises(
    ValueError,
    match="key must not be empty",
  ):
    ProofRepositoryEntry(
      key="",
      step=step,
    )


def test_repository_entry_rejects_non_string_key():
  step = make_step(
    BaseStatement(
      value="A",
    )
  )

  with pytest.raises(
    TypeError,
    match="key must be a str",
  ):
    ProofRepositoryEntry(
      key=79,
      step=step,
    )


def test_repository_entry_rejects_non_proof_step():
  with pytest.raises(
    TypeError,
    match="step must be a ProofStep",
  ):
    ProofRepositoryEntry(
      key="phase79.a",
      step=BaseStatement(
        value="A",
      ),
    )


def test_repository_entry_rejects_non_string_phase():
  step = make_step(
    BaseStatement(
      value="A",
    )
  )

  with pytest.raises(
    TypeError,
    match="phase must be a str or None",
  ):
    ProofRepositoryEntry(
      key="phase79.a",
      step=step,
      phase=79,
    )


def test_repository_entry_rejects_non_string_theorem():
  step = make_step(
    BaseStatement(
      value="A",
    )
  )

  with pytest.raises(
    TypeError,
    match="theorem must be a str or None",
  ):
    ProofRepositoryEntry(
      key="phase79.a",
      step=step,
      theorem=79,
    )


def test_repository_register_and_get_preserve_entry_and_step_identity():
  repository = ProofRepository()
  step = make_step(
    BaseStatement(
      value="A",
    )
  )
  entry = ProofRepositoryEntry(
    key="phase79.a",
    step=step,
    phase="79",
    theorem="Repository test theorem",
  )

  repository.register(
    entry
  )

  found = repository.get(
    "phase79.a"
  )

  assert found is entry
  assert found.step is step


def test_repository_get_raises_key_error_for_missing_key():
  repository = ProofRepository()

  with pytest.raises(
    KeyError,
  ):
    repository.get(
      "missing"
    )


def test_repository_register_rejects_non_entry():
  repository = ProofRepository()

  with pytest.raises(
    TypeError,
    match="entry must be a ProofRepositoryEntry",
  ):
    repository.register(
      "not-an-entry"
    )


def test_repository_register_rejects_duplicate_key():
  repository = ProofRepository()
  first_step = make_step(
    BaseStatement(
      value="A",
    )
  )
  second_step = make_step(
    BaseStatement(
      value="B",
    )
  )

  repository.register(
    ProofRepositoryEntry(
      key="phase79.same",
      step=first_step,
    )
  )

  with pytest.raises(
    ValueError,
    match="duplicate repository key",
  ):
    repository.register(
      ProofRepositoryEntry(
        key="phase79.same",
        step=second_step,
      )
    )


def test_repository_allows_same_conclusion_with_different_keys():
  repository = ProofRepository()
  conclusion = BaseStatement(
    value="A",
  )
  first_entry = ProofRepositoryEntry(
    key="phase79.first",
    step=make_step(
      conclusion
    ),
  )
  second_entry = ProofRepositoryEntry(
    key="phase79.second",
    step=make_step(
      conclusion
    ),
  )

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  assert (
    repository.find_by_conclusion(
      conclusion
    )
    == (
      first_entry,
      second_entry,
    )
  )


def test_repository_allows_same_step_with_different_keys():
  repository = ProofRepository()
  step = make_step(
    BaseStatement(
      value="A",
    )
  )
  first_entry = ProofRepositoryEntry(
    key="phase79.first",
    step=step,
  )
  second_entry = ProofRepositoryEntry(
    key="phase79.second",
    step=step,
  )

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  assert (
    repository.get(
      "phase79.first"
    ).step
    is step
  )
  assert (
    repository.get(
      "phase79.second"
    ).step
    is step
  )


def test_find_by_conclusion_returns_empty_tuple_when_not_found():
  repository = ProofRepository()

  assert (
    repository.find_by_conclusion(
      BaseStatement(
        value="missing",
      )
    )
    == ()
  )


def test_find_by_statement_type_uses_isinstance_and_registration_order():
  repository = ProofRepository()
  child_entry = ProofRepositoryEntry(
    key="phase79.child",
    step=make_step(
      ChildStatement(
        value="child",
      )
    ),
  )
  base_entry = ProofRepositoryEntry(
    key="phase79.base",
    step=make_step(
      BaseStatement(
        value="base",
      )
    ),
  )

  repository.register(
    child_entry
  )
  repository.register(
    base_entry
  )

  assert (
    repository.find_by_statement_type(
      BaseStatement
    )
    == (
      child_entry,
      base_entry,
    )
  )


def test_find_by_statement_type_rejects_non_type():
  repository = ProofRepository()

  with pytest.raises(
    TypeError,
    match="statement_type must be a type",
  ):
    repository.find_by_statement_type(
      "BaseStatement"
    )


def test_find_by_phase_uses_exact_match_and_registration_order():
  repository = ProofRepository()
  first_entry = ProofRepositoryEntry(
    key="phase78.first",
    step=make_step(
      BaseStatement(
        value="A",
      )
    ),
    phase="78",
  )
  other_entry = ProofRepositoryEntry(
    key="phase78_11.other",
    step=make_step(
      BaseStatement(
        value="B",
      )
    ),
    phase="78-11",
  )
  second_entry = ProofRepositoryEntry(
    key="phase78.second",
    step=make_step(
      BaseStatement(
        value="C",
      )
    ),
    phase="78",
  )

  repository.register(
    first_entry
  )
  repository.register(
    other_entry
  )
  repository.register(
    second_entry
  )

  assert (
    repository.find_by_phase(
      "78"
    )
    == (
      first_entry,
      second_entry,
    )
  )


def test_find_by_theorem_uses_exact_match_and_registration_order():
  repository = ProofRepository()
  theorem = "Toda Equation (5.16)"
  first_entry = ProofRepositoryEntry(
    key="phase76.first",
    step=make_step(
      BaseStatement(
        value="A",
      )
    ),
    theorem=theorem,
  )
  other_entry = ProofRepositoryEntry(
    key="phase76.other",
    step=make_step(
      BaseStatement(
        value="B",
      )
    ),
    theorem="Toda (5.16)",
  )
  second_entry = ProofRepositoryEntry(
    key="phase76.second",
    step=make_step(
      BaseStatement(
        value="C",
      )
    ),
    theorem=theorem,
  )

  repository.register(
    first_entry
  )
  repository.register(
    other_entry
  )
  repository.register(
    second_entry
  )

  assert (
    repository.find_by_theorem(
      theorem
    )
    == (
      first_entry,
      second_entry,
    )
  )


def test_dependencies_return_exact_direct_premises():
  repository = ProofRepository()
  first_step = make_step(
    BaseStatement(
      value="A",
    )
  )
  second_step = make_step(
    BaseStatement(
      value="B",
    )
  )
  final_step = make_step(
    BaseStatement(
      value="C",
    ),
    premises=(
      first_step,
      second_step,
    ),
    rule=ProofRule.INFERENCE,
  )
  final_entry = ProofRepositoryEntry(
    key="phase79.final",
    step=final_step,
  )

  repository.register(
    final_entry
  )

  dependencies = repository.dependencies(
    final_entry
  )

  assert dependencies == (
    first_step,
    second_step,
  )
  assert dependencies[0] is first_step
  assert dependencies[1] is second_step


def test_dependencies_of_root_step_are_empty():
  repository = ProofRepository()
  root_step = make_step(
    BaseStatement(
      value="A",
    )
  )
  root_entry = ProofRepositoryEntry(
    key="phase79.root",
    step=root_step,
  )

  repository.register(
    root_entry
  )

  assert (
    repository.dependencies(
      root_entry
    )
    == ()
  )


def test_dependencies_reject_non_entry():
  repository = ProofRepository()

  with pytest.raises(
    TypeError,
    match="entry must be a ProofRepositoryEntry",
  ):
    repository.dependencies(
      "not-an-entry"
    )


def test_phase78_actual_steps_register_and_retrieve_without_graph_changes():
  from test_phase78_stable_g0_to_g7_integration import (
    build_phase78_11_data,
  )

  data = build_phase78_11_data()
  repository = ProofRepository()

  g7_step = data[
    "g7_step"
  ]
  aggregate_step = data[
    "aggregate_step"
  ]

  g7_entry = ProofRepositoryEntry(
    key="phase78.g7",
    step=g7_step,
    phase="78",
    theorem=(
      "Toda stable G_0 through G_7 integration"
    ),
  )
  aggregate_entry = ProofRepositoryEntry(
    key="phase78.stable_g0_to_g7",
    step=aggregate_step,
    phase="78",
    theorem=(
      "Toda stable G_0 through G_7 integration"
    ),
  )

  repository.register(
    g7_entry
  )
  repository.register(
    aggregate_entry
  )

  assert (
    repository.get(
      "phase78.g7"
    ).step
    is g7_step
  )

  assert (
    repository.get(
      "phase78.stable_g0_to_g7"
    ).step
    is aggregate_step
  )

  assert (
    repository.find_by_conclusion(
      g7_step.conclusion
    )
    == (
      g7_entry,
    )
  )

  assert (
    repository.find_by_phase(
      "78"
    )
    == (
      g7_entry,
      aggregate_entry,
    )
  )

  dependencies = repository.dependencies(
    aggregate_entry
  )

  assert (
    dependencies
    == data[
      "premise_steps"
    ]
  )

  assert all(
    actual is expected
    for actual, expected in zip(
      dependencies,
      data[
        "premise_steps"
      ],
    )
  )


