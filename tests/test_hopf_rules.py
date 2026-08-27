import pytest

from expression import (
  Multiple,
  Zero,
  eta,
  nu,
)
from hopf_rules import (
  HopfCompositionLawStatement,
  HopfInvariantStatement,
  hopf_composition_law_inference_rule,
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
    expression=nu(4),
    value=eta(7),
  )

  assert statement.expression == nu(4)
  assert statement.value == eta(7)


def test_hopf_invariant_statement_has_structural_equality():
  first = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
  )

  second = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
  )

  assert first == second


def test_hopf_invariant_statement_distinguishes_expression():
  first = HopfInvariantStatement(
    expression=eta(4),
    value=eta(7),
  )

  different_expression = (
    HopfInvariantStatement(
      expression=nu(4),
      value=eta(7),
    )
  )

  assert first != different_expression


def test_hopf_invariant_statement_distinguishes_value():
  first = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
  )

  different_value = (
    HopfInvariantStatement(
      expression=nu(4),
      value=Zero(),
    )
  )

  assert first != different_value


def test_hopf_invariant_statement_supports_zero_value():
  statement = HopfInvariantStatement(
    expression=nu(4),
    value=Zero(),
  )

  assert statement.value == Zero()


def test_hopf_invariant_statement_supports_multiple_value():
  statement = HopfInvariantStatement(
    expression=nu(4),
    value=Multiple(
      coefficient=2,
      expression=eta(7),
    ),
  )

  assert statement.value == Multiple(
    coefficient=2,
    expression=eta(7),
  )


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
    expression=nu(4),
    value=eta(7),
    source=reference,
    note="known generalized Hopf invariant fact",
  )

  assert statement.source == reference

  assert (
    statement.note
    == "known generalized Hopf invariant fact"
  )


def test_hopf_invariant_proof_step():
  statement = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
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
    expression=nu(4),
    value=eta(7),
    source=reference,
    note="known generalized Hopf invariant fact",
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
    == "known generalized Hopf invariant fact"
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


def test_hopf_composition_law_statement():
  statement = HopfCompositionLawStatement(
    alpha=nu(4),
    beta=eta(7),
  )

  assert statement.alpha == nu(4)
  assert statement.beta == eta(7)


def test_hopf_invariant_implies_hopf_composition_law_statement():
  hopf_statement = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
  )

  premise = hopf_invariant_proof_step(
    hopf_statement
  )

  rule = (
    hopf_composition_law_inference_rule()
  )

  match = find_inference_match(
    rule,
    premise,
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    HopfCompositionLawStatement(
      alpha=nu(4),
      beta=eta(7),
    )
  )

  assert step.premises == (
    premise,
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule


def test_hopf_composition_law_inference_preserves_hopf_fact_provenance():
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

  hopf_statement = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
    source=reference,
    note=(
      "known generalized "
      "Hopf invariant fact"
    ),
  )

  premise = hopf_invariant_proof_step(
    hopf_statement
  )

  rule = (
    hopf_composition_law_inference_rule()
  )

  match = find_inference_match(
    rule,
    premise,
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    HopfCompositionLawStatement(
      alpha=nu(4),
      beta=eta(7),
    )
  )

  assert step.premises == (
    premise,
  )

  assert (
    step.premises[0].conclusion.source
    == reference
  )

  assert (
    step.premises[0].conclusion.note
    == (
      "known generalized "
      "Hopf invariant fact"
    )
  )

  assert step.inference_rule == rule


def test_hopf_composition_law_inference_rejects_non_hopf_statement():
  premise = ProofStep(
    conclusion=eta(2),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    hopf_composition_law_inference_rule()
  )

  match = find_inference_match(
    rule,
    premise,
  )

  assert match is None






