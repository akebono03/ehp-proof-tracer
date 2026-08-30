from algebra import (
  GroupElement,
  Subgroup,
  generated_subgroup_elements,
)
from expression import (
  Multiple,
  ScalarSymbol,
  Sum,
  eta,
  nu,
  sigma,
)
from indeterminacy_rules import (
  CoefficientIndeterminacyStatement,
  CosetMembershipStatement,
  SignIndeterminacyStatement,
  coset_membership_implies_modulo_inference_rule,
  equality_implies_sign_indeterminacy_inference_rule,
  modulo_implies_coset_membership_inference_rule,
)
from models import (
  AbelianGroup,
  GroupComponent,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  derive_inference_round_result,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  OddScalarStatement,
)
from set_rules import (
  Coset,
  MembershipStatement,
  ModuloStatement,
)


def make_cyclic_group(
  order,
  generator,
):
  return AbelianGroup(
    n=0,
    k=0,
    components=[
      GroupComponent(
        id=0,
        order=order,
        generator=generator,
        element=[],
        gen_coe=[],
      )
    ],
  )


def make_subgroup(
  group,
  generators,
):
  generators = tuple(
    GroupElement(
      group,
      coefficients,
    )
    for coefficients in generators
  )

  elements = generated_subgroup_elements(
    group,
    generators,
  )

  return Subgroup(
    ambient_group=group,
    elements=elements,
    generators=generators,
  )


def test_coset_membership_statement():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)
  beta = nu(4)

  coset = Coset(
    representative=beta,
    subgroup=subgroup,
  )

  statement = CosetMembershipStatement(
    element=alpha,
    coset=coset,
  )

  assert statement.element == alpha
  assert statement.coset == coset


def test_coset_membership_statement_has_structural_equality():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  first = CosetMembershipStatement(
    element=eta(3),
    coset=Coset(
      representative=nu(4),
      subgroup=subgroup,
    ),
  )

  second = CosetMembershipStatement(
    element=eta(3),
    coset=Coset(
      representative=nu(4),
      subgroup=subgroup,
    ),
  )

  assert first == second


def test_coset_membership_statement_distinguishes_element():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  first = CosetMembershipStatement(
    element=eta(3),
    coset=Coset(
      representative=nu(4),
      subgroup=subgroup,
    ),
  )

  second = CosetMembershipStatement(
    element=nu(4),
    coset=Coset(
      representative=nu(4),
      subgroup=subgroup,
    ),
  )

  assert first != second


def test_coset_membership_statement_distinguishes_coset():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  first = CosetMembershipStatement(
    element=eta(3),
    coset=Coset(
      representative=nu(4),
      subgroup=subgroup,
    ),
  )

  second = CosetMembershipStatement(
    element=eta(3),
    coset=Coset(
      representative=eta(3),
      subgroup=subgroup,
    ),
  )

  assert first != second


def test_sign_indeterminacy_statement():
  alpha = eta(3)
  beta = nu(4)

  statement = SignIndeterminacyStatement(
    value=alpha,
    representative=beta,
  )

  assert statement.value == alpha
  assert statement.representative == beta


def test_sign_indeterminacy_statement_has_structural_equality():
  first = SignIndeterminacyStatement(
    value=eta(3),
    representative=nu(4),
  )

  second = SignIndeterminacyStatement(
    value=eta(3),
    representative=nu(4),
  )

  assert first == second


def test_sign_indeterminacy_statement_distinguishes_value():
  first = SignIndeterminacyStatement(
    value=eta(3),
    representative=nu(4),
  )

  second = SignIndeterminacyStatement(
    value=nu(4),
    representative=nu(4),
  )

  assert first != second


def test_sign_indeterminacy_statement_distinguishes_representative():
  first = SignIndeterminacyStatement(
    value=eta(3),
    representative=nu(4),
  )

  second = SignIndeterminacyStatement(
    value=eta(3),
    representative=eta(3),
  )

  assert first != second


