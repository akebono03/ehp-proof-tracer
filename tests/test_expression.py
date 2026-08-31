from expression import (
  Composition,
  Expression,
  GeneratorSymbol,
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


def test_phase22_1_generator_symbol_preserves_minimum_structure():
  symbol = GeneratorSymbol(
    family="ν",
    index=3,
    decoration="′",
  )

  assert symbol.family == "ν"
  assert symbol.index == 3
  assert symbol.decoration == "′"


def test_phase22_1_generator_symbol_is_not_expression():
  symbol = GeneratorSymbol(
    family="ν",
  )

  assert not isinstance(
    symbol,
    Expression,
  )


def test_phase22_2_generator_symbol_same_family_and_index_are_equal():
  left = GeneratorSymbol(
    family="η",
    index=3,
  )
  right = GeneratorSymbol(
    family="η",
    index=3,
  )

  assert left == right


def test_phase22_2_generator_symbol_different_family_is_not_equal():
  eta_3 = GeneratorSymbol(
    family="η",
    index=3,
  )
  mu_3 = GeneratorSymbol(
    family="μ",
    index=3,
  )

  assert eta_3 != mu_3


def test_phase22_2_generator_symbol_different_index_is_not_equal():
  eta_3 = GeneratorSymbol(
    family="η",
    index=3,
  )
  eta_4 = GeneratorSymbol(
    family="η",
    index=4,
  )

  assert eta_3 != eta_4


def test_phase22_2_generator_symbol_indexed_and_unindexed_are_not_equal():
  eta = GeneratorSymbol(
    family="η",
  )
  eta_3 = GeneratorSymbol(
    family="η",
    index=3,
  )

  assert eta != eta_3


def test_phase22_3_generator_symbol_same_decoration_are_equal():
  left = GeneratorSymbol(
    family="ν",
    decoration="′",
  )
  right = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  assert left == right


def test_phase22_3_generator_symbol_plain_and_decorated_are_not_equal():
  nu_plain = GeneratorSymbol(
    family="ν",
  )
  nu_prime = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  assert nu_plain != nu_prime


def test_phase22_3_generator_symbol_different_decorations_are_not_equal():
  nu_prime = GeneratorSymbol(
    family="ν",
    decoration="′",
  )
  nu_bar = GeneratorSymbol(
    family="ν",
    decoration="bar",
  )

  assert nu_prime != nu_bar


def test_phase22_3_generator_symbol_decoration_is_preserved():
  symbol = GeneratorSymbol(
    family="ν",
    decoration="bar",
  )

  assert symbol.decoration == "bar"


def test_phase22_4_nu_family_representative_distinctions():
  nu_plain = GeneratorSymbol(
    family="ν",
  )
  nu_prime = GeneratorSymbol(
    family="ν",
    decoration="′",
  )
  nu_bar = GeneratorSymbol(
    family="ν",
    decoration="bar",
  )

  assert nu_plain != nu_prime
  assert nu_plain != nu_bar
  assert nu_prime != nu_bar


def test_phase22_4_decoration_and_index_are_independent_roles():
  nu_prime = GeneratorSymbol(
    family="ν",
    decoration="′",
  )
  nu_prime_7 = GeneratorSymbol(
    family="ν",
    index=7,
    decoration="′",
  )

  assert nu_prime != nu_prime_7
  assert nu_prime.decoration == nu_prime_7.decoration
  assert nu_prime.index is None
  assert nu_prime_7.index == 7


def test_phase22_4_same_display_family_does_not_collapse_decoration():
  nu_plain = GeneratorSymbol(
    family="ν",
  )
  nu_prime = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  assert nu_plain.family == nu_prime.family
  assert nu_plain != nu_prime


def test_phase22_5_indexed_eta_generator_representation():
  eta_3 = GeneratorSymbol(
    family="η",
    index=3,
  )

  assert eta_3.family == "η"
  assert eta_3.index == 3
  assert eta_3.decoration is None


def test_phase22_5_indexed_mu_generator_representation():
  mu_3 = GeneratorSymbol(
    family="μ",
    index=3,
  )

  assert mu_3.family == "μ"
  assert mu_3.index == 3
  assert mu_3.decoration is None


def test_phase22_5_indexed_iota_generator_representation():
  iota_7 = GeneratorSymbol(
    family="ι",
    index=7,
  )

  assert iota_7.family == "ι"
  assert iota_7.index == 7
  assert iota_7.decoration is None


def test_phase22_5_indexed_generator_families_remain_distinct():
  eta_3 = GeneratorSymbol(
    family="η",
    index=3,
  )
  mu_3 = GeneratorSymbol(
    family="μ",
    index=3,
  )

  assert eta_3 != mu_3


def test_phase22_5_index_is_part_of_generator_identity():
  iota_7 = GeneratorSymbol(
    family="ι",
    index=7,
  )
  iota_8 = GeneratorSymbol(
    family="ι",
    index=8,
  )

  assert iota_7 != iota_8


def test_homotopy_element():
  element = HomotopyElement(
    name="η",
    dimension=3,
  )

  assert element.name == "η"
  assert element.dimension == 3


def test_homotopy_element_preserves_source_and_target():
  element = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  assert element.name == "α"
  assert element.dimension == 3
  assert element.source == 5
  assert element.target == 3


def test_homotopy_element_source_and_target_default_to_none():
  element = HomotopyElement(
    name="η",
    dimension=3,
  )

  assert element.name == "η"
  assert element.dimension == 3
  assert element.source is None
  assert element.target is None


def test_phase21_2_source_and_target_affect_structural_equality():
  source_mismatch = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  different_source = HomotopyElement(
    name="α",
    dimension=3,
    source=6,
    target=3,
  )

  target_mismatch = HomotopyElement(
    name="β",
    dimension=4,
    source=7,
    target=4,
  )

  different_target = HomotopyElement(
    name="β",
    dimension=4,
    source=7,
    target=5,
  )

  assert source_mismatch != different_source
  assert target_mismatch != different_target


def test_phase21_2_same_typed_homotopy_elements_are_structurally_equal():
  first = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  second = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  assert first == second


def test_phase21_2_untyped_and_typed_homotopy_elements_are_structurally_distinct():
  untyped = HomotopyElement(
    name="α",
    dimension=3,
  )

  typed = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  assert untyped != typed


def test_phase21_3_suspension_shifts_source_and_target():
  alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  suspended = Suspension(
    expression=alpha,
  )

  assert suspended.expression == alpha
  assert suspended.source == 6
  assert suspended.target == 4


def test_phase21_3_suspension_preserves_unknown_typing():
  source_only = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=None,
  )

  target_only = HomotopyElement(
    name="β",
    dimension=4,
    source=None,
    target=4,
  )

  suspended_source_only = Suspension(
    expression=source_only,
  )

  suspended_target_only = Suspension(
    expression=target_only,
  )

  assert suspended_source_only.source == 6
  assert suspended_source_only.target is None

  assert suspended_target_only.source is None
  assert suspended_target_only.target == 5


