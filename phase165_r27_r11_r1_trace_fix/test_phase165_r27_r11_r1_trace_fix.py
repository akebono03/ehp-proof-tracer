import ast
from pathlib import Path

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view


@pytest.mark.parametrize('mode', ('trace', 'outline', 'narrative'))
def test_r27_r11_r1_incomplete_mode_contract(mode):
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=('unproven',), diagnostics=('No typed derivation',),
    )
    view = build_partial_web_group_proof_view(result, mode=mode)
    assert view.partial_result is True
    assert view.theorem is None
    assert view.conclusion_latex == r'\pi_{4}^{3}'
    if mode == 'trace':
        assert view.rendered_lines == ()
    else:
        assert view.rendered_lines
    assert not view.steps


def test_r27_r11_r1_adapter_keeps_common_module_dependency():
    tree = ast.parse(Path('phase165_r52_r3_web_adapter.py').read_text(encoding='utf-8-sig'))
    modules = {node.module for node in tree.body if isinstance(node, ast.ImportFrom)}
    assert 'web_group_proof_common' in modules
    assert 'web_group_proof' not in modules
