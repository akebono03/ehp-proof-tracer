"""R3R24 replacement is bounded to one complete function."""
from __future__ import annotations
import ast
import pytest
from phase176_r3r24_composite_left_formula_specialization.installer import replacement_text

def test_replacement_only_named_function() -> None:
    old = ('def before():\n    return 1\n\n'
           'def _formula_parts(goal):\n    not isinstance(alpha, HomotopyElement)\n    product.is_type_compatible()\n    expected = Composition(MapApplication(EHP_H_MAP, alpha), right)\n\n'
           'def after():\n    return 2\n')
    new = replacement_text(old)
    ast.parse(new)
    assert 'def before():' in new and 'def after():' in new
    assert 'expression_endpoints' in new

def test_unexpected_baseline_fails_closed() -> None:
    with pytest.raises(RuntimeError, match='BASELINE_CHANGED'):
        replacement_text('def _formula_parts(goal):\n    return None\n')
