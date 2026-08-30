from expression import (
  Multiple,
  ScalarSymbol,
  Sum,
  eta,
  nu,
  sigma,
)
from proof import (
  ProofRule,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  relation_proof_step,
)
from relation_rules import (
  equality_symmetry_inference_rule,
)
from scalar_rules import (
  EvenScalarStatement,
  OddScalarStatement,
  ScalarCongruenceStatement,
)


def test_odd_scalar_statement():
  k = ScalarSymbol(
    name="k",
  )

  statement = OddScalarStatement(
    scalar=k,
  )

  assert statement.scalar == k


def test_odd_scalar_statement_has_structural_equality():
  first = OddScalarStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
  )

  second = OddScalarStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
  )

  assert first == second


def test_odd_scalar_statement_distinguishes_scalar():
  k_statement = OddScalarStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
  )

  ell_statement = OddScalarStatement(
    scalar=ScalarSymbol(
      name="l",
    ),
  )

  assert k_statement != ell_statement


def test_even_scalar_statement():
  k = ScalarSymbol(
    name="k",
  )

  statement = EvenScalarStatement(
    scalar=k,
  )

  assert statement.scalar == k


def test_even_scalar_statement_has_structural_equality():
  first = EvenScalarStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
  )

  second = EvenScalarStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
  )

  assert first == second


def test_scalar_congruence_statement():
  k = ScalarSymbol(
    name="k",
  )

  statement = ScalarCongruenceStatement(
    scalar=k,
    residue=1,
    modulus=2,
  )

  assert statement.scalar == k
  assert statement.residue == 1
  assert statement.modulus == 2


def test_scalar_congruence_statement_has_structural_equality():
  first = ScalarCongruenceStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
    residue=1,
    modulus=2,
  )

  second = ScalarCongruenceStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
    residue=1,
    modulus=2,
  )

  assert first == second


def test_scalar_congruence_statement_distinguishes_constraints():
  odd_congruence = ScalarCongruenceStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
    residue=1,
    modulus=2,
  )

  other_congruence = ScalarCongruenceStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
    residue=0,
    modulus=2,
  )

  assert odd_congruence != other_congruence


def test_symbolic_additive_equality():
  k = ScalarSymbol(
    name="k",
  )

  alpha = eta(3)
  beta = nu(4)
  gamma = sigma(8)

  equality = Relation(
    lhs=alpha,
    rhs=Sum(
      left=Multiple(
        coefficient=k,
        expression=beta,
      ),
      right=gamma,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert equality.lhs == alpha

  assert equality.rhs == Sum(
    left=Multiple(
      coefficient=ScalarSymbol(
        name="k",
      ),
      expression=beta,
    ),
    right=gamma,
  )

  assert equality.relation_type == (
    RelationType.EQUALITY
  )


def test_symbolic_additive_equality_uses_generic_equality_reasoning():
  k = ScalarSymbol(
    name="k",
  )

  alpha = eta(3)
  beta = nu(4)
  gamma = sigma(8)

  equality = Relation(
    lhs=alpha,
    rhs=Sum(
      left=Multiple(
        coefficient=k,
        expression=beta,
      ),
      right=gamma,
    ),
    relation_type=RelationType.EQUALITY,
  )

  equality_step = relation_proof_step(
    equality
  )

  rule = equality_symmetry_inference_rule()

  match = find_inference_match(
    rule,
    (
      equality_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == Relation(
    lhs=Sum(
      left=Multiple(
        coefficient=k,
        expression=beta,
      ),
      right=gamma,
    ),
    rhs=alpha,
    relation_type=RelationType.EQUALITY,
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    equality_step,
  )






