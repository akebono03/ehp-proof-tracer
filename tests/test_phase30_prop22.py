from expression import (
  Composition,
  HomotopyElement,
  MapApplication,
  Suspension,
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




