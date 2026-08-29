from expression import (
  MapApplication,
  MapSymbol,
  Sum,
  Zero,
  eta,
  nu,
)
from homomorphism_rules import (
  HomomorphismStatement,
  homomorphism_preserves_addition_inference_rule,
  homomorphism_preserves_zero_inference_rule,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  run_inference_round,
)


def test_homomorphism_statement():
  f = MapSymbol(
    name="f",
  )

  statement = HomomorphismStatement(
    map=f,
  )

  assert statement.map == f


def test_homomorphism_statement_has_structural_equality():
  f = MapSymbol(
    name="f",
  )

  first = HomomorphismStatement(
    map=f,
  )

  second = HomomorphismStatement(
    map=f,
  )

  assert first == second


def test_homomorphism_statement_distinguishes_map():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  f_statement = HomomorphismStatement(
    map=f,
  )

  g_statement = HomomorphismStatement(
    map=g,
  )

  assert f_statement != g_statement


def test_homomorphism_preserves_addition():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)
  beta = nu(4)

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_addition_inference_rule(
      alpha,
      beta,
    )
  )

  match = find_inference_match(
    rule,
    (
      homomorphism_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == Relation(
    lhs=MapApplication(
      map=f,
      expression=Sum(
        left=alpha,
        right=beta,
      ),
    ),
    rhs=Sum(
      left=MapApplication(
        map=f,
        expression=alpha,
      ),
      right=MapApplication(
        map=f,
        expression=beta,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )


def test_homomorphism_preserves_addition_requires_homomorphism_statement():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)
  beta = nu(4)

  unrelated_step = ProofStep(
    conclusion=f,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_addition_inference_rule(
      alpha,
      beta,
    )
  )

  match = find_inference_match(
    rule,
    (
      unrelated_step,
    ),
  )

  assert match is None


def test_homomorphism_preserves_addition_uses_map_from_premise():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  alpha = eta(3)
  beta = nu(4)

  f_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  g_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=g,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_addition_inference_rule(
      alpha,
      beta,
    )
  )

  new_steps = run_inference_round(
    (
      rule,
    ),
    (
      f_step,
      g_step,
    ),
  )

  assert Relation(
    lhs=MapApplication(
      map=f,
      expression=Sum(
        left=alpha,
        right=beta,
      ),
    ),
    rhs=Sum(
      left=MapApplication(
        map=f,
        expression=alpha,
      ),
      right=MapApplication(
        map=f,
        expression=beta,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  ) in tuple(
    step.conclusion
    for step in new_steps
  )

  assert Relation(
    lhs=MapApplication(
      map=g,
      expression=Sum(
        left=alpha,
        right=beta,
      ),
    ),
    rhs=Sum(
      left=MapApplication(
        map=g,
        expression=alpha,
      ),
      right=MapApplication(
        map=g,
        expression=beta,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  ) in tuple(
    step.conclusion
    for step in new_steps
  )


def test_homomorphism_preserves_addition_preserves_provenance():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)
  beta = nu(4)

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_addition_inference_rule(
      alpha,
      beta,
    )
  )

  match = find_inference_match(
    rule,
    (
      homomorphism_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    homomorphism_step,
  )


def test_homomorphism_preserves_addition_keeps_structural_sides_distinct():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)
  beta = nu(4)

  left = MapApplication(
    map=f,
    expression=Sum(
      left=alpha,
      right=beta,
    ),
  )

  right = Sum(
    left=MapApplication(
      map=f,
      expression=alpha,
    ),
    right=MapApplication(
      map=f,
      expression=beta,
    ),
  )

  assert left != right


def test_homomorphism_preserves_zero():
  f = MapSymbol(
    name="f",
  )

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      homomorphism_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == Relation(
    lhs=MapApplication(
      map=f,
      expression=Zero(),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )


def test_homomorphism_preserves_zero_requires_homomorphism_statement():
  f = MapSymbol(
    name="f",
  )

  unrelated_step = ProofStep(
    conclusion=f,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      unrelated_step,
    ),
  )

  assert match is None


def test_homomorphism_preserves_zero_uses_map_from_premise():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  f_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  g_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=g,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_zero_inference_rule()
  )

  new_steps = run_inference_round(
    (
      rule,
    ),
    (
      f_step,
      g_step,
    ),
  )

  conclusions = tuple(
    step.conclusion
    for step in new_steps
  )

  assert Relation(
    lhs=MapApplication(
      map=f,
      expression=Zero(),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  ) in conclusions

  assert Relation(
    lhs=MapApplication(
      map=g,
      expression=Zero(),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  ) in conclusions


def test_homomorphism_preserves_zero_preserves_provenance():
  f = MapSymbol(
    name="f",
  )

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      homomorphism_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    homomorphism_step,
  )







