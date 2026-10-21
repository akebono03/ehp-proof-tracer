from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension
from phase166_r3ao_semantic_type_audit.audit import expression_dimensions


def test_eta_composition_dimensions():
    a = HomotopyElement('η13', 13, source=14, target=13, generator=GeneratorSymbol('η', 13))
    b = HomotopyElement('η14', 14, source=15, target=14, generator=GeneratorSymbol('η', 14))
    assert expression_dimensions(Composition(a, b)) == (15, 13, [])


def test_reject_mismatched_composition():
    a = HomotopyElement('η13', 13, source=14, target=13)
    b = HomotopyElement('η15', 15, source=16, target=15)
    assert 'composition_interface_mismatch' in expression_dimensions(Composition(a, b))[2]


def test_suspension_dimension():
    nu_prime = HomotopyElement('ν′', 3, source=6, target=3)
    assert expression_dimensions(IteratedSuspension(nu_prime, 1)) == (7, 4, [])
