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
  relation_proof_step,
  run_inference_round,
  run_inference_until_stable_with_history,
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










