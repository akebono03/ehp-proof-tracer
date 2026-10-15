"""R57-R9: audit safety and data contract, no system-wide tests."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase165_r57_r9_renderer_comparison.audit import (
    _math_signatures,
    _step_record,
    replace_attribute,
)


def test_temporary_renderer_override_restores_after_normal_exit():
    obj = SimpleNamespace(render='old')
    with replace_attribute(obj, 'render', 'new') as old:
        assert old == 'old'
        assert obj.render == 'new'
    assert obj.render == 'old'


def test_temporary_renderer_override_restores_after_exception():
    obj = SimpleNamespace(render='old')
    with pytest.raises(RuntimeError):
        with replace_attribute(obj, 'render', 'new'):
            raise RuntimeError('test')
    assert obj.render == 'old'


def test_step_record_has_unambiguous_premise_count():
    leaf = SimpleNamespace(rule=SimpleNamespace(value='given'), inference_rule=None, conclusion='leaf', premises=())
    root = SimpleNamespace(rule=SimpleNamespace(value='inference'), inference_rule=SimpleNamespace(name='Toda 4.5 generic finite-cyclic transport'), conclusion='target', premises=(leaf,))
    found = _step_record(root)
    assert found['premise_count'] == 1
    assert found['premise_types'] == ['str']
    assert '4.5' in found['inference_rule']


def test_math_signatures_do_not_claim_proof_equivalence():
    result = _math_signatures('使用する結果 (4.5) Proposition 5.1 証明 □')
    assert result['has_reference']
    assert result['has_toda45']
    assert result['has_prop51']
    assert result['has_qed']
    assert not result['has_unresolved']
