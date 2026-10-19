import ast
from pathlib import Path

def test_runner_requires_audited_scope():
    code = Path(__file__).with_name('resumable_full_pytest.py').read_text(encoding='utf-8')
    ast.parse(code)
    assert 'collection_scope.json' in code
    assert 'no whole-tree discovery' in code
    assert 'Scope changed; use a new results directory' in code

def test_install_verifies_runner():
    source = Path(__file__).with_name('install.ps1').read_text(encoding='utf-8-sig')
    assert 'Runner version verification failed' in source
    assert 'VERIFIED: audited-scope resumable runner installed' in source

def test_script_has_expected_marker():
    source = Path(__file__).with_name('run.ps1').read_text(encoding='utf-8-sig')
    assert 'PHASE165 RESUMABLE R6 FIX' in source