def test_phase21_3_nested_suspension_shifts_source_and_target_repeatedly():
  alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  once = Suspension(
    expression=alpha,
  )

  twice = Suspension(
    expression=once,
  )

  assert once.source == 6
  assert once.target == 4

  assert twice.source == 7
  assert twice.target == 5


def test_phase21_4_iterated_suspension_shifts_source_and_target_for_concrete_exponent():
  alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=7,
    target=3,
  )

  suspended = IteratedSuspension(
    expression=alpha,
    exponent=2,
  )

  assert suspended.expression == alpha
  assert suspended.exponent == 2
  assert suspended.source == 9
  assert suspended.target == 5


def test_phase21_4_iterated_suspension_preserves_unknown_typing():
  source_only = HomotopyElement(
    name="α",
    dimension=3,
    source=7,
    target=None,
  )

  target_only = HomotopyElement(
    name="β",
    dimension=4,
    source=None,
    target=4,
  )

  suspended_source_only = IteratedSuspension(
    expression=source_only,
    exponent=3,
  )

  suspended_target_only = IteratedSuspension(
    expression=target_only,
    exponent=3,
  )

  assert suspended_source_only.source == 10
  assert suspended_source_only.target is None

  assert suspended_target_only.source is None
  assert suspended_target_only.target == 7


def test_phase21_4_symbolic_exponent_does_not_produce_source_or_target():
  alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=7,
    target=3,
  )

  t = ScalarSymbol(
    name="t",
  )

  suspended = IteratedSuspension(
    expression=alpha,
    exponent=t,
  )

  assert suspended.expression == alpha
  assert suspended.exponent == t
  assert suspended.source is None
  assert suspended.target is None


