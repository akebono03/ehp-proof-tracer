from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _function(path: str, name: str) -> ast.FunctionDef:
    tree = ast.parse((ROOT / path).read_text(encoding='utf-8'))
    found = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    assert len(found) == 1
    return found[0]


def test_shared_search_does_not_apply_legacy_order_gates():
    node = _function('phase165_r52_r9_shared_math.py', 'search_shared_group_goal')
    names = {child.id for child in ast.walk(node) if isinstance(child, ast.Name)}
    assert 'restrict_registered_ordered_claims' not in names
    assert 'restrict_by_proof_use_order' not in names
    assert 'resolve_registered_proof_use_order' not in names
    assert 'screen_shared_proof_context' in names


def test_pi43_audit_does_not_reapply_legacy_order_gate():
    node = _function('phase165_r12_r8_typed_source_connection.py', 'audit_real_pi43_quotient_connection')
    names = {child.id for child in ast.walk(node) if isinstance(child, ast.Name)}
    assert 'screen_shared_proof_context' in names
    assert 'restrict_registered_ordered_claims' not in names


def test_publication_order_check_remains_connected():
    node = _function('phase165_r52_r16_web_citation_gate.py', 'screen_shared_proof_context')
    names = {child.id for child in ast.walk(node) if isinstance(child, ast.Name)}
    assert 'precedes_citing_assertion' in names
    assert 'ProofStepLink' in names
    assert 'ProofStep' in names


def test_shared_search_keeps_existing_call_parameters():
    node = _function('phase165_r52_r9_shared_math.py', 'search_shared_group_goal')
    parameters = {arg.arg for arg in node.args.kwonlyargs}
    assert {'n', 'k', 'group_structure', 'proof_use_order', 'citing_assertion_id'} <= parameters
