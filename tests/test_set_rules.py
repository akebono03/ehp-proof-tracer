from algebra import (
  GroupElement,
  Subgroup,
  generated_subgroup_elements,
)
from expression import (
  eta,
  nu,
)
from models import (
  AbelianGroup,
  GroupComponent,
)
from set_rules import (
  MembershipStatement,
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


def test_membership_statement():
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

  statement = MembershipStatement(
    element=alpha,
    subgroup=subgroup,
  )

  assert statement.element == alpha
  assert statement.subgroup == subgroup


def test_membership_statement_has_structural_equality():
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

  first = MembershipStatement(
    element=alpha,
    subgroup=subgroup,
  )

  second = MembershipStatement(
    element=alpha,
    subgroup=subgroup,
  )

  assert first == second


def test_membership_statement_distinguishes_element():
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

  alpha_statement = MembershipStatement(
    element=alpha,
    subgroup=subgroup,
  )

  beta_statement = MembershipStatement(
    element=beta,
    subgroup=subgroup,
  )

  assert alpha_statement != beta_statement


def test_membership_statement_distinguishes_subgroup():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup_two = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  whole_group = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  alpha = eta(3)

  subgroup_two_statement = MembershipStatement(
    element=alpha,
    subgroup=subgroup_two,
  )

  whole_group_statement = MembershipStatement(
    element=alpha,
    subgroup=whole_group,
  )

  assert (
    subgroup_two_statement
    != whole_group_statement
  )





