"""R4R14R3 focused read-only audit contracts."""
from __future__ import annotations

from pathlib import Path

from phase175_r4r14r3_binary_composition_audit import audit


def test_binary_suspension_and_zero_propagation_are_separate_obligations() -> None:
    from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase169_r10e5_composite_generator_image.rule import component_image_obligations
    from phase174_r3_r7_r7_composite_zero_audit.rule import composite_zero_generator_inputs

    a = HomotopyElement("a", 5, 8, 5, GeneratorSymbol("a", 5))
    b = HomotopyElement("b", 8, 9, 8, GeneratorSymbol("b", 8))
    a1 = HomotopyElement("a1", 6, 9, 6, GeneratorSymbol("a", 6))
    b1 = HomotopyElement("b1", 9, 10, 9, GeneratorSymbol("b", 9))
    source = Composition(a, b)
    target = Composition(a1, b1)
    mapping = TodaSuspensionMap(TodaPrimaryGroup(9, 5), TodaPrimaryGroup(10, 6))
    assert len(component_image_obligations(GeneratorImage(mapping, source, target))) == 2
    obligations = composite_zero_generator_inputs(GeneratorImage(mapping, source, Zero()),
                                                  GeneratorImage(mapping, source, target))
    assert obligations is not None
    assert obligations[1].lhs == a1
    assert obligations[1].lhs != target


def test_audit_has_no_mutation_or_new_mathematical_axiom() -> None:
    code = (Path(__file__).resolve().parents[1] / "audit.py").read_text(encoding="utf-8")
    assert chr(34) + "new_given" + chr(34) in code
    assert chr(34) + "new_rules" + chr(34) in code
    assert "hash-object" in code
    assert "BINARY_COMPOSITION_ZERO_PROPAGATION_GAP" in code


def test_source_guard_pin_format() -> None:
    assert len(audit.SOURCE_BLOBS) == 7
    assert all(len(blob) == 40 for blob in audit.SOURCE_BLOBS.values())
