from expression import (
  Composition,
  Expression,
  HomotopyElement,
  IndexedTodaBracketData,
  IteratedSuspension,
  MapApplication,
  MapSymbol,
  Multiple,
  ScalarSymbol,
  Sum,
  Suspension,
  TodaBracket,
  Zero,
  eta,
  nu,
  sigma,
)


def test_scalar_symbol():
  scalar = ScalarSymbol(
    name="k",
  )

  assert scalar.name == "k"


def test_scalar_symbol_has_structural_equality():
  k = ScalarSymbol(
    name="k",
  )

  same_k = ScalarSymbol(
    name="k",
  )

  ell = ScalarSymbol(
    name="l",
  )

  assert k == same_k
  assert k != ell


def test_scalar_symbol_is_not_expression():
  scalar = ScalarSymbol(
    name="k",
  )

  assert not isinstance(
    scalar,
    Expression,
  )


def test_homotopy_element():
  element = HomotopyElement(
    name="η",
    dimension=3,
  )

  assert element.name == "η"
  assert element.dimension == 3


def test_eta():
  assert eta(3) == HomotopyElement("η", 3)


def test_nu():
  assert nu(4) == HomotopyElement("ν", 4)


def test_sigma():
  assert sigma(8) == HomotopyElement("σ", 8)


def test_zero():
  assert Zero() == Zero()


def test_multiple():
  expression = Multiple(
    2,
    eta(3),
  )

  assert expression.coefficient == 2
  assert expression.expression == eta(3)


def test_multiple_accepts_symbolic_scalar():
  k = ScalarSymbol(
    name="k",
  )

  alpha = eta(3)

  multiple = Multiple(
    coefficient=k,
    expression=alpha,
  )

  assert multiple.coefficient == k
  assert multiple.expression == alpha


def test_symbolic_multiple_has_structural_equality():
  k = ScalarSymbol(
    name="k",
  )

  alpha = eta(3)

  first = Multiple(
    coefficient=k,
    expression=alpha,
  )

  second = Multiple(
    coefficient=ScalarSymbol(
      name="k",
    ),
    expression=alpha,
  )

  assert first == second


def test_symbolic_multiple_distinguishes_scalar_symbol():
  k = ScalarSymbol(
    name="k",
  )

  ell = ScalarSymbol(
    name="l",
  )

  alpha = eta(3)

  k_multiple = Multiple(
    coefficient=k,
    expression=alpha,
  )

  ell_multiple = Multiple(
    coefficient=ell,
    expression=alpha,
  )

  assert k_multiple != ell_multiple


def test_symbolic_multiple_remains_distinct_from_integer_multiple():
  k = ScalarSymbol(
    name="k",
  )

  alpha = eta(3)

  symbolic_multiple = Multiple(
    coefficient=k,
    expression=alpha,
  )

  integer_multiple = Multiple(
    coefficient=2,
    expression=alpha,
  )

  assert symbolic_multiple != integer_multiple


def test_inverse_is_represented_by_negative_one_multiple():
  alpha = eta(3)

  inverse = Multiple(
    -1,
    alpha,
  )

  assert inverse.coefficient == -1
  assert inverse.expression == alpha
  assert inverse == Multiple(
    -1,
    alpha,
  )


def test_multiple_remains_distinct_from_repeated_sum():
  alpha = eta(3)

  multiple = Multiple(
    2,
    alpha,
  )

  repeated_sum = Sum(
    alpha,
    alpha,
  )

  assert multiple != repeated_sum
  assert multiple.coefficient == 2
  assert multiple.expression == alpha


def test_zero_remains_distinct_from_zero_multiple():
  alpha = eta(3)

  zero = Zero()

  zero_multiple = Multiple(
    0,
    alpha,
  )

  assert zero_multiple != zero
  assert zero_multiple.coefficient == 0
  assert zero_multiple.expression == alpha


def test_sum():
  expression = Sum(
    eta(3),
    nu(4),
  )

  assert expression.left == eta(3)
  assert expression.right == nu(4)