def test_phase21_4_iterated_suspension_shifts_already_suspended_expression():
  alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=7,
    target=3,
  )

  once = Suspension(
    expression=alpha,
  )

  iterated = IteratedSuspension(
    expression=once,
    exponent=2,
  )

  assert once.source == 8
  assert once.target == 4

  assert iterated.source == 10
  assert iterated.target == 6


def test_phase21_4_negative_exponent_does_not_produce_source_or_target():
  alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=7,
    target=3,
  )

  suspended = IteratedSuspension(
    expression=alpha,
    exponent=-1,
  )

  assert suspended.source is None
  assert suspended.target is None


def test_phase21_5_composition_is_type_compatible_for_matching_boundary():
  alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  beta = HomotopyElement(
    name="β",
    dimension=5,
    source=7,
    target=5,
  )

  composition = Composition(
    left=alpha,
    right=beta,
  )

  assert alpha.source == beta.target
  assert composition.is_type_compatible()


def test_phase21_5_composition_uses_suspension_typing():
  alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  beta = HomotopyElement(
    name="β",
    dimension=6,
    source=8,
    target=6,
  )

  suspended_alpha = Suspension(
    expression=alpha,
  )

  composition = Composition(
    left=suspended_alpha,
    right=beta,
  )

  assert suspended_alpha.source == 6
  assert beta.target == 6
  assert composition.is_type_compatible()


def test_phase21_5_composition_uses_concrete_iterated_suspension_typing():
  alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  beta = HomotopyElement(
    name="β",
    dimension=7,
    source=9,
    target=7,
  )

  iterated_alpha = IteratedSuspension(
    expression=alpha,
    exponent=2,
  )

  composition = Composition(
    left=iterated_alpha,
    right=beta,
  )

  assert iterated_alpha.source == 7
  assert beta.target == 7
  assert composition.is_type_compatible()


def test_phase21_5_unknown_typing_is_not_type_compatible():
  untyped_alpha = HomotopyElement(
    name="α",
    dimension=3,
  )

  beta = HomotopyElement(
    name="β",
    dimension=5,
    source=7,
    target=5,
  )

  left_unknown = Composition(
    left=untyped_alpha,
    right=beta,
  )

  alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  untyped_beta = HomotopyElement(
    name="β",
    dimension=5,
  )

  right_unknown = Composition(
    left=alpha,
    right=untyped_beta,
  )

  assert not left_unknown.is_type_compatible()
  assert not right_unknown.is_type_compatible()


def test_phase21_6_known_mismatch_is_not_type_compatible():
  alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  beta = HomotopyElement(
    name="β",
    dimension=4,
    source=7,
    target=4,
  )

  composition = Composition(
    left=alpha,
    right=beta,
  )

  assert alpha.source == 5
  assert beta.target == 4
  assert alpha.source != beta.target
  assert not composition.is_type_compatible()


def test_phase21_6_mismatched_composition_remains_constructible():
  alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  beta = HomotopyElement(
    name="β",
    dimension=4,
    source=7,
    target=4,
  )

  composition = Composition(
    left=alpha,
    right=beta,
  )

  assert composition.left == alpha
  assert composition.right == beta
  assert not composition.is_type_compatible()


def test_phase21_7_toda_entries_are_composition_compatible():
  a = HomotopyElement(
    name="a",
    dimension=3,
    source=5,
    target=3,
  )

  b = HomotopyElement(
    name="b",
    dimension=5,
    source=7,
    target=5,
  )

  c = HomotopyElement(
    name="c",
    dimension=7,
    source=9,
    target=7,
  )

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  assert Composition(
    left=a,
    right=b,
  ).is_type_compatible()

  assert Composition(
    left=b,
    right=c,
  ).is_type_compatible()

  assert (
    bracket
    .are_defining_compositions_type_compatible()
  )


def test_phase21_7_first_toda_composition_mismatch_is_incompatible():
  a = HomotopyElement(
    name="a",
    dimension=3,
    source=5,
    target=3,
  )

  b = HomotopyElement(
    name="b",
    dimension=4,
    source=7,
    target=4,
  )

  c = HomotopyElement(
    name="c",
    dimension=7,
    source=9,
    target=7,
  )

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  assert not Composition(
    left=a,
    right=b,
  ).is_type_compatible()

  assert Composition(
    left=b,
    right=c,
  ).is_type_compatible()

  assert not (
    bracket
    .are_defining_compositions_type_compatible()
  )


