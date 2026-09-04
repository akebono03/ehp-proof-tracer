from typing import (
  get_type_hints,
)

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  PrimaryComponent,
  TodaPrimaryGroup,
)
from models import (
  AbelianGroup,
  GroupComponent,
)
from proof import (
  Relation,
  RelationType,
)
from scalar_rules import (
  EvenScalarStatement,
  OddScalarStatement,
)


def build_phase44_1_symbolic_critical_degree():
  n = ScalarSymbol(
    name="n",
  )

  two_n_minus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  return (
    n,
    two_n_minus_one,
  )


def test_phase44_1_current_parity_represents_symbolic_n():
  n = ScalarSymbol(
    name="n",
  )

  odd_statement = OddScalarStatement(
    scalar=n,
  )

  even_statement = EvenScalarStatement(
    scalar=n,
  )

  assert odd_statement.scalar == n
  assert even_statement.scalar == n


def test_phase44_1_symbolic_critical_degree_is_representable():
  n, two_n_minus_one = (
    build_phase44_1_symbolic_critical_degree()
  )

  assert two_n_minus_one == ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )


def test_phase44_1_toda_group_represents_symbolic_critical_degree():
  n, two_n_minus_one = (
    build_phase44_1_symbolic_critical_degree()
  )

  group = TodaPrimaryGroup(
    group_dimension=two_n_minus_one,
    sphere_dimension=n,
  )

  assert group.group_dimension == (
    two_n_minus_one
  )

  assert group.sphere_dimension == n


def test_phase44_1_primary_component_represents_symbolic_critical_degree():
  n, two_n_minus_one = (
    build_phase44_1_symbolic_critical_degree()
  )

  component = PrimaryComponent(
    group_dimension=two_n_minus_one,
    sphere_dimension=n,
    prime=2,
  )

  assert component.group_dimension == (
    two_n_minus_one
  )

  assert component.sphere_dimension == n
  assert component.prime == 2


def test_phase44_1_odd_case_group_conclusion_is_representable_as_relation():
  n, two_n_minus_one = (
    build_phase44_1_symbolic_critical_degree()
  )

  conclusion = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
    ),
    rhs=PrimaryComponent(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
      prime=2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert conclusion.lhs == (
    TodaPrimaryGroup(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
    )
  )

  assert conclusion.rhs == (
    PrimaryComponent(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
      prime=2,
    )
  )

  assert (
    conclusion.relation_type
    == RelationType.EQUALITY
  )


def test_phase44_1_homotopy_element_dimension_remains_concrete_integer():
  type_hints = get_type_hints(
    HomotopyElement
  )

  assert type_hints[
    "dimension"
  ] is int


def test_phase44_1_generator_symbol_index_remains_concrete_integer_or_none():
  type_hints = get_type_hints(
    GeneratorSymbol
  )

  assert type_hints[
    "index"
  ] == (
    int | None
  )


def test_phase44_1_general_symbolic_whitehead_identity_is_not_yet_lossless():
  n = ScalarSymbol(
    name="n",
  )

  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  homotopy_element_hints = (
    get_type_hints(
      HomotopyElement
    )
  )

  generator_symbol_hints = (
    get_type_hints(
      GeneratorSymbol
    )
  )

  assert (
    homotopy_element_hints[
      "dimension"
    ]
    is int
  )

  assert (
    generator_symbol_hints[
      "index"
    ]
    == (
      int | None
    )
  )

  assert not isinstance(
    n_minus_one,
    int,
  )


def test_phase44_1_abelian_group_components_use_string_generator_labels():
  type_hints = get_type_hints(
    GroupComponent
  )

  assert type_hints[
    "generator"
  ] is str


def test_phase44_1_abelian_group_uses_concrete_integer_dimensions():
  type_hints = get_type_hints(
    AbelianGroup
  )

  assert type_hints[
    "n"
  ] is int

  assert type_hints[
    "k"
  ] is int


def test_phase44_1_abelian_group_component_cannot_preserve_primary_component_as_summand():
  n, two_n_minus_one = (
    build_phase44_1_symbolic_critical_degree()
  )

  primary_component = PrimaryComponent(
    group_dimension=two_n_minus_one,
    sphere_dimension=n,
    prime=2,
  )

  component_hints = get_type_hints(
    GroupComponent
  )

  assert component_hints[
    "generator"
  ] is str

  assert not isinstance(
    primary_component,
    str,
  )


def test_phase44_1_current_group_layer_has_no_structural_direct_sum_term():
  group = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  component = PrimaryComponent(
    group_dimension=9,
    sphere_dimension=5,
    prime=2,
  )

  for value in (
    group,
    component,
  ):
    assert not hasattr(
      value,
      "left_summand",
    )

    assert not hasattr(
      value,
      "right_summand",
    )

    assert not hasattr(
      value,
      "summands",
    )


def test_phase44_1_has_no_toda_lemma_4_1_case_semantics_yet():
  n = ScalarSymbol(
    name="n",
  )

  statements = (
    OddScalarStatement(
      scalar=n,
    ),
    EvenScalarStatement(
      scalar=n,
    ),
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=ScalarProduct(
          left=2,
          right=n,
        ),
        right=-1,
      ),
      sphere_dimension=n,
    ),
  )

  for statement in statements:
    assert not hasattr(
      statement,
      "toda_lemma_4_1",
    )

    assert not hasattr(
      statement,
      "case",
    )

    assert not hasattr(
      statement,
      "result_group",
    )



