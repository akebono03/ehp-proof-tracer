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
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  order_relation,
  relation_proof_step,
  run_inference_until_stable_with_history,
)
from relation_rules import (
  equality_symmetry_inference_rule,
)
from scalar_rules import (
  EvenScalarStatement,
  OddScalarStatement,
  ScalarCongruenceStatement,
  even_scalar_implies_mod_two_congruence_inference_rule,
  mod_two_one_scalar_preserves_order_two_element_inference_rule,
  odd_scalar_implies_mod_two_congruence_inference_rule,
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


def test_odd_scalar_implies_mod_two_congruence():
  k = ScalarSymbol(
    name="k",
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=k,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    odd_scalar_implies_mod_two_congruence_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      odd_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == ScalarCongruenceStatement(
    scalar=k,
    residue=1,
    modulus=2,
  )

  assert derived_step.rule == ProofRule.INFERENCE

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    odd_step,
  )


def test_odd_scalar_rule_rejects_even_scalar_statement():
  k = ScalarSymbol(
    name="k",
  )

  even_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=k,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    odd_scalar_implies_mod_two_congruence_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
    ),
  )

  assert match is None


def test_even_scalar_implies_mod_two_congruence():
  k = ScalarSymbol(
    name="k",
  )

  even_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=k,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    even_scalar_implies_mod_two_congruence_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == ScalarCongruenceStatement(
    scalar=k,
    residue=0,
    modulus=2,
  )

  assert derived_step.rule == ProofRule.INFERENCE

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    even_step,
  )


def test_even_scalar_rule_rejects_odd_scalar_statement():
  k = ScalarSymbol(
    name="k",
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=k,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    even_scalar_implies_mod_two_congruence_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      odd_step,
    ),
  )

  assert match is None


def test_mod_two_one_scalar_preserves_order_two_element():
  k = ScalarSymbol(
    name="k",
  )

  beta = nu(4)

  order_step = relation_proof_step(
    order_relation(
      beta,
      2,
    )
  )

  congruence_step = ProofStep(
    conclusion=ScalarCongruenceStatement(
      scalar=k,
      residue=1,
      modulus=2,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    mod_two_one_scalar_preserves_order_two_element_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      order_step,
      congruence_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == Relation(
    lhs=Multiple(
      coefficient=k,
      expression=beta,
    ),
    rhs=beta,
    relation_type=RelationType.EQUALITY,
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    order_step,
    congruence_step,
  )


def test_mod_two_one_scalar_rule_rejects_non_order_two_element():
  k = ScalarSymbol(
    name="k",
  )

  beta = nu(4)

  order_step = relation_proof_step(
    order_relation(
      beta,
      3,
    )
  )

  congruence_step = ProofStep(
    conclusion=ScalarCongruenceStatement(
      scalar=k,
      residue=1,
      modulus=2,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    mod_two_one_scalar_preserves_order_two_element_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      order_step,
      congruence_step,
    ),
  )

  assert match is None


def test_mod_two_one_scalar_rule_rejects_zero_mod_two_scalar():
  k = ScalarSymbol(
    name="k",
  )

  beta = nu(4)

  order_step = relation_proof_step(
    order_relation(
      beta,
      2,
    )
  )

  congruence_step = ProofStep(
    conclusion=ScalarCongruenceStatement(
      scalar=k,
      residue=0,
      modulus=2,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    mod_two_one_scalar_preserves_order_two_element_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      order_step,
      congruence_step,
    ),
  )

  assert match is None


def test_odd_scalar_and_order_two_reach_symbolic_multiple_equality():
  k = ScalarSymbol(
    name="k",
  )

  beta = nu(4)

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=k,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  order_step = relation_proof_step(
    order_relation(
      beta,
      2,
    )
  )

  parity_rule = (
    odd_scalar_implies_mod_two_congruence_inference_rule()
  )

  order_bridge_rule = (
    mod_two_one_scalar_preserves_order_two_element_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      (
        parity_rule,
        order_bridge_rule,
      ),
      (
        odd_step,
        order_step,
      ),
    )
  )

  congruence = ScalarCongruenceStatement(
    scalar=k,
    residue=1,
    modulus=2,
  )

  symbolic_equality = Relation(
    lhs=Multiple(
      coefficient=k,
      expression=beta,
    ),
    rhs=beta,
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert congruence in conclusions

  assert symbolic_equality in conclusions

  congruence_step = next(
    step
    for step in result.steps
    if step.conclusion == congruence
  )

  equality_step = next(
    step
    for step in result.steps
    if step.conclusion == symbolic_equality
  )

  assert congruence_step.premises == (
    odd_step,
  )

  assert congruence_step.inference_rule == (
    parity_rule
  )

  assert equality_step.premises == (
    order_step,
    congruence_step,
  )

  assert equality_step.inference_rule == (
    order_bridge_rule
  )



