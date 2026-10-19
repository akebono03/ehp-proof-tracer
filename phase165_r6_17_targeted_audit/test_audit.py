import ast
from pathlib import Path
from audit import audit, get_func


def test_get_func_extracts_whole_function(tmp_path):
    p=tmp_path/'a.py'
    p.write_text('def example():\n    return 42\n', encoding='utf-8')
    n=get_func(p,'example')
    assert isinstance(n,ast.FunctionDef)
    assert n.lineno==1 and n.end_lineno==2


def test_missing_files_are_reported_without_changes(tmp_path):
    result=audit(tmp_path)
    assert result['status']=='NEEDS_REVIEW'
    assert all(r['status']=='MISSING_FILE' for r in result['items'])
    assert result['full_pytest_run'] is False


def test_required_context_names():
    tree=ast.parse('construct_registered_group_proof(n=3, k=2)')
    call=tree.body[0].value
    present=[k.arg for k in call.keywords]
    assert 'goal' not in present and 'citing_assertion_id' not in present
