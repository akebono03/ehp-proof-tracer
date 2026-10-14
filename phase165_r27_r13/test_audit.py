from pathlib import Path
from audit import category, collect, refs
import ast

def test_scope_priority():
    assert category(Path('tests/test_old.py'))=='TEST_ONLY_REFERENCE'
    assert category(Path('archive/foo.py'))=='HISTORICAL_OR_PACKAGE_REFERENCE'
    assert category(Path('web_app.py'))=='PUBLIC_ENTRY_OR_BRIDGE'

def test_ast_edges_distinguish_call_and_definition():
    x=refs(ast.parse('def build_standard_toda_report():\n  pass\nbuild_standard_toda_report()\n'))
    assert ('build_standard_toda_report','definition',1) in x
    assert ('build_standard_toda_report','call',3) in x

def test_report_is_conservative():
    r=collect(Path.cwd())
    assert r['deletion_authorized'] is False
    assert r['unused_code_certified'] is False
    assert r['full_pytest_run'] is False
    assert r['files_with_references']>0
