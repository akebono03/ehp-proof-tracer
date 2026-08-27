import pytest

from expression import (
  Composition,
  Multiple,
  Suspension,
  Zero,
  eta,
  nu,
)
from hopf_rules import (
  HopfCompositionLawStatement,
  HopfInvariantStatement,
  hopf_composition_formula_inference_rule,
  hopf_composition_law_inference_rule,
  hopf_invariant_proof_step,
  hopf_invariant_value_zero_inference_rule,
)
from proof import (
  LiteratureReference,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
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


def test_hopf_composition_formula():
  law_statement = (
    HopfCompositionLawStatement(
      alpha=nu(4),
      beta=eta(7),
    )
  )

  law_step = ProofStep(
    conclusion=law_statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  gamma = eta(8)

  gamma_step = ProofStep(
    conclusion=gamma,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    hopf_composition_formula_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      law_step,
      gamma_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    HopfInvariantStatement(
      expression=Composition(
        left=nu(4),
        right=Suspension(
          expression=eta(8),
        ),
      ),
      value=Composition(
        left=eta(7),
        right=Suspension(
          expression=eta(8),
        ),
      ),
    )
  )

  assert step.premises == (
    law_step,
    gamma_step,
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule


def test_hopf_invariant_reaches_hopf_composition_formula():
  hopf_statement = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
  )

  hopf_step = hopf_invariant_proof_step(
    hopf_statement
  )

  law_rule = (
    hopf_composition_law_inference_rule()
  )

  law_match = find_inference_match(
    law_rule,
    hopf_step,
  )

  assert law_match is not None

  law_step = apply_inference_match(
    law_match
  )

  gamma = eta(8)

  gamma_step = ProofStep(
    conclusion=gamma,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  formula_rule = (
    hopf_composition_formula_inference_rule()
  )

  formula_match = find_inference_match(
    formula_rule,
    (
      law_step,
      gamma_step,
    ),
  )

  assert formula_match is not None

  formula_step = apply_inference_match(
    formula_match
  )

  assert formula_step.conclusion == (
    HopfInvariantStatement(
      expression=Composition(
        left=nu(4),
        right=Suspension(
          expression=eta(8),
        ),
      ),
      value=Composition(
        left=eta(7),
        right=Suspension(
          expression=eta(8),
        ),
      ),
    )
  )

  assert formula_step.premises == (
    law_step,
    gamma_step,
  )

  assert law_step.premises == (
    hopf_step,
  )


def test_hopf_composition_formula_rejects_missing_law_statement():
  unrelated_step = ProofStep(
    conclusion=nu(4),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  gamma_step = ProofStep(
    conclusion=eta(8),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    hopf_composition_formula_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      unrelated_step,
      gamma_step,
    ),
  )

  assert match is None


def test_hopf_invariant_value_zero():
  value = Composition(
    left=eta(7),
    right=Suspension(
      expression=eta(8),
    ),
  )

  hopf_step = ProofStep(
    conclusion=HopfInvariantStatement(
      expression=nu(4),
      value=value,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_step = ProofStep(
    conclusion=Relation(
      lhs=value,
      rhs=Zero(),
      relation_type=(
        RelationType.ZERO
      ),
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  rule = (
    hopf_invariant_value_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      hopf_step,
      zero_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    HopfInvariantStatement(
      expression=nu(4),
      value=Zero(),
    )
  )

  assert step.premises == (
    hopf_step,
    zero_step,
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule


def test_hopf_invariant_value_zero_rejects_unrelated_zero():
  value = Composition(
    left=eta(7),
    right=Suspension(
      expression=eta(8),
    ),
  )

  unrelated_value = Composition(
    left=nu(7),
    right=Suspension(
      expression=eta(8),
    ),
  )

  hopf_step = ProofStep(
    conclusion=HopfInvariantStatement(
      expression=nu(4),
      value=value,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_step = ProofStep(
    conclusion=Relation(
      lhs=unrelated_value,
      rhs=Zero(),
      relation_type=(
        RelationType.ZERO
      ),
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  rule = (
    hopf_invariant_value_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      hopf_step,
      zero_step,
    ),
  )

  assert match is None


def test_hopf_invariant_zero_does_not_mean_expression_zero():
  hopf_step = ProofStep(
    conclusion=HopfInvariantStatement(
      expression=nu(4),
      value=Zero(),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    hopf_invariant_value_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    hopf_step,
  )

  assert match is None











