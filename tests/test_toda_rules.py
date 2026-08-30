from algebra import (
  GroupElement,
  Subgroup,
  generated_subgroup_elements,
)
from expression import (
  Composition,
  TodaBracket,
  Zero,
  eta,
  nu,
  sigma,
)
from indeterminacy_rules import (
  CosetMembershipStatement,
  SignIndeterminacyStatement,
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
  find_inference_match,
  relation_proof_step,
  run_inference_until_stable_with_history,
)
from relation_rules import (
  composition_equality_to_zero_inference_rule,
)
from set_rules import (
  Coset,
)
from toda_rules import (
  TodaBracketDefinedStatement,
  TodaBracketMembershipStatement,
  toda_bracket_defined_by_zero_compositions_inference_rule,
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


def test_toda_bracket_membership_statement():
  x = eta(3)

  bracket = TodaBracket(
    first=nu(4),
    second=sigma(8),
    third=eta(9),
  )

  statement = TodaBracketMembershipStatement(
    element=x,
    bracket=bracket,
  )

  assert statement.element == x
  assert statement.bracket == bracket


def test_toda_bracket_membership_statement_has_structural_equality():
  bracket = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
  )

  first = TodaBracketMembershipStatement(
    element=eta(9),
    bracket=bracket,
  )

  second = TodaBracketMembershipStatement(
    element=eta(9),
    bracket=bracket,
  )

  assert first == second


def test_toda_bracket_membership_statement_distinguishes_element():
  bracket = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
  )

  first = TodaBracketMembershipStatement(
    element=eta(9),
    bracket=bracket,
  )

  second = TodaBracketMembershipStatement(
    element=nu(9),
    bracket=bracket,
  )

  assert first != second


def test_toda_bracket_membership_statement_distinguishes_bracket():
  element = eta(9)

  first = TodaBracketMembershipStatement(
    element=element,
    bracket=TodaBracket(
      first=eta(3),
      second=nu(4),
      third=sigma(8),
    ),
  )

  second = TodaBracketMembershipStatement(
    element=element,
    bracket=TodaBracket(
      first=eta(3),
      second=sigma(8),
      third=nu(4),
    ),
  )

  assert first != second


def test_toda_bracket_membership_coexists_with_sign_indeterminacy():
  x = eta(9)
  alpha = nu(9)

  bracket_membership = TodaBracketMembershipStatement(
    element=x,
    bracket=TodaBracket(
      first=eta(3),
      second=nu(4),
      third=sigma(8),
    ),
  )

  sign_indeterminacy = SignIndeterminacyStatement(
    value=x,
    representative=alpha,
  )

  knowledge = (
    bracket_membership,
    sign_indeterminacy,
  )

  assert bracket_membership in knowledge
  assert sign_indeterminacy in knowledge
  assert bracket_membership.element == sign_indeterminacy.value


def test_toda_bracket_membership_coexists_with_coset_indeterminacy():
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

  x = eta(9)
  beta = nu(9)

  bracket_membership = TodaBracketMembershipStatement(
    element=x,
    bracket=TodaBracket(
      first=eta(3),
      second=nu(4),
      third=sigma(8),
    ),
  )

  coset_membership = CosetMembershipStatement(
    element=x,
    coset=Coset(
      representative=beta,
      subgroup=subgroup,
    ),
  )

  knowledge = (
    bracket_membership,
    coset_membership,
  )

  assert bracket_membership in knowledge
  assert coset_membership in knowledge
  assert bracket_membership.element == coset_membership.element


def test_toda_bracket_membership_does_not_collapse_sign_indeterminacy():
  x = eta(9)
  alpha = nu(9)

  bracket_membership = TodaBracketMembershipStatement(
    element=x,
    bracket=TodaBracket(
      first=eta(3),
      second=nu(4),
      third=sigma(8),
    ),
  )

  sign_indeterminacy = SignIndeterminacyStatement(
    value=x,
    representative=alpha,
  )

  assert bracket_membership != sign_indeterminacy
  assert bracket_membership.element == sign_indeterminacy.value


def test_toda_bracket_membership_does_not_collapse_coset_indeterminacy():
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

  x = eta(9)

  bracket_membership = TodaBracketMembershipStatement(
    element=x,
    bracket=TodaBracket(
      first=eta(3),
      second=nu(4),
      third=sigma(8),
    ),
  )

  coset_membership = CosetMembershipStatement(
    element=x,
    coset=Coset(
      representative=nu(9),
      subgroup=subgroup,
    ),
  )

  assert bracket_membership != coset_membership
  assert bracket_membership.element == coset_membership.element


def test_toda_bracket_defined_statement():
  bracket = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
  )

  statement = TodaBracketDefinedStatement(
    bracket=bracket,
  )

  assert statement.bracket == bracket


def test_toda_bracket_defined_by_zero_compositions():
  a = eta(3)
  b = nu(4)
  c = sigma(8)

  first_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  second_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_zero_step,
      second_zero_step,
    ),
  )

  assert match is not None

  result = run_inference_until_stable_with_history(
    rule,
    (
      first_zero_step,
      second_zero_step,
    ),
  )

  expected = TodaBracketDefinedStatement(
    bracket=TodaBracket(
      first=a,
      second=b,
      third=c,
    ),
  )

  assert expected in tuple(
    step.conclusion
    for step in result.steps
  )

  derived_step = next(
    step
    for step in result.steps
    if step.conclusion == expected
  )

  assert derived_step.rule == ProofRule.INFERENCE
  assert derived_step.inference_rule == rule
  assert derived_step.premises == (
    first_zero_step,
    second_zero_step,
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_toda_bracket_defined_rule_rejects_mismatched_middle_entry():
  a = eta(3)
  b = nu(4)
  different_b = nu(5)
  c = sigma(8)

  first_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  second_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=different_b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_zero_step,
      second_zero_step,
    ),
  )

  assert match is None


def test_toda_bracket_defined_rule_requires_both_zero_compositions():
  a = eta(3)
  b = nu(4)

  first_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_zero_step,
    ),
  )

  assert match is None


def test_toda_bracket_defined_from_known_zero_composition_equalities():
  a = eta(3)
  b = nu(4)
  c = sigma(8)

  first_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note="known zero composition",
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note="known zero composition",
    )
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      zero_rule,
      defined_rule,
    ),
    (
      first_equality_step,
      second_equality_step,
    ),
  )

  first_zero = Relation(
    lhs=Composition(
      left=a,
      right=b,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  second_zero = Relation(
    lhs=Composition(
      left=b,
      right=c,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  defined = TodaBracketDefinedStatement(
    bracket=TodaBracket(
      first=a,
      second=b,
      third=c,
    ),
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert first_zero in conclusions
  assert second_zero in conclusions
  assert defined in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2




