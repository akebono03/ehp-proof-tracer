import ast
from pathlib import Path
import sys
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parent))
from apply import transform, apply

SAMPLE='''from repository_proof_scope import build_repository_proof_scope
from repository_symbolic_sigma_specialization import specialize_repository_proof_scope_for_generator

def first(scope):
    return build_repository_proof_scope(scope)

def second(scope):
    return specialize_repository_proof_scope_for_generator(scope)
'''
MODS=frozenset({'repository_proof_scope','repository_symbolic_sigma_specialization'})

def test_two_functions_deferred():
    result,changed,moved=transform(SAMPLE,MODS)
    assert changed and len(moved)==2
    code=ast.parse(result)
    assert not any(isinstance(n,ast.ImportFrom) and n.module in MODS for n in code.body)
    assert len([n for n in ast.walk(code) if isinstance(n,ast.ImportFrom) and n.module in MODS])==2

def test_preserves_implementation():
    result,_,_=transform(SAMPLE,MODS)
    assert 'return build_repository_proof_scope(scope)' in result
    assert 'return specialize_repository_proof_scope_for_generator(scope)' in result

def test_idempotence():
    result,_,_=transform(SAMPLE,MODS)
    again,changed,_=transform(result,MODS)
    assert not changed and again==result

def test_top_level_use_rejected():
    with pytest.raises(RuntimeError,match='module scope'):
        transform(SAMPLE+'x = build_repository_proof_scope(None)\n',MODS)

def test_alias_rejected():
    with pytest.raises(RuntimeError,match='aliased'):
        transform('from repository_proof_scope import build_repository_proof_scope as alias\n',MODS)

def test_unexpected_source_rejected():
    with pytest.raises(RuntimeError,match='absent'):
        transform('def x():\n    return 1\n',MODS)

def test_docstring_position():
    s='''from repository_proof_scope import build_repository_proof_scope

def x():
    """Doc."""
    return build_repository_proof_scope(None)
'''
    result,_,_=transform(s,MODS)
    assert ast.get_docstring(ast.parse(result).body[-1])=='Doc.'

def test_apply_idempotent_in_temporary_project(tmp_path):
    (tmp_path/'toda_calculation.py').write_text(SAMPLE,encoding='utf-8')
    (tmp_path/'toda_calculation_report.py').write_text('from toda_calculation import build_toda_calculation_result\n\ndef report():\n    return build_toda_calculation_result(None,None)\n',encoding='utf-8')
    assert apply(tmp_path)['status']=='CHANGED'
    assert apply(tmp_path)['status']=='ALREADY_INSTALLED'

def test_backup_conflict_fails_without_writing(tmp_path):
    (tmp_path/'toda_calculation.py').write_text(SAMPLE,encoding='utf-8')
    (tmp_path/'toda_calculation_report.py').write_text('from toda_calculation import build_toda_calculation_result\n\ndef report():\n    return build_toda_calculation_result(None,None)\n',encoding='utf-8')
    b=tmp_path/'phase165_r27_r55_backup';b.mkdir()
    (b/'toda_calculation.py').write_text('conflict',encoding='utf-8')
    with pytest.raises(RuntimeError,match='backup conflict'):
        apply(tmp_path)
    assert (tmp_path/'toda_calculation.py').read_text(encoding='utf-8')==SAMPLE
