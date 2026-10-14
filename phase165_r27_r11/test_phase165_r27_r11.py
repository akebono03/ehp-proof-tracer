import ast
from pathlib import Path

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from web_group_proof import build_standard_web_group_proof_view


def test_r27_r11_common_renderer_independent_of_legacy_module():
    source = Path('phase165_r52_r3_web_adapter.py').read_text(encoding='utf-8-sig')
    tree = ast.parse(source)
    imports = [node.module for node in tree.body if isinstance(node, ast.ImportFrom)]
    assert 'web_group_proof_common' in imports
    assert 'web_group_proof' not in imports


def test_r27_r11_legacy_builder_no_longer_calls_report_or_replay():
    source = Path('web_group_proof.py').read_text(encoding='utf-8-sig')
    tree = ast.parse(source)
    entry = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'build_standard_web_group_proof_view')
    calls = {node.func.id for node in ast.walk(entry) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    assert 'build_standard_toda_report' not in calls
    assert 'build_phase164_r5_r2_common_replay' not in calls
    assert 'search_group_structure_automatically' in calls


def test_r27_r11_compatibility_entry_never_claims_unknown_proof(monkeypatch):
    import phase165_r52_r5_auto_search as auto
    def fake(*, n, k):
        return make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED, open_goals=('unproven',), diagnostics=('No typed proof',))
    monkeypatch.setattr(auto, 'search_group_structure_automatically', fake)
    view = build_standard_web_group_proof_view(3, 1)
    assert view.partial_result is True
    assert view.theorem is None
    assert view.conclusion_latex == r'\pi_{4}^{3}'
    assert any('証明未完成' in line.prefix or any('証明未完成' in s.value for s in line.segments) for line in view.rendered_lines)


@pytest.mark.parametrize('mode', ['trace', 'outline', 'narrative'])
def test_r27_r11_mode_compatibility(monkeypatch, mode):
    import phase165_r52_r5_auto_search as auto
    monkeypatch.setattr(auto, 'search_group_structure_automatically', lambda *, n, k: make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED, diagnostics=('unproved',)))
    view = build_standard_web_group_proof_view(3, 1, mode=mode)
    assert view.mode == mode
    assert view.partial_result
