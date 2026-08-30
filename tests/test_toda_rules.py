from algebra import (
  GroupElement,
  Subgroup,
  generated_subgroup_elements,
)
from expression import (
  TodaBracket,
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
from set_rules import (
  Coset,
)
from toda_rules import (
  TodaBracketMembershipStatement,
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




