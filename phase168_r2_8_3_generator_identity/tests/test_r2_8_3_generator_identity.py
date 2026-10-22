from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension, Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation


def el(name, index, stem, *, with_degrees=True, family=None, decoration=None):
    return HomotopyElement(name, index, index + stem if with_degrees else None,
                           index if with_degrees else None,
                           GeneratorSymbol(family or name.split('_')[0], index=index, decoration=decoration))


def eta(index, typed):
    return HomotopyElement(f"η{index}" if typed else f"η_{index}", index,
                           index + 1 if typed else None, index if typed else None,
                           GeneratorSymbol("η", index=index))


def eta_power(n, exponent, typed):
    expression = eta(n + exponent - 1, typed)
    for index in reversed(range(n, n + exponent - 1)):
        expression = Composition(eta(index, typed), expression)
    return FiniteCyclicGroup(2, expression)


def test_eta_squared_metadata_does_not_block_same_generators():
    assert same_registered_group_presentation(eta_power(2, 2, True), eta_power(2, 2, False))
    assert same_registered_group_presentation(eta_power(3, 2, True), eta_power(3, 2, False))
    assert same_registered_group_presentation(eta_power(4, 2, True), eta_power(4, 2, False))


def test_eta_cubed_nested_composition():
    assert same_registered_group_presentation(eta_power(2, 3, True), eta_power(2, 3, False))


def test_nu_prime_db_symbol_matches_registry_decorated_symbol():
    db = HomotopyElement("ν'", 3, 6, 3, GeneratorSymbol("\\nu'"))
    literature = HomotopyElement("ν′", 3, generator=GeneratorSymbol("ν", index=3, decoration="′"))
    assert same_registered_group_presentation(FiniteCyclicGroup(4, db), FiniteCyclicGroup(4, literature))


def test_direct_sum_suspension_equivalence():
    nu_db = HomotopyElement("ν₄", 4, 7, 4, GeneratorSymbol("ν", 4))
    nu_lit = HomotopyElement("ν_4", 4, generator=GeneratorSymbol("ν", 4))
    prime_db = HomotopyElement("ν'", 3, 6, 3, GeneratorSymbol("\\nu'"))
    prime_lit = HomotopyElement("ν′", 3, generator=GeneratorSymbol("ν", 3, "′"))
    a = DirectSumGroup((FreeCyclicGroup(nu_db), FiniteCyclicGroup(4, IteratedSuspension(prime_db, 1))))
    b = DirectSumGroup((FreeCyclicGroup(nu_lit), FiniteCyclicGroup(4, Suspension(prime_lit))))
    assert same_registered_group_presentation(a, b)


def test_reject_wrong_index_order_and_group_shape():
    assert not same_registered_group_presentation(eta_power(2, 2, True), eta_power(3, 2, False))
    assert not same_registered_group_presentation(eta_power(2, 2, True), FiniteCyclicGroup(4, eta_power(2, 2, False).generator))
    assert not same_registered_group_presentation(eta_power(2, 2, True), FreeCyclicGroup(eta_power(2, 2, False).generator))


def test_reject_contradictory_source_target():
    invalid = HomotopyElement("η_2", 2, 55, 2, GeneratorSymbol("η", 2))
    assert not same_registered_group_presentation(FiniteCyclicGroup(2, invalid), FiniteCyclicGroup(2, eta(2, True)))