def test_sum_with_zero_preserves_right_zero_structure():
  alpha = eta(3)

  expression = Sum(
    alpha,
    Zero(),
  )

  assert expression.left == alpha
  assert expression.right == Zero()
  assert expression != alpha


def test_sum_with_zero_preserves_left_zero_structure():
  alpha = eta(3)

  expression = Sum(
    Zero(),
    alpha,
  )

  assert expression.left == Zero()
  assert expression.right == alpha
  assert expression != alpha


def test_composition():
  expression = Composition(
    eta(3),
    eta(4),
  )

  assert expression.left == eta(3)
  assert expression.right == eta(4)


def test_suspension():
  expression = Suspension(
    eta(3),
  )

  assert expression.expression == eta(3)


def test_nested_suspension():
  expression = Suspension(
    Suspension(
      eta(3),
    )
  )

  assert expression == Suspension(
    Suspension(
      eta(3),
    )
  )

  assert expression.expression == Suspension(
    eta(3),
  )


def test_sum_has_structural_equality():
  expression = Sum(
    eta(3),
    nu(4),
  )

  assert expression == Sum(
    eta(3),
    nu(4),
  )


def test_sum_distinguishes_operand_order():
  left_right = Sum(
    eta(3),
    nu(4),
  )

  right_left = Sum(
    nu(4),
    eta(3),
  )

  assert left_right != right_left


def test_nested_sum_preserves_structure():
  alpha = eta(3)
  beta = nu(4)
  gamma = sigma(8)

  left_nested = Sum(
    Sum(
      alpha,
      beta,
    ),
    gamma,
  )

  right_nested = Sum(
    alpha,
    Sum(
      beta,
      gamma,
    ),
  )

  assert left_nested.left == Sum(
    alpha,
    beta,
  )
  assert left_nested.right == gamma

  assert right_nested.left == alpha
  assert right_nested.right == Sum(
    beta,
    gamma,
  )

  assert left_nested != right_nested


def test_map_symbol():
  map_symbol = MapSymbol(
    name="f",
  )

  assert map_symbol.name == "f"


def test_map_symbol_has_structural_equality():
  first = MapSymbol(
    name="f",
  )

  second = MapSymbol(
    name="f",
  )

  assert first == second


def test_map_symbol_distinguishes_name():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  assert f != g


def test_map_application():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  application = MapApplication(
    map=f,
    expression=alpha,
  )

  assert application.map == f
  assert application.expression == alpha


def test_map_application_has_structural_equality():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  first = MapApplication(
    map=f,
    expression=alpha,
  )

  second = MapApplication(
    map=f,
    expression=alpha,
  )

  assert first == second


def test_map_application_distinguishes_map():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  alpha = eta(3)

  f_alpha = MapApplication(
    map=f,
    expression=alpha,
  )

  g_alpha = MapApplication(
    map=g,
    expression=alpha,
  )

  assert f_alpha != g_alpha


def test_map_application_distinguishes_expression():
  f = MapSymbol(
    name="f",
  )

  f_alpha = MapApplication(
    map=f,
    expression=eta(3),
  )

  f_beta = MapApplication(
    map=f,
    expression=nu(4),
  )

  assert f_alpha != f_beta


def test_map_application_preserves_structured_argument():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)
  beta = nu(4)

  argument = Sum(
    alpha,
    beta,
  )

  application = MapApplication(
    map=f,
    expression=argument,
  )

  assert application.expression == Sum(
    alpha,
    beta,
  )

  assert application != Sum(
    MapApplication(
      map=f,
      expression=alpha,
    ),
    MapApplication(
      map=f,
      expression=beta,
    ),
  )


def test_toda_bracket():
  a = eta(3)
  b = nu(4)
  c = sigma(8)

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  assert bracket.first == a
  assert bracket.second == b
  assert bracket.third == c


def test_toda_bracket_is_not_expression():
  bracket = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
  )

  assert not isinstance(
    bracket,
    Expression,
  )


