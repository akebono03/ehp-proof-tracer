import ast
import pytest
from apply import REPLACEMENT,transform

BEFORE='''from dataclasses import dataclass
from toda_calculation_facade import build_standard_toda_report
from toda_human_readable_renderer import render_toda_group_result_latex
class WebGroupQueryView:
    pass

def build_standard_web_group_query_view(n: int,k: int):
    report=build_standard_toda_report(n=n,k=k)
    return report
'''

def test_changes_only_intended_entry():
    after,changed=transform(BEFORE)
    assert changed
    assert 'build_standard_toda_report' not in after
    assert 'render_toda_group_result_latex' not in after
    assert 'search_group_structure_automatically' in after
    ast.parse(after)

def test_idempotence():
    after,_=transform(BEFORE)
    again,changed=transform(after)
    assert not changed
    assert again==after

def test_refuse_unknown_entry():
    with pytest.raises(RuntimeError,match='unknown Group Query'):
        transform(BEFORE.replace('build_standard_toda_report(n=n,k=k)','object()'))

def test_refuse_cross_use():
    with pytest.raises(RuntimeError,match='outside Group Query'):
        transform(BEFORE+'\ndef other(): return build_standard_toda_report()\n')

def test_function_signature():
    n=ast.parse(REPLACEMENT).body[0]
    assert [a.arg for a in n.args.args]==['n','k']

def test_no_unproven_found():
    t=ast.parse(REPLACEMENT)
    body=ast.unparse(t)
    assert 'ProofSearchStatus.COMPLETE' in body
    assert 'TodaCalculationStatus.NOT_FOUND' in body
    assert 'result.conclusion' in body

def test_preserves_view_class():
    out,_=transform(BEFORE)
    assert any(isinstance(n,ast.ClassDef) and n.name=='WebGroupQueryView' for n in ast.parse(out).body)