def test_phase21_7_second_toda_composition_mismatch_is_incompatible():
  a = HomotopyElement(
    name="a",
    dimension=3,
    source=5,
    target=3,
  )

  b = HomotopyElement(
    name="b",
    dimension=5,
    source=7,
    target=5,
  )

  c = HomotopyElement(
    name="c",
    dimension=6,
    source=9,
    target=6,
  )

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  assert Composition(
    left=a,
    right=b,
  ).is_type_compatible()

  assert not Composition(
    left=b,
    right=c,
  ).is_type_compatible()

  assert not (
    bracket
    .are_defining_compositions_type_compatible()
  )


def test_phase21_7_unknown_toda_typing_is_not_compatible():
  a = HomotopyElement(
    name="a",
    dimension=3,
    source=5,
    target=3,
  )

  b = HomotopyElement(
    name="b",
    dimension=5,
  )

  c = HomotopyElement(
    name="c",
    dimension=7,
    source=9,
    target=7,
  )

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  assert not (
    bracket
    .are_defining_compositions_type_compatible()
  )


def test_phase21_8_representative_typed_toda_scenario():
  a = HomotopyElement(
    name="a",
    dimension=3,
    source=5,
    target=3,
  )

  b_base = HomotopyElement(
    name="b",
    dimension=4,
    source=6,
    target=4,
  )

  c_base = HomotopyElement(
    name="c",
    dimension=5,
    source=9,
    target=5,
  )

  b = Suspension(
    expression=b_base,
  )

  c = IteratedSuspension(
    expression=c_base,
    exponent=2,
  )

  first_composition = Composition(
    left=a,
    right=b,
  )

  second_composition = Composition(
    left=b,
    right=c,
  )

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  assert a.source == 5
  assert a.target == 3

  assert b.source == 7
  assert b.target == 5

  assert c.source == 11
  assert c.target == 7

  assert first_composition.is_type_compatible()
  assert second_composition.is_type_compatible()

  assert (
    bracket
    .are_defining_compositions_type_compatible()
  )


def test_phase21_9_typing_boundary_regression():
  typed_alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  same_typed_alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  different_source_alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=6,
    target=3,
  )

  untyped_alpha = HomotopyElement(
    name="α",
    dimension=3,
  )

  assert typed_alpha == same_typed_alpha
  assert typed_alpha != different_source_alpha
  assert typed_alpha != untyped_alpha

  suspended = Suspension(
    expression=typed_alpha,
  )

  assert suspended.source == 6
  assert suspended.target == 4

  concrete_iterated = IteratedSuspension(
    expression=typed_alpha,
    exponent=2,
  )

  assert concrete_iterated.source == 7
  assert concrete_iterated.target == 5

  t = ScalarSymbol(
    name="t",
  )

  symbolic_iterated = IteratedSuspension(
    expression=typed_alpha,
    exponent=t,
  )

  assert symbolic_iterated.source is None
  assert symbolic_iterated.target is None

  negative_iterated = IteratedSuspension(
    expression=typed_alpha,
    exponent=-1,
  )

  assert negative_iterated.source is None
  assert negative_iterated.target is None

  compatible_beta = HomotopyElement(
    name="β",
    dimension=5,
    source=7,
    target=5,
  )

  compatible_composition = Composition(
    left=typed_alpha,
    right=compatible_beta,
  )

  assert compatible_composition.is_type_compatible()

  mismatched_beta = HomotopyElement(
    name="β",
    dimension=4,
    source=7,
    target=4,
  )

  mismatched_composition = Composition(
    left=typed_alpha,
    right=mismatched_beta,
  )

  assert mismatched_composition.left == typed_alpha
  assert mismatched_composition.right == mismatched_beta
  assert not mismatched_composition.is_type_compatible()

  unknown_composition = Composition(
    left=untyped_alpha,
    right=compatible_beta,
  )

  assert not unknown_composition.is_type_compatible()


