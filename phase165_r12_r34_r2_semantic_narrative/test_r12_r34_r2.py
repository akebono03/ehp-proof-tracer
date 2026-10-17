from phase165_r12_r34_r2_semantic_narrative import _element, _group
from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaPrimaryGroup
import pytest

def test_group_latex():
    assert _group(TodaPrimaryGroup(4,3)) == r"\pi_{4}^{3}"

def test_typed_generator_latex():
    assert _element(HomotopyElement(name="η₂",dimension=2, source=3,target=2,generator=GeneratorSymbol("η",2))) == "η_{2}"

def test_untyped_generator_rejected():
    with pytest.raises(ValueError):
        _element(object())
