import pytest

from expression import (
  eta,
  nu,
)
from hopf_rules import (
  HopfInvariantOneStatement,
  HopfInvariantStatement,
  hopf_invariant_one_inference_rule,
  hopf_invariant_proof_step,
)
from proof import (
  LiteratureReference,
  ProofRule,
  ProofStep,
  apply_inference_match,
  find_inference_match,
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


def test_hopf_invariant_one_rule():
  statement = HopfInvariantStatement(
    expression=eta(2),
    value=1,
  )

  hopf_step = hopf_invariant_proof_step(
    statement
  )

  rule = (
    hopf_invariant_one_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      hopf_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    HopfInvariantOneStatement(
      expression=eta(2),
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    hopf_step,
  )


def test_hopf_invariant_one_rule_rejects_zero():
  statement = HopfInvariantStatement(
    expression=eta(2),
    value=0,
  )

  hopf_step = hopf_invariant_proof_step(
    statement
  )

  rule = (
    hopf_invariant_one_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      hopf_step,
    ),
  )

  assert match is None


def test_hopf_invariant_one_rule_rejects_other_value():
  statement = HopfInvariantStatement(
    expression=eta(2),
    value=2,
  )

  hopf_step = hopf_invariant_proof_step(
    statement
  )

  rule = (
    hopf_invariant_one_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      hopf_step,
    ),
  )

  assert match is None


def test_hopf_invariant_one_rule_preserves_provenance():
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

  hopf_step = hopf_invariant_proof_step(
    statement
  )

  rule = (
    hopf_invariant_one_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      hopf_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    HopfInvariantOneStatement(
      expression=eta(2),
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    hopf_step,
  )

  assert (
    derived_step
    .premises[0]
    .conclusion
    .source
    == reference
  )

  assert (
    derived_step
    .premises[0]
    .conclusion
    .note
    == "known Hopf invariant fact"
  )






