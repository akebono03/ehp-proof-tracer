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
)
from models import (
  AbelianGroup,
  GroupComponent,
)
from set_rules import (
  Coset,
)
from scalar_rules import (
  OddScalarStatement,
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