def test_phase21_9_toda_compatibility_boundary_regression():
  a = HomotopyElement(
    name="a",
    dimension=3,
    source=5,
    target=3,
  )

  b = HomotopyElement(
    name="b",
    dimension=5,
    source=7,
    target=5,
  )

  c = HomotopyElement(
    name="c",
    dimension=7,
    source=9,
    target=7,
  )

  compatible_bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  assert (
    compatible_bracket
    .are_defining_compositions_type_compatible()
  )

  first_mismatch_b = HomotopyElement(
    name="b",
    dimension=4,
    source=7,
    target=4,
  )

  first_mismatch_bracket = TodaBracket(
    first=a,
    second=first_mismatch_b,
    third=c,
  )

  assert not (
    first_mismatch_bracket
    .are_defining_compositions_type_compatible()
  )

  second_mismatch_c = HomotopyElement(
    name="c",
    dimension=6,
    source=9,
    target=6,
  )

  second_mismatch_bracket = TodaBracket(
    first=a,
    second=b,
    third=second_mismatch_c,
  )

  assert not (
    second_mismatch_bracket
    .are_defining_compositions_type_compatible()
  )

  untyped_b = HomotopyElement(
    name="b",
    dimension=5,
  )

  unknown_bracket = TodaBracket(
    first=a,
    second=untyped_b,
    third=c,
  )

  assert not (
    unknown_bracket
    .are_defining_compositions_type_compatible()
  )

  indexed_bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
    index=2,
  )

  assert (
    indexed_bracket
    .are_defining_compositions_type_compatible()
  )

  assert indexed_bracket.index == 2
  assert indexed_bracket != compatible_bracket


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


def test_indexed_toda_bracket_data_preserves_symbolic_indexed_toda_correspondence():
  a = eta(3)

  b = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  c = nu(6)

  t = ScalarSymbol(
    name="t",
  )

  second = IteratedSuspension(
    expression=b,
    exponent=t,
  )

  third = IteratedSuspension(
    expression=c,
    exponent=t,
  )

  bracket = TodaBracket(
    first=a,
    second=second,
    third=third,
    index=t,
  )

  data = IndexedTodaBracketData(
    bracket=bracket,
    second_base=b,
    third_base=c,
    suspension_exponent=t,
  )

  assert data.bracket.first == a

  assert data.bracket.second == IteratedSuspension(
    expression=data.second_base,
    exponent=data.suspension_exponent,
  )

  assert data.bracket.third == IteratedSuspension(
    expression=data.third_base,
    exponent=data.suspension_exponent,
  )

  assert data.bracket.index == data.suspension_exponent

  assert data.bracket.second.exponent == data.bracket.index
  assert data.bracket.third.exponent == data.bracket.index

  assert data.bracket.second.expression == data.second_base
  assert data.bracket.third.expression == data.third_base


def test_indexed_toda_bracket_data_is_consistent_for_symbolic_indexed_toda_form():
  a = eta(3)

  b = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  c = nu(6)

  t = ScalarSymbol(
    name="t",
  )

  data = IndexedTodaBracketData(
    bracket=TodaBracket(
      first=a,
      second=IteratedSuspension(
        expression=b,
        exponent=t,
      ),
      third=IteratedSuspension(
        expression=c,
        exponent=t,
      ),
      index=t,
    ),
    second_base=b,
    third_base=c,
    suspension_exponent=t,
  )

  assert data.is_consistent()


def test_indexed_toda_bracket_data_is_inconsistent_when_index_differs_from_suspension_exponent():
  a = eta(3)

  b = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  c = nu(6)

  t = ScalarSymbol(
    name="t",
  )

  s = ScalarSymbol(
    name="s",
  )

  data = IndexedTodaBracketData(
    bracket=TodaBracket(
      first=a,
      second=IteratedSuspension(
        expression=b,
        exponent=t,
      ),
      third=IteratedSuspension(
        expression=c,
        exponent=t,
      ),
      index=s,
    ),
    second_base=b,
    third_base=c,
    suspension_exponent=t,
  )

  assert not data.is_consistent()


def test_indexed_toda_bracket_data_is_inconsistent_when_second_entry_does_not_match_base():
  a = eta(3)

  b = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  other_b = HomotopyElement(
    name="ν″",
    dimension=3,
  )

  c = nu(6)

  t = ScalarSymbol(
    name="t",
  )

  data = IndexedTodaBracketData(
    bracket=TodaBracket(
      first=a,
      second=IteratedSuspension(
        expression=other_b,
        exponent=t,
      ),
      third=IteratedSuspension(
        expression=c,
        exponent=t,
      ),
      index=t,
    ),
    second_base=b,
    third_base=c,
    suspension_exponent=t,
  )

  assert not data.is_consistent()


