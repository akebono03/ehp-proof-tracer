from expression import (
  Composition,
  HomotopyElement,
  MapApplication,
  Suspension,
)
from hopf_rules import (
  HopfInvariantStatement,
)
from map_facts import HOPF_MAP
from proof import (
  Relation,
  RelationType,
)


def test_phase30_1_right_hopf_formula_is_structurally_representable():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=a,
        right=Suspension(
          expression=b,
        ),
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      right=Suspension(
        expression=b,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert statement.lhs == MapApplication(
    map=HOPF_MAP,
    expression=Composition(
      left=a,
      right=Suspension(
        expression=b,
      ),
    ),
  )

  assert statement.rhs == Composition(
    left=MapApplication(
      map=HOPF_MAP,
      expression=a,
    ),
    right=Suspension(
      expression=b,
    ),
  )

  assert statement.relation_type == (
    RelationType.EQUALITY
  )


def test_phase30_1_right_hopf_formula_preserves_suspension_structure():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=a,
        right=Suspension(
          expression=b,
        ),
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      right=Suspension(
        expression=b,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert isinstance(
    statement.lhs.expression,
    Composition,
  )

  assert isinstance(
    statement.lhs.expression.right,
    Suspension,
  )

  assert statement.lhs.expression.right.expression == b

  assert isinstance(
    statement.rhs,
    Composition,
  )

  assert isinstance(
    statement.rhs.right,
    Suspension,
  )

  assert statement.rhs.right.expression == b


def test_phase30_1_right_hopf_formula_preserves_actual_hopf_map_identity():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=a,
        right=Suspension(
          expression=b,
        ),
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      right=Suspension(
        expression=b,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert statement.lhs.map is HOPF_MAP
  assert statement.rhs.left.map is HOPF_MAP


def test_phase30_1_right_hopf_formula_distinguishes_unsuspended_right_factor():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  formula = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=a,
        right=Suspension(
          expression=b,
        ),
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      right=Suspension(
        expression=b,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  different = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=a,
        right=b,
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      right=b,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert formula != different


def test_phase30_2_phase11_hopf_statement_is_distinct_from_map_application_relation():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  value = HomotopyElement(
    name="value",
    dimension=1,
  )

  phase11_statement = HopfInvariantStatement(
    expression=a,
    value=value,
  )

  map_application_relation = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=a,
    ),
    rhs=value,
    relation_type=RelationType.EQUALITY,
  )

  assert phase11_statement != (
    map_application_relation
  )


def test_phase30_2_phase11_hopf_statement_preserves_expression_and_value_without_map_symbol():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  value = HomotopyElement(
    name="value",
    dimension=1,
  )

  statement = HopfInvariantStatement(
    expression=a,
    value=value,
  )

  assert statement.expression == a
  assert statement.value == value

  assert not hasattr(
    statement,
    "map",
  )


def test_phase30_2_map_application_representation_preserves_actual_hopf_map():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  application = MapApplication(
    map=HOPF_MAP,
    expression=a,
  )

  assert application.map is HOPF_MAP
  assert application.expression == a


def test_phase30_2_phase11_right_formula_and_map_application_formula_have_matching_mathematical_parts():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  h_a = HomotopyElement(
    name="H(a)",
    dimension=1,
  )

  suspended_b = Suspension(
    expression=b,
  )

  phase11_formula = HopfInvariantStatement(
    expression=Composition(
      left=a,
      right=suspended_b,
    ),
    value=Composition(
      left=h_a,
      right=suspended_b,
    ),
  )

  map_application_formula = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=a,
        right=suspended_b,
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      right=suspended_b,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    phase11_formula.expression
    == map_application_formula.lhs.expression
  )

  assert (
    phase11_formula.value.right
    == map_application_formula.rhs.right
  )

  assert isinstance(
    phase11_formula.value,
    Composition,
  )

  assert isinstance(
    map_application_formula.rhs,
    Composition,
  )

  assert isinstance(
    map_application_formula.rhs.left,
    MapApplication,
  )


def test_phase30_2_no_implicit_bridge_exists_between_phase11_and_actual_hopf_map_representation():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  value = HomotopyElement(
    name="value",
    dimension=1,
  )

  phase11_statement = HopfInvariantStatement(
    expression=a,
    value=value,
  )

  assert phase11_statement != Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=a,
    ),
    rhs=value,
    relation_type=RelationType.EQUALITY,
  )





