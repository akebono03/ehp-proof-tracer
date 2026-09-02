import expression as expression_module
from expression import (
  Composition,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  ScalarSymbol,
  SmashProduct,
  Sum,
)


def test_phase33_1_single_symbol_iterated_suspensions_are_representable():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  assert IteratedSuspension(
    expression=a,
    exponent=q,
  ) == IteratedSuspension(
    expression=a,
    exponent=ScalarSymbol(
      name="q",
    ),
  )

  assert IteratedSuspension(
    expression=b,
    exponent=p,
  ) == IteratedSuspension(
    expression=b,
    exponent=ScalarSymbol(
      name="p",
    ),
  )


def test_phase33_1_existing_expression_nodes_compose_without_new_production_code():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  q = ScalarSymbol(
    name="q",
  )

  left = Composition(
    left=IteratedSuspension(
      expression=a,
      exponent=q,
    ),
    right=b,
  )

  right = Sum(
    left=Multiple(
      coefficient=2,
      expression=a,
    ),
    right=SmashProduct(
      left=a,
      right=b,
    ),
  )

  assert left.left == IteratedSuspension(
    expression=a,
    exponent=q,
  )

  assert left.right == b

  assert right.left == Multiple(
    coefficient=2,
    expression=a,
  )

  assert right.right == SmashProduct(
    left=a,
    right=b,
  )


def test_phase33_1_symbolic_exponent_sum_has_no_structural_representation_yet():
  assert not hasattr(
    expression_module,
    "ScalarSum",
  )

  opaque_exponent = ScalarSymbol(
    name="p+k",
  )

  assert opaque_exponent.name == "p+k"
  assert not hasattr(
    opaque_exponent,
    "left",
  )
  assert not hasattr(
    opaque_exponent,
    "right",
  )


def test_phase33_1_symbolic_exponent_product_has_no_structural_representation_yet():
  assert not hasattr(
    expression_module,
    "ScalarProduct",
  )

  opaque_exponent = ScalarSymbol(
    name="ph",
  )

  assert opaque_exponent.name == "ph"
  assert not hasattr(
    opaque_exponent,
    "left",
  )
  assert not hasattr(
    opaque_exponent,
    "right",
  )


def test_phase33_1_symbolic_power_has_no_structural_representation_yet():
  assert not hasattr(
    expression_module,
    "ScalarPower",
  )

  opaque_sign = ScalarSymbol(
    name="(-1)^n",
  )

  assert opaque_sign.name == "(-1)^n"
  assert not hasattr(
    opaque_sign,
    "base",
  )
  assert not hasattr(
    opaque_sign,
    "exponent",
  )


def test_phase33_1_barratt_hilton_gap_is_scalar_structure_not_main_expression_structure():
  missing_scalar_nodes = tuple(
    name
    for name in (
      "ScalarSum",
      "ScalarProduct",
      "ScalarPower",
    )
    if not hasattr(
      expression_module,
      name,
    )
  )

  assert missing_scalar_nodes == (
    "ScalarSum",
    "ScalarProduct",
    "ScalarPower",
  )

  for name in (
    "IteratedSuspension",
    "Composition",
    "Multiple",
    "Sum",
    "SmashProduct",
  ):
    assert hasattr(
      expression_module,
      name,
    )