def test_toda_bracket_structural_equality():
  a = eta(3)
  b = nu(4)
  c = sigma(8)

  left = TodaBracket(
    first=a,
    second=b,
    third=c,
  )
  right = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  assert left == right


def test_toda_bracket_entry_order_is_structural():
  a = eta(3)
  b = nu(4)
  c = sigma(8)

  original = TodaBracket(
    first=a,
    second=b,
    third=c,
  )
  reordered = TodaBracket(
    first=a,
    second=c,
    third=b,
  )

  assert original != reordered


def test_indexed_toda_bracket():
  bracket = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
    index=1,
  )

  assert bracket.first == eta(3)
  assert bracket.second == nu(4)
  assert bracket.third == sigma(8)
  assert bracket.index == 1


def test_unindexed_toda_bracket_has_no_index():
  bracket = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
  )

  assert bracket.index is None


def test_unindexed_and_indexed_toda_brackets_are_structurally_distinct():
  unindexed = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
  )
  indexed = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
    index=1,
  )

  assert unindexed != indexed


def test_toda_brackets_with_different_indices_are_structurally_distinct():
  index_one = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
    index=1,
  )
  index_two = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
    index=2,
  )

  assert index_one != index_two


def test_toda_brackets_with_same_entries_and_same_index_are_structurally_equal():
  left = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
    index=1,
  )
  right = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
    index=1,
  )

  assert left == right


def test_indexed_toda_bracket_data_preserves_underlying_entries():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
    index=1,
  )

  data = IndexedTodaBracketData(
    bracket=bracket,
    second_base=nu_prime,
    third_base=nu(6),
    suspension_exponent=1,
  )

  assert data.bracket == bracket
  assert data.second_base == nu_prime
  assert data.third_base == nu(6)
  assert data.suspension_exponent == 1

  assert data.bracket.first == eta(3)

  assert data.bracket.second == Suspension(
    nu_prime,
  )

  assert data.bracket.third == nu(7)

  assert data.bracket.index == 1


def test_indexed_toda_bracket_data_keeps_suspension_exponent_separate_from_index():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
    index=1,
  )

  data = IndexedTodaBracketData(
    bracket=bracket,
    second_base=nu_prime,
    third_base=nu(6),
    suspension_exponent=2,
  )

  assert data.bracket.index == 1
  assert data.suspension_exponent == 2
  assert data.bracket.index != data.suspension_exponent


def test_indexed_toda_bracket_data_distinguishes_underlying_entries():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  other_nu_prime = HomotopyElement(
    name="ν″",
    dimension=3,
  )

  bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
    index=1,
  )

  first = IndexedTodaBracketData(
    bracket=bracket,
    second_base=nu_prime,
    third_base=nu(6),
    suspension_exponent=1,
  )

  second = IndexedTodaBracketData(
    bracket=bracket,
    second_base=other_nu_prime,
    third_base=nu(6),
    suspension_exponent=1,
  )

  assert first != second


def test_iterated_suspension_preserves_concrete_exponent():
  expression = eta(3)

  suspended = IteratedSuspension(
    expression=expression,
    exponent=2,
  )

  assert suspended.expression == expression
  assert suspended.exponent == 2
  assert isinstance(
    suspended,
    Expression,
  )


def test_iterated_suspension_preserves_symbolic_exponent():
  expression = eta(3)

  t = ScalarSymbol(
    name="t",
  )

  suspended = IteratedSuspension(
    expression=expression,
    exponent=t,
  )

  assert suspended.expression == expression
  assert suspended.exponent == t


def test_iterated_suspension_one_is_structurally_distinct_from_suspension():
  expression = eta(3)

  iterated = IteratedSuspension(
    expression=expression,
    exponent=1,
  )

  ordinary = Suspension(
    expression,
  )

  assert iterated != ordinary


def test_iterated_suspension_two_is_structurally_distinct_from_nested_suspension():
  expression = eta(3)

  iterated = IteratedSuspension(
    expression=expression,
    exponent=2,
  )

  nested = Suspension(
    Suspension(
      expression,
    ),
  )

  assert iterated != nested


