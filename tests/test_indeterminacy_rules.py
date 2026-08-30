from algebra import (
  GroupElement,
  Subgroup,
  generated_subgroup_elements,
)
from expression import (
  eta,
  nu,
)
from indeterminacy_rules import (
  CosetMembershipStatement,
)
from models import (
  AbelianGroup,
  GroupComponent,
)
from set_rules import (
  Coset,
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



