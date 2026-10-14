"""Focused tests for AST-safe removal and the retained generic path."""
from pathlib import Path
import ast
from install import FILES, NAME, retire_source

def test_r26_legacy_factory_removed_without_touching_neighbor():
    src = 'def before():\n    return 1\n\ndef '+NAME+'():\n    return 2\n\ndef after():\n    return 3\n'
    result, count = retire_source(src,'toda_rules.py')
    assert count == 1
    assert [n.name for n in ast.parse(result).body] == ['before','after']

def test_r26_bootstrap_retirement_removes_only_target():
    src = 'from toda_rules import (\n    other_rule,\n    '+NAME+',\n)\n\ndef run():\n    rules = (\n        other_rule(),\n        '+NAME+'(),\n    )\n    return rules\n'
    result, count = retire_source(src,'toda_upstream_bootstrap.py')
    assert count == 2
    assert 'other_rule()' in result
    assert NAME not in result
    ast.parse(result)

def test_r26_probe_retirement_same_contract():
    src = 'from toda_rules import (\n    other_rule,\n    '+NAME+',\n)\n\ndef run():\n    rules = (\n        '+NAME+'(),\n    )\n    return rules\n'
    result, count = retire_source(src,'probes/probe_phase49_capabilities.py')
    assert count == 2
    assert NAME not in result

def test_r26_active_source_references_removed():
    root = Path(__file__).resolve().parent.parent
    if not (root/'toda_rules.py').exists():
        import pytest
        pytest.skip('Requires EHP Proof Tracer repository')
    for name in FILES:
        assert NAME not in (root/name).read_text(encoding='utf-8')
