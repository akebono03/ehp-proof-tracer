from expression import (
  Composition,
  HomotopyElement,
  MapApplication,
  SmashProduct,
  Suspension,
)
from map_facts import (
  HOPF_MAP,
)
from proof import (
  Relation,
  RelationType,
)


def test_phase32_1_left_hopf_formula_is_structurally_representable():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  suspended_c = Suspension(
    expression=c,
  )

  suspended_c_smash_c = Suspension(
    expression=SmashProduct(
      left=c,
      right=c,
    ),
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=suspended_c,
        right=a,
      ),
    ),
    rhs=Composition(
      left=suspended_c_smash_c,
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert statement.lhs == MapApplication(
    map=HOPF_MAP,
    expression=Composition(
      left=Suspension(
        expression=c,
      ),
      right=a,
    ),
  )

  assert statement.rhs == Composition(
    left=Suspension(
      expression=SmashProduct(
        left=c,
        right=c,
      ),
    ),
    right=MapApplication(
      map=HOPF_MAP,
      expression=a,
    ),
  )

  assert statement.relation_type == (
    RelationType.EQUALITY
  )


def test_phase32_1_left_hopf_formula_preserves_suspended_left_factor():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert isinstance(
    statement.lhs.expression,
    Composition,
  )

  assert isinstance(
    statement.lhs.expression.left,
    Suspension,
  )

  assert (
    statement
    .lhs
    .expression
    .left
    .expression
    == c
  )

  assert statement.lhs.expression.right == a


def test_phase32_1_left_hopf_formula_preserves_suspended_smash_product():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert isinstance(
    statement.rhs,
    Composition,
  )

  assert isinstance(
    statement.rhs.left,
    Suspension,
  )

  assert isinstance(
    statement.rhs.left.expression,
    SmashProduct,
  )

  assert (
    statement
    .rhs
    .left
    .expression
    .left
    == c
  )

  assert (
    statement
    .rhs
    .left
    .expression
    .right
    == c
  )

  assert isinstance(
    statement.rhs.right,
    MapApplication,
  )

  assert statement.rhs.right.map is HOPF_MAP
  assert statement.rhs.right.expression == a


def test_phase32_1_left_hopf_formula_preserves_actual_hopf_map_identity():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert statement.lhs.map is HOPF_MAP
  assert statement.rhs.right.map is HOPF_MAP


def test_phase32_1_left_hopf_formula_distinguishes_unsuspended_left_factor():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  formula = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  different = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=c,
        right=a,
      ),
    ),
    rhs=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert formula != different


def test_phase32_1_left_hopf_formula_distinguishes_unsuspended_smash_product():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  formula = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  different = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=SmashProduct(
        left=c,
        right=c,
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert formula != different





