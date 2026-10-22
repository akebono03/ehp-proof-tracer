from expression import Composition, GeneratorSymbol, HomotopyElement
from phase168_r2_8_2_structured_generator_audit.audit import differences, structure


def test_generator_symbol_fields_are_preserved():
    value = GeneratorSymbol(family="ν", index=3, decoration="′")
    assert structure(value) == {"type": "GeneratorSymbol", "family": "ν", "index": 3, "decoration": "′"}


def test_composition_is_not_flattened_to_display_text():
    left = HomotopyElement("η₂", 2, source=3, target=2, generator=GeneratorSymbol("η", 2))
    right = HomotopyElement("η₃", 3, source=4, target=3, generator=GeneratorSymbol("η", 3))
    tree = structure(Composition(left, right))
    assert tree["type"] == "Composition"
    assert tree["left"]["generator"]["index"] == 2
    assert tree["right"]["generator"]["index"] == 3
    assert tree["type_compatible"] is True


def test_difference_reports_exact_family_path():
    left = structure(GeneratorSymbol(family="\\nu'"))
    right = structure(GeneratorSymbol(family="ν", index=3, decoration="′"))
    paths = {item["path"] for item in differences(left, right)}
    assert paths == {"rhs.family", "rhs.index", "rhs.decoration"}


def test_identical_structure_has_no_differences():
    symbol = structure(GeneratorSymbol("η", 2))
    assert differences(symbol, symbol) == []