def test_indexed_toda_bracket_data_is_inconsistent_when_third_entry_does_not_match_base():
  a = eta(3)

  b = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  c = nu(6)
  other_c = nu(7)

  t = ScalarSymbol(
    name="t",
  )

  data = IndexedTodaBracketData(
    bracket=TodaBracket(
      first=a,
      second=IteratedSuspension(
        expression=b,
        exponent=t,
      ),
      third=IteratedSuspension(
        expression=other_c,
        exponent=t,
      ),
      index=t,
    ),
    second_base=b,
    third_base=c,
    suspension_exponent=t,
  )

  assert not data.is_consistent()


def test_indexed_toda_bracket_data_is_consistent_for_concrete_indexed_toda_form():
  a = eta(3)

  b = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  c = nu(6)

  exponent = 2

  data = IndexedTodaBracketData(
    bracket=TodaBracket(
      first=a,
      second=IteratedSuspension(
        expression=b,
        exponent=exponent,
      ),
      third=IteratedSuspension(
        expression=c,
        exponent=exponent,
      ),
      index=exponent,
    ),
    second_base=b,
    third_base=c,
    suspension_exponent=exponent,
  )

  assert data.is_consistent()


def test_phase20_representative_indexed_toda_expression_and_boundary():
  a = eta(3)

  b = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  c = nu(6)

  t = ScalarSymbol(
    name="t",
  )

  s = ScalarSymbol(
    name="s",
  )

  second = IteratedSuspension(
    expression=b,
    exponent=t,
  )

  third = IteratedSuspension(
    expression=c,
    exponent=t,
  )

  bracket = TodaBracket(
    first=a,
    second=second,
    third=third,
    index=t,
  )

  data = IndexedTodaBracketData(
    bracket=bracket,
    second_base=b,
    third_base=c,
    suspension_exponent=t,
  )

  assert data.bracket.first == a

  assert data.bracket.second == IteratedSuspension(
    expression=b,
    exponent=t,
  )

  assert data.bracket.third == IteratedSuspension(
    expression=c,
    exponent=t,
  )

  assert data.bracket.index == t
  assert data.suspension_exponent == t

  assert data.bracket.second.exponent == data.suspension_exponent
  assert data.bracket.third.exponent == data.suspension_exponent
  assert data.bracket.index == data.suspension_exponent

  assert data.is_consistent()

  same_data = IndexedTodaBracketData(
    bracket=TodaBracket(
      first=a,
      second=IteratedSuspension(
        expression=b,
        exponent=ScalarSymbol(
          name="t",
        ),
      ),
      third=IteratedSuspension(
        expression=c,
        exponent=ScalarSymbol(
          name="t",
        ),
      ),
      index=ScalarSymbol(
        name="t",
      ),
    ),
    second_base=b,
    third_base=c,
    suspension_exponent=ScalarSymbol(
      name="t",
    ),
  )

  assert data == same_data

  assert IteratedSuspension(
    expression=b,
    exponent=1,
  ) != Suspension(
    b,
  )

  assert IteratedSuspension(
    expression=b,
    exponent=2,
  ) != Suspension(
    Suspension(
      b,
    ),
  )

  assert IteratedSuspension(
    expression=b,
    exponent=t,
  ) != IteratedSuspension(
    expression=b,
    exponent=2,
  )

  assert TodaBracket(
    first=a,
    second=second,
    third=third,
    index=t,
  ) != TodaBracket(
    first=a,
    second=second,
    third=third,
    index=2,
  )

  inconsistent_data = IndexedTodaBracketData(
    bracket=TodaBracket(
      first=a,
      second=IteratedSuspension(
        expression=b,
        exponent=t,
      ),
      third=IteratedSuspension(
        expression=c,
        exponent=t,
      ),
      index=s,
    ),
    second_base=b,
    third_base=c,
    suspension_exponent=t,
  )

  assert inconsistent_data.bracket.index == s
  assert inconsistent_data.suspension_exponent == t
  assert not inconsistent_data.is_consistent()






