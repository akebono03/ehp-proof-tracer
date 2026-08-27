import pytest

from expression import (
  eta,
  nu,
)
from hopf_rules import (
  HopfInvariantStatement,
  hopf_invariant_proof_step,
)
from proof import (
  LiteratureReference,
  ProofRule,
)


def test_hopf_invariant_statement():
  statement = HopfInvariantStatement(
    expression=eta(2),
    value=1,
  )

  assert statement.expression == eta(2)
  assert statement.value == 1


def test_hopf_invariant_statement_has_structural_equality():
  first = HopfInvariantStatement(
    expression=eta(2),
    value=1,
  )

  second = HopfInvariantStatement(
    expression=eta(2),
    value=1,
  )

  assert first == second


def test_hopf_invariant_statement_distinguishes_expression():
  first = HopfInvariantStatement(
    expression=eta(2),
    value=1,
  )

  different_expression = (
    HopfInvariantStatement(
      expression=nu(4),
      value=1,
    )
  )

  assert first != different_expression


def test_hopf_invariant_statement_distinguishes_value():
  first = HopfInvariantStatement(
    expression=eta(2),
    value=1,
  )

  different_value = (
    HopfInvariantStatement(
      expression=eta(2),
      value=0,
    )
  )

  assert first != different_value


def test_hopf_invariant_statement_preserves_provenance():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Hopf invariant fact",
  )

  statement = HopfInvariantStatement(
    expression=eta(2),
    value=1,
    source=reference,
    note="known Hopf invariant fact",
  )

  assert statement.source == reference
  assert (
    statement.note
    == "known Hopf invariant fact"
  )


def test_hopf_invariant_proof_step():
  statement = HopfInvariantStatement(
    expression=eta(2),
    value=1,
  )

  step = hopf_invariant_proof_step(
    statement
  )

  assert step.conclusion == statement
  assert step.premises == ()
  assert step.rule == ProofRule.GIVEN
  assert step.inference_rule is None


def test_hopf_invariant_proof_step_preserves_provenance():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Hopf invariant fact",
  )

  statement = HopfInvariantStatement(
    expression=eta(2),
    value=1,
    source=reference,
    note="known Hopf invariant fact",
  )

  step = hopf_invariant_proof_step(
    statement
  )

  assert step.conclusion == statement

  assert (
    step.conclusion.source
    == reference
  )

  assert (
    step.conclusion.note
    == "known Hopf invariant fact"
  )

  assert step.premises == ()
  assert step.rule == ProofRule.GIVEN
  assert step.inference_rule is None


def test_hopf_invariant_proof_step_rejects_non_hopf_statement():
  with pytest.raises(
    TypeError
  ):
    hopf_invariant_proof_step(
      eta(2)
    )