def test_coefficient_indeterminacy_statement():
  k = ScalarSymbol(
    name="k",
  )

  x = eta(3)
  beta = nu(4)
  gamma = sigma(8)

  expression = Sum(
    left=Multiple(
      coefficient=k,
      expression=beta,
    ),
    right=gamma,
  )

  constraint = OddScalarStatement(
    scalar=k,
  )

  statement = CoefficientIndeterminacyStatement(
    value=x,
    expression=expression,
    constraint=constraint,
  )

  assert statement.value == x
  assert statement.expression == expression
  assert statement.constraint == constraint


def test_coefficient_indeterminacy_statement_has_structural_equality():
  k = ScalarSymbol(
    name="k",
  )

  first = CoefficientIndeterminacyStatement(
    value=eta(3),
    expression=Sum(
      left=Multiple(
        coefficient=k,
        expression=nu(4),
      ),
      right=sigma(8),
    ),
    constraint=OddScalarStatement(
      scalar=k,
    ),
  )

  second = CoefficientIndeterminacyStatement(
    value=eta(3),
    expression=Sum(
      left=Multiple(
        coefficient=ScalarSymbol(
          name="k",
        ),
        expression=nu(4),
      ),
      right=sigma(8),
    ),
    constraint=OddScalarStatement(
      scalar=ScalarSymbol(
        name="k",
      ),
    ),
  )

  assert first == second


def test_coefficient_indeterminacy_statement_distinguishes_value():
  k = ScalarSymbol(
    name="k",
  )

  expression = Sum(
    left=Multiple(
      coefficient=k,
      expression=nu(4),
    ),
    right=sigma(8),
  )

  constraint = OddScalarStatement(
    scalar=k,
  )

  first = CoefficientIndeterminacyStatement(
    value=eta(3),
    expression=expression,
    constraint=constraint,
  )

  second = CoefficientIndeterminacyStatement(
    value=nu(4),
    expression=expression,
    constraint=constraint,
  )

  assert first != second


def test_coefficient_indeterminacy_statement_distinguishes_expression():
  k = ScalarSymbol(
    name="k",
  )

  constraint = OddScalarStatement(
    scalar=k,
  )

  first = CoefficientIndeterminacyStatement(
    value=eta(3),
    expression=Sum(
      left=Multiple(
        coefficient=k,
        expression=nu(4),
      ),
      right=sigma(8),
    ),
    constraint=constraint,
  )

  second = CoefficientIndeterminacyStatement(
    value=eta(3),
    expression=Sum(
      left=Multiple(
        coefficient=k,
        expression=sigma(8),
      ),
      right=nu(4),
    ),
    constraint=constraint,
  )

  assert first != second


def test_coefficient_indeterminacy_statement_distinguishes_scalar_constraint():
  first_scalar = ScalarSymbol(
    name="k",
  )

  second_scalar = ScalarSymbol(
    name="l",
  )

  first = CoefficientIndeterminacyStatement(
    value=eta(3),
    expression=Sum(
      left=Multiple(
        coefficient=first_scalar,
        expression=nu(4),
      ),
      right=sigma(8),
    ),
    constraint=OddScalarStatement(
      scalar=first_scalar,
    ),
  )

  second = CoefficientIndeterminacyStatement(
    value=eta(3),
    expression=Sum(
      left=Multiple(
        coefficient=first_scalar,
        expression=nu(4),
      ),
      right=sigma(8),
    ),
    constraint=OddScalarStatement(
      scalar=second_scalar,
    ),
  )

  assert first != second


