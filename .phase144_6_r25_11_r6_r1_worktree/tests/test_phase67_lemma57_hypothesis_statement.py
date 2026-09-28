from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_rules import (
  TodaLemma57TwoIota5ImageMembershipStatement,
)


def test_phase67_2_statement_stores_e2_alpha():
  i = ScalarSymbol(
    name="i",
  )

  alpha = HomotopyElement(
    name="α",
    dimension=i,
    source=i,
    target=3,
  )

  e2_alpha = IteratedSuspension(
    expression=alpha,
    exponent=2,
  )

  statement = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=e2_alpha,
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=2,
        ),
        sphere_dimension=5,
      ),
    )
  )

  assert statement.element == e2_alpha


def test_phase67_2_statement_stores_pi_i_plus_2_s5_source_group():
  i = ScalarSymbol(
    name="i",
  )

  alpha = HomotopyElement(
    name="α",
    dimension=i,
    source=i,
    target=3,
  )

  statement = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=alpha,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=2,
        ),
        sphere_dimension=5,
      ),
    )
  )

  assert (
    statement.source_group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=2,
      ),
      sphere_dimension=5,
    )
  )


def test_phase67_2_statement_represents_exact_symbolic_hypothesis():
  i = ScalarSymbol(
    name="i",
  )

  alpha = HomotopyElement(
    name="α",
    dimension=i,
    source=i,
    target=3,
  )

  statement = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=alpha,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=2,
        ),
        sphere_dimension=5,
      ),
    )
  )

  assert isinstance(
    statement.element,
    IteratedSuspension,
  )

  assert statement.element.exponent == 2

  assert (
    statement.element.expression
    == alpha
  )

  assert (
    statement.source_group
    .group_dimension
    == ScalarSum(
      left=i,
      right=2,
    )
  )

  assert (
    statement.source_group
    .sphere_dimension
    == 5
  )


def test_phase67_2_statement_has_structural_equality():
  i = ScalarSymbol(
    name="i",
  )

  alpha = HomotopyElement(
    name="α",
    dimension=i,
    source=i,
    target=3,
  )

  first = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=alpha,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=2,
        ),
        sphere_dimension=5,
      ),
    )
  )

  same = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=alpha,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=2,
        ),
        sphere_dimension=5,
      ),
    )
  )

  assert first == same


def test_phase67_2_statement_distinguishes_different_element():
  i = ScalarSymbol(
    name="i",
  )

  alpha = HomotopyElement(
    name="α",
    dimension=i,
    source=i,
    target=3,
  )

  beta = HomotopyElement(
    name="β",
    dimension=i,
    source=i,
    target=3,
  )

  alpha_statement = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=alpha,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=2,
        ),
        sphere_dimension=5,
      ),
    )
  )

  beta_statement = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=beta,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=2,
        ),
        sphere_dimension=5,
      ),
    )
  )

  assert alpha_statement != beta_statement


def test_phase67_2_statement_distinguishes_wrong_source_group_dimension():
  i = ScalarSymbol(
    name="i",
  )

  alpha = HomotopyElement(
    name="α",
    dimension=i,
    source=i,
    target=3,
  )

  correct = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=alpha,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=2,
        ),
        sphere_dimension=5,
      ),
    )
  )

  wrong = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=alpha,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=3,
        ),
        sphere_dimension=5,
      ),
    )
  )

  assert correct != wrong


def test_phase67_2_statement_distinguishes_wrong_sphere_dimension():
  i = ScalarSymbol(
    name="i",
  )

  alpha = HomotopyElement(
    name="α",
    dimension=i,
    source=i,
    target=3,
  )

  correct = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=alpha,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=2,
        ),
        sphere_dimension=5,
      ),
    )
  )

  wrong = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=alpha,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=2,
        ),
        sphere_dimension=4,
      ),
    )
  )

  assert correct != wrong


def test_phase67_2_statement_supports_nu_prime_specialization():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  statement = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=nu_prime,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      ),
    )
  )

  assert (
    statement.element
    == IteratedSuspension(
      expression=nu_prime,
      exponent=2,
    )
  )

  assert (
    statement.source_group
    == TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    )
  )


def test_phase67_2_statement_does_not_add_generic_image_witness_semantics():
  i = ScalarSymbol(
    name="i",
  )

  alpha = HomotopyElement(
    name="α",
    dimension=i,
    source=i,
    target=3,
  )

  statement = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=alpha,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=2,
        ),
        sphere_dimension=5,
      ),
    )
  )

  assert not hasattr(
    statement,
    "witness",
  )

  assert not hasattr(
    statement,
    "map",
  )

  assert not hasattr(
    statement,
    "image",
  )

  assert not hasattr(
    statement,
    "left_factor",
  )