def test_iterated_suspension_distinguishes_exponent():
  expression = eta(3)

  first = IteratedSuspension(
    expression=expression,
    exponent=1,
  )

  second = IteratedSuspension(
    expression=expression,
    exponent=2,
  )

  assert first != second


def test_iterated_suspension_distinguishes_symbolic_exponent():
  expression = eta(3)

  t = ScalarSymbol(
    name="t",
  )

  s = ScalarSymbol(
    name="s",
  )

  first = IteratedSuspension(
    expression=expression,
    exponent=t,
  )

  second = IteratedSuspension(
    expression=expression,
    exponent=s,
  )

  assert first != second


def test_indexed_toda_bracket_data_accepts_symbolic_suspension_exponent():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  t = ScalarSymbol(
    name="t",
  )

  bracket = TodaBracket(
    first=eta(3),
    second=IteratedSuspension(
      expression=nu_prime,
      exponent=t,
    ),
    third=IteratedSuspension(
      expression=nu(6),
      exponent=t,
    ),
    index=1,
  )

  data = IndexedTodaBracketData(
    bracket=bracket,
    second_base=nu_prime,
    third_base=nu(6),
    suspension_exponent=t,
  )

  assert data.suspension_exponent == t

  assert data.bracket.second == IteratedSuspension(
    expression=data.second_base,
    exponent=data.suspension_exponent,
  )

  assert data.bracket.third == IteratedSuspension(
    expression=data.third_base,
    exponent=data.suspension_exponent,
  )


def test_indexed_toda_bracket_data_distinguishes_symbolic_suspension_exponent():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  bracket = TodaBracket(
    first=eta(3),
    second=IteratedSuspension(
      expression=nu_prime,
      exponent=ScalarSymbol(
        name="t",
      ),
    ),
    third=IteratedSuspension(
      expression=nu(6),
      exponent=ScalarSymbol(
        name="t",
      ),
    ),
    index=1,
  )

  first = IndexedTodaBracketData(
    bracket=bracket,
    second_base=nu_prime,
    third_base=nu(6),
    suspension_exponent=ScalarSymbol(
      name="t",
    ),
  )

  second = IndexedTodaBracketData(
    bracket=bracket,
    second_base=nu_prime,
    third_base=nu(6),
    suspension_exponent=ScalarSymbol(
      name="s",
    ),
  )

  assert first != second


def test_toda_bracket_accepts_symbolic_index():
  t = ScalarSymbol(
    name="t",
  )

  bracket = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
    index=t,
  )

  assert bracket.index == t


def test_toda_brackets_with_same_symbolic_index_are_structurally_equal():
  left = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
    index=ScalarSymbol(
      name="t",
    ),
  )

  right = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
    index=ScalarSymbol(
      name="t",
    ),
  )

  assert left == right


def test_toda_brackets_with_different_symbolic_indices_are_structurally_distinct():
  t_indexed = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
    index=ScalarSymbol(
      name="t",
    ),
  )

  s_indexed = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
    index=ScalarSymbol(
      name="s",
    ),
  )

  assert t_indexed != s_indexed


def test_indexed_toda_bracket_data_represents_symbolic_indexed_suspension_form():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  t = ScalarSymbol(
    name="t",
  )

  bracket = TodaBracket(
    first=eta(3),
    second=IteratedSuspension(
      expression=nu_prime,
      exponent=t,
    ),
    third=IteratedSuspension(
      expression=nu(6),
      exponent=t,
    ),
    index=t,
  )

  data = IndexedTodaBracketData(
    bracket=bracket,
    second_base=nu_prime,
    third_base=nu(6),
    suspension_exponent=t,
  )

  assert data.bracket.first == eta(3)

  assert data.bracket.second == IteratedSuspension(
    expression=data.second_base,
    exponent=t,
  )

  assert data.bracket.third == IteratedSuspension(
    expression=data.third_base,
    exponent=t,
  )

  assert data.bracket.index == t
  assert data.suspension_exponent == t
  assert data.bracket.index == data.suspension_exponent