def test_modulo_implies_coset_membership():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)
  beta = nu(4)

  modulo_step = ProofStep(
    conclusion=ModuloStatement(
      left=alpha,
      right=beta,
      modulus=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    modulo_implies_coset_membership_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      modulo_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    CosetMembershipStatement(
      element=alpha,
      coset=Coset(
        representative=beta,
        subgroup=subgroup,
      ),
    )
  )


def test_modulo_implies_coset_membership_preserves_representative_direction():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)
  beta = nu(4)

  modulo_step = ProofStep(
    conclusion=ModuloStatement(
      left=alpha,
      right=beta,
      modulus=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    modulo_implies_coset_membership_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      modulo_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion != (
    CosetMembershipStatement(
      element=beta,
      coset=Coset(
        representative=alpha,
        subgroup=subgroup,
      ),
    )
  )


def test_modulo_implies_coset_membership_preserves_provenance():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)
  beta = nu(4)

  modulo_step = ProofStep(
    conclusion=ModuloStatement(
      left=alpha,
      right=beta,
      modulus=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    modulo_implies_coset_membership_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      modulo_step,
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
    modulo_step,
  )


def test_modulo_to_coset_membership_rule_rejects_plain_membership():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=eta(3),
      subgroup=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    modulo_implies_coset_membership_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
    ),
  )

  assert match is None


def test_equality_implies_sign_indeterminacy():
  alpha = eta(3)
  beta = nu(4)

  equality_step = ProofStep(
    conclusion=Relation(
      lhs=alpha,
      rhs=beta,
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    equality_implies_sign_indeterminacy_inference_rule()
  )

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

  assert derived_step.conclusion == (
    SignIndeterminacyStatement(
      value=alpha,
      representative=beta,
    )
  )


def test_equality_to_sign_indeterminacy_rejects_non_equality_relation():
  alpha = eta(3)

  zero_step = ProofStep(
    conclusion=Relation(
      lhs=alpha,
      rhs=0,
      relation_type=RelationType.ORDER,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    equality_implies_sign_indeterminacy_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      zero_step,
    ),
  )

  assert match is None


def test_equality_implies_sign_indeterminacy_preserves_provenance():
  alpha = eta(3)
  beta = nu(4)

  equality_step = ProofStep(
    conclusion=Relation(
      lhs=alpha,
      rhs=beta,
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    equality_implies_sign_indeterminacy_inference_rule()
  )

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

  assert derived_step.rule == ProofRule.INFERENCE

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    equality_step,
  )


def test_coset_membership_implies_modulo():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)
  beta = nu(4)

  membership_step = ProofStep(
    conclusion=CosetMembershipStatement(
      element=alpha,
      coset=Coset(
        representative=beta,
        subgroup=subgroup,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    coset_membership_implies_modulo_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    ModuloStatement(
      left=alpha,
      right=beta,
      modulus=subgroup,
    )
  )


def test_coset_membership_implies_modulo_preserves_coset_structure():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)
  beta = nu(4)

  membership_step = ProofStep(
    conclusion=CosetMembershipStatement(
      element=alpha,
      coset=Coset(
        representative=beta,
        subgroup=subgroup,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    coset_membership_implies_modulo_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion.left == alpha
  assert derived_step.conclusion.right == beta
  assert derived_step.conclusion.modulus == subgroup


def test_coset_membership_does_not_imply_equality():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)
  beta = nu(4)

  membership_step = ProofStep(
    conclusion=CosetMembershipStatement(
      element=alpha,
      coset=Coset(
        representative=beta,
        subgroup=subgroup,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    coset_membership_implies_modulo_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion != Relation(
    lhs=alpha,
    rhs=beta,
    relation_type=RelationType.EQUALITY,
  )


def test_modulo_coset_membership_bridge_reaches_fixed_point():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)
  beta = nu(4)

  modulo_step = ProofStep(
    conclusion=ModuloStatement(
      left=alpha,
      right=beta,
      modulus=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  modulo_to_membership_rule = (
    modulo_implies_coset_membership_inference_rule()
  )

  membership_to_modulo_rule = (
    coset_membership_implies_modulo_inference_rule()
  )

  rules = (
    modulo_to_membership_rule,
    membership_to_modulo_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        modulo_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert ModuloStatement(
    left=alpha,
    right=beta,
    modulus=subgroup,
  ) in conclusions

  assert CosetMembershipStatement(
    element=alpha,
    coset=Coset(
      representative=beta,
      subgroup=subgroup,
    ),
  ) in conclusions

  terminal_round = derive_inference_round_result(
    rules,
    result.steps,
  )

  assert terminal_round.new_steps == ()





