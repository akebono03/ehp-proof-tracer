from pathlib import Path
import ast

import pytest

import phase164_r5_r2_common_replay as selector
from phase165_goal_only_search import GoalSearchIncompleteError


@pytest.mark.parametrize('mode', ('narrative', 'trace', 'outline'))
@pytest.mark.parametrize('n,k', ((2, 1), (3, 1), (4, 1), (3, 2), (2, 2), (6, 3)))
def test_no_legacy_replay_for_any_mode(n, k, mode):
    with pytest.raises(GoalSearchIncompleteError, match='legacy proof selection remains disabled'):
        selector.build_phase164_r5_r2_common_replay(n, k, object(), 2, mode)


def test_no_fallback_in_selector_source():
    source = Path(selector.__file__).read_text(encoding='utf-8')
    function = next(node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef) and node.name == 'build_phase164_r5_r2_common_replay')
    text = ast.get_source_segment(source, function)
    assert 'build_toda_group_result_proof_replay' not in text
    assert 'build_toda_stable_eta_proof_replay' not in text
    assert 'build_phase164_r5_web_pi5_3_proof' not in text
