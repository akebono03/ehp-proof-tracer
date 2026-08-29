from expression import (
  MapApplication,
  MapSymbol,
  Multiple,
  Sum,
  Suspension,
  Zero,
  eta,
  nu,
)
from homomorphism_rules import (
  SUSPENSION_MAP,
  HomomorphismStatement,
  homomorphism_preserves_addition_inference_rule,
  homomorphism_preserves_inverse_inference_rule,
  homomorphism_preserves_known_zero_inference_rule,
  homomorphism_preserves_multiple_inference_rule,
  homomorphism_preserves_zero_inference_rule,
  suspension_additivity_bridge_inference_rule,
  suspension_is_homomorphism_inference_rule,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  order_relation,
  relation_proof_step,
  run_inference_round,
  run_inference_until_stable_with_history,
)
from relation_rules import (
  equality_symmetry_inference_rule,
  order_implies_zero_multiple_inference_rule,
  zero_equality_implies_zero_inference_rule,
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


def test_homomorphism_preserves_inverse():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_inverse_inference_rule(
      alpha,
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
      expression=Multiple(
        coefficient=-1,
        expression=alpha,
      ),
    ),
    rhs=Multiple(
      coefficient=-1,
      expression=MapApplication(
        map=f,
        expression=alpha,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )


def test_homomorphism_preserves_inverse_requires_homomorphism_statement():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  unrelated_step = ProofStep(
    conclusion=f,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_inverse_inference_rule(
      alpha,
    )
  )

  match = find_inference_match(
    rule,
    (
      unrelated_step,
    ),
  )

  assert match is None


def test_homomorphism_preserves_inverse_uses_map_from_premise():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  alpha = eta(3)

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
    homomorphism_preserves_inverse_inference_rule(
      alpha,
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

  conclusions = tuple(
    step.conclusion
    for step in new_steps
  )

  assert Relation(
    lhs=MapApplication(
      map=f,
      expression=Multiple(
        coefficient=-1,
        expression=alpha,
      ),
    ),
    rhs=Multiple(
      coefficient=-1,
      expression=MapApplication(
        map=f,
        expression=alpha,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  ) in conclusions

  assert Relation(
    lhs=MapApplication(
      map=g,
      expression=Multiple(
        coefficient=-1,
        expression=alpha,
      ),
    ),
    rhs=Multiple(
      coefficient=-1,
      expression=MapApplication(
        map=g,
        expression=alpha,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  ) in conclusions


def test_homomorphism_preserves_inverse_preserves_provenance():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_inverse_inference_rule(
      alpha,
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


def test_homomorphism_preserves_inverse_keeps_structural_sides_distinct():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  left = MapApplication(
    map=f,
    expression=Multiple(
      coefficient=-1,
      expression=alpha,
    ),
  )

  right = Multiple(
    coefficient=-1,
    expression=MapApplication(
      map=f,
      expression=alpha,
    ),
  )

  assert left != right


def test_homomorphism_preserves_multiple():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=2,
      expression=alpha,
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
      expression=Multiple(
        coefficient=2,
        expression=alpha,
      ),
    ),
    rhs=Multiple(
      coefficient=2,
      expression=MapApplication(
        map=f,
        expression=alpha,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )


def test_homomorphism_preserves_multiple_with_negative_coefficient():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=-3,
      expression=alpha,
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
      expression=Multiple(
        coefficient=-3,
        expression=alpha,
      ),
    ),
    rhs=Multiple(
      coefficient=-3,
      expression=MapApplication(
        map=f,
        expression=alpha,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )


def test_homomorphism_preserves_multiple_requires_homomorphism_statement():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  unrelated_step = ProofStep(
    conclusion=f,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=2,
      expression=alpha,
    )
  )

  match = find_inference_match(
    rule,
    (
      unrelated_step,
    ),
  )

  assert match is None


def test_homomorphism_preserves_multiple_uses_map_from_premise():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  alpha = eta(3)

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
    homomorphism_preserves_multiple_inference_rule(
      coefficient=2,
      expression=alpha,
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

  conclusions = tuple(
    step.conclusion
    for step in new_steps
  )

  assert Relation(
    lhs=MapApplication(
      map=f,
      expression=Multiple(
        coefficient=2,
        expression=alpha,
      ),
    ),
    rhs=Multiple(
      coefficient=2,
      expression=MapApplication(
        map=f,
        expression=alpha,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  ) in conclusions

  assert Relation(
    lhs=MapApplication(
      map=g,
      expression=Multiple(
        coefficient=2,
        expression=alpha,
      ),
    ),
    rhs=Multiple(
      coefficient=2,
      expression=MapApplication(
        map=g,
        expression=alpha,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  ) in conclusions


def test_homomorphism_preserves_multiple_preserves_provenance():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=2,
      expression=alpha,
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


def test_homomorphism_preserves_multiple_keeps_structural_sides_distinct():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  left = MapApplication(
    map=f,
    expression=Multiple(
      coefficient=2,
      expression=alpha,
    ),
  )

  right = Multiple(
    coefficient=2,
    expression=MapApplication(
      map=f,
      expression=alpha,
    ),
  )

  assert left != right


def test_suspension_is_homomorphism():
  rule = (
    suspension_is_homomorphism_inference_rule()
  )

  result = run_inference_round(
    (
      rule,
    ),
    (),
  )

  assert HomomorphismStatement(
    map=SUSPENSION_MAP,
  ) in tuple(
    step.conclusion
    for step in result
  )


def test_suspension_additivity_bridge():
  alpha = eta(3)
  beta = nu(4)

  generic_additivity_step = (
    relation_proof_step(
      Relation(
        lhs=MapApplication(
          map=SUSPENSION_MAP,
          expression=Sum(
            left=alpha,
            right=beta,
          ),
        ),
        rhs=Sum(
          left=MapApplication(
            map=SUSPENSION_MAP,
            expression=alpha,
          ),
          right=MapApplication(
            map=SUSPENSION_MAP,
            expression=beta,
          ),
        ),
        relation_type=(
          RelationType.EQUALITY
        ),
      )
    )
  )

  rule = (
    suspension_additivity_bridge_inference_rule(
      alpha,
      beta,
    )
  )

  match = find_inference_match(
    rule,
    (
      generic_additivity_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == Relation(
    lhs=Suspension(
      expression=Sum(
        left=alpha,
        right=beta,
      ),
    ),
    rhs=Sum(
      left=Suspension(
        expression=alpha,
      ),
      right=Suspension(
        expression=beta,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )


def test_suspension_additivity_bridge_requires_generic_additivity():
  alpha = eta(3)
  beta = nu(4)

  unrelated_step = relation_proof_step(
    Relation(
      lhs=alpha,
      rhs=beta,
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = (
    suspension_additivity_bridge_inference_rule(
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


def test_suspension_additivity_bridge_rejects_different_map():
  alpha = eta(3)
  beta = nu(4)

  other_map = MapSymbol(
    name="f",
  )

  generic_additivity_step = (
    relation_proof_step(
      Relation(
        lhs=MapApplication(
          map=other_map,
          expression=Sum(
            left=alpha,
            right=beta,
          ),
        ),
        rhs=Sum(
          left=MapApplication(
            map=other_map,
            expression=alpha,
          ),
          right=MapApplication(
            map=other_map,
            expression=beta,
          ),
        ),
        relation_type=(
          RelationType.EQUALITY
        ),
      )
    )
  )

  rule = (
    suspension_additivity_bridge_inference_rule(
      alpha,
      beta,
    )
  )

  match = find_inference_match(
    rule,
    (
      generic_additivity_step,
    ),
  )

  assert match is None


def test_suspension_homomorphism_additivity_integration():
  alpha = eta(3)
  beta = nu(4)

  suspension_homomorphism_rule = (
    suspension_is_homomorphism_inference_rule()
  )

  generic_additivity_rule = (
    homomorphism_preserves_addition_inference_rule(
      alpha,
      beta,
    )
  )

  bridge_rule = (
    suspension_additivity_bridge_inference_rule(
      alpha,
      beta,
    )
  )

  result = (
    run_inference_until_stable_with_history(
      (
        suspension_homomorphism_rule,
        generic_additivity_rule,
        bridge_rule,
      ),
      (),
    )
  )

  expected_generic_additivity = Relation(
    lhs=MapApplication(
      map=SUSPENSION_MAP,
      expression=Sum(
        left=alpha,
        right=beta,
      ),
    ),
    rhs=Sum(
      left=MapApplication(
        map=SUSPENSION_MAP,
        expression=alpha,
      ),
      right=MapApplication(
        map=SUSPENSION_MAP,
        expression=beta,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  expected_suspension_additivity = Relation(
    lhs=Suspension(
      expression=Sum(
        left=alpha,
        right=beta,
      ),
    ),
    rhs=Sum(
      left=Suspension(
        expression=alpha,
      ),
      right=Suspension(
        expression=beta,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert HomomorphismStatement(
    map=SUSPENSION_MAP,
  ) in conclusions

  assert (
    expected_generic_additivity
    in conclusions
  )

  assert (
    expected_suspension_additivity
    in conclusions
  )


def test_suspension_additivity_bridge_preserves_provenance():
  alpha = eta(3)
  beta = nu(4)

  generic_additivity_step = (
    relation_proof_step(
      Relation(
        lhs=MapApplication(
          map=SUSPENSION_MAP,
          expression=Sum(
            left=alpha,
            right=beta,
          ),
        ),
        rhs=Sum(
          left=MapApplication(
            map=SUSPENSION_MAP,
            expression=alpha,
          ),
          right=MapApplication(
            map=SUSPENSION_MAP,
            expression=beta,
          ),
        ),
        relation_type=(
          RelationType.EQUALITY
        ),
      )
    )
  )

  rule = (
    suspension_additivity_bridge_inference_rule(
      alpha,
      beta,
    )
  )

  match = find_inference_match(
    rule,
    (
      generic_additivity_step,
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
    generic_additivity_step,
  )


def test_homomorphism_preserves_known_zero():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  zero_expression = Multiple(
    coefficient=2,
    expression=alpha,
  )

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_step = relation_proof_step(
    Relation(
      lhs=zero_expression,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    homomorphism_preserves_known_zero_inference_rule(
      zero_expression,
    )
  )

  match = find_inference_match(
    rule,
    (
      homomorphism_step,
      zero_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == Relation(
    lhs=MapApplication(
      map=f,
      expression=zero_expression,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    homomorphism_step,
    zero_step,
  )


def test_homomorphism_preserves_known_zero_requires_homomorphism_statement():
  alpha = eta(3)

  zero_expression = Multiple(
    coefficient=2,
    expression=alpha,
  )

  zero_step = relation_proof_step(
    Relation(
      lhs=zero_expression,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    homomorphism_preserves_known_zero_inference_rule(
      zero_expression,
    )
  )

  match = find_inference_match(
    rule,
    (
      zero_step,
    ),
  )

  assert match is None


def test_homomorphism_preserves_known_zero_requires_zero_relation():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  zero_expression = Multiple(
    coefficient=2,
    expression=alpha,
  )

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  unrelated_step = relation_proof_step(
    Relation(
      lhs=zero_expression,
      rhs=eta(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = (
    homomorphism_preserves_known_zero_inference_rule(
      zero_expression,
    )
  )

  match = find_inference_match(
    rule,
    (
      homomorphism_step,
      unrelated_step,
    ),
  )

  assert match is None


def test_homomorphism_preserves_known_zero_rejects_different_expression():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)
  beta = nu(4)

  target_expression = Multiple(
    coefficient=2,
    expression=alpha,
  )

  other_expression = Multiple(
    coefficient=2,
    expression=beta,
  )

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_step = relation_proof_step(
    Relation(
      lhs=other_expression,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    homomorphism_preserves_known_zero_inference_rule(
      target_expression,
    )
  )

  match = find_inference_match(
    rule,
    (
      homomorphism_step,
      zero_step,
    ),
  )

  assert match is None


def test_phase13_order_homomorphism_integration_reaches_zero_multiple():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  order_step = relation_proof_step(
    order_relation(
      alpha,
      2,
    )
  )

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  double_alpha = Multiple(
    coefficient=2,
    expression=alpha,
  )

  f_alpha = MapApplication(
    map=f,
    expression=alpha,
  )

  f_double_alpha = MapApplication(
    map=f,
    expression=double_alpha,
  )

  double_f_alpha = Multiple(
    coefficient=2,
    expression=f_alpha,
  )

  order_rule = (
    order_implies_zero_multiple_inference_rule()
  )

  multiple_rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=2,
      expression=alpha,
    )
  )

  known_zero_rule = (
    homomorphism_preserves_known_zero_inference_rule(
      double_alpha,
    )
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  zero_propagation_rule = (
    zero_equality_implies_zero_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      (
        order_rule,
        multiple_rule,
        known_zero_rule,
        symmetry_rule,
        zero_propagation_rule,
      ),
      (
        order_step,
        homomorphism_step,
      ),
    )
  )

  order_zero = Relation(
    lhs=double_alpha,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  multiple_preservation = Relation(
    lhs=f_double_alpha,
    rhs=double_f_alpha,
    relation_type=RelationType.EQUALITY,
  )

  mapped_zero = Relation(
    lhs=f_double_alpha,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  reverse_multiple_preservation = Relation(
    lhs=double_f_alpha,
    rhs=f_double_alpha,
    relation_type=RelationType.EQUALITY,
  )

  final_zero = Relation(
    lhs=double_f_alpha,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert order_zero in conclusions
  assert multiple_preservation in conclusions
  assert mapped_zero in conclusions
  assert (
    reverse_multiple_preservation
    in conclusions
  )
  assert final_zero in conclusions


def test_phase13_order_homomorphism_integration_preserves_provenance():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  order_step = relation_proof_step(
    order_relation(
      alpha,
      2,
    )
  )

  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  double_alpha = Multiple(
    coefficient=2,
    expression=alpha,
  )

  f_alpha = MapApplication(
    map=f,
    expression=alpha,
  )

  f_double_alpha = MapApplication(
    map=f,
    expression=double_alpha,
  )

  double_f_alpha = Multiple(
    coefficient=2,
    expression=f_alpha,
  )

  order_rule = (
    order_implies_zero_multiple_inference_rule()
  )

  multiple_rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=2,
      expression=alpha,
    )
  )

  known_zero_rule = (
    homomorphism_preserves_known_zero_inference_rule(
      double_alpha,
    )
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  zero_propagation_rule = (
    zero_equality_implies_zero_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      (
        order_rule,
        multiple_rule,
        known_zero_rule,
        symmetry_rule,
        zero_propagation_rule,
      ),
      (
        order_step,
        homomorphism_step,
      ),
    )
  )

  order_zero = Relation(
    lhs=double_alpha,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  multiple_preservation = Relation(
    lhs=f_double_alpha,
    rhs=double_f_alpha,
    relation_type=RelationType.EQUALITY,
  )

  mapped_zero = Relation(
    lhs=f_double_alpha,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  reverse_multiple_preservation = Relation(
    lhs=double_f_alpha,
    rhs=f_double_alpha,
    relation_type=RelationType.EQUALITY,
  )

  final_zero = Relation(
    lhs=double_f_alpha,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  order_zero_step = next(
    step
    for step in result.steps
    if step.conclusion == order_zero
  )

  multiple_step = next(
    step
    for step in result.steps
    if step.conclusion
    == multiple_preservation
  )

  mapped_zero_step = next(
    step
    for step in result.steps
    if step.conclusion == mapped_zero
  )

  reverse_multiple_step = next(
    step
    for step in result.steps
    if step.conclusion
    == reverse_multiple_preservation
  )

  final_zero_step = next(
    step
    for step in result.steps
    if step.conclusion == final_zero
  )

  assert order_zero_step.premises == (
    order_step,
  )

  assert order_zero_step.inference_rule == (
    order_rule
  )

  assert multiple_step.premises == (
    homomorphism_step,
  )

  assert multiple_step.inference_rule == (
    multiple_rule
  )

  assert mapped_zero_step.premises == (
    homomorphism_step,
    order_zero_step,
  )

  assert mapped_zero_step.inference_rule == (
    known_zero_rule
  )

  assert reverse_multiple_step.premises == (
    multiple_step,
  )

  assert reverse_multiple_step.inference_rule == (
    symmetry_rule
  )

  assert final_zero_step.premises == (
    mapped_zero_step,
    reverse_multiple_step,
  )

  assert final_zero_step.inference_rule == (
    zero_propagation_rule
  )

  assert final_zero_step.rule == (
    ProofRule.INFERENCE
  )














