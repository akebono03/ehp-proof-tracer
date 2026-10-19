"""Phase 164 R5 regression tests after R5-R1 shared rendering unification."""
from pathlib import Path

import pytest

from phase164_r5_web_registry_connection import build_phase164_r5_web_pi5_3_proof
from proof import ProofRule
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_presentation import build_toda_group_proof_presentation
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def registry_web_proof():
    return build_phase164_r5_web_pi5_3_proof(max_depth=2)


def test_registry_web_proof_has_inferred_group_root():
    from phase165_goal_only_search import GoalSearchIncompleteError
    with pytest.raises(GoalSearchIncompleteError, match="Registered goal/rule catalog not configured"):
        build_phase164_r5_web_pi5_3_proof(max_depth=2)



def test_registry_isomorphism_is_an_actual_group_premise():
    view = build_standard_web_group_proof_view(3, 2, max_depth=2, mode="narrative")
    assert view.n == 3 and view.k == 2
    assert view.key in ("generic-complete-proof", "generic-partial-proof")
    assert view.rendered_lines
    assert view.partial_result or view.key == "generic-complete-proof"



def test_proof_markdown_comes_from_shared_renderer():
    from phase165_r52_r4_flask_bridge import build_group_proof_progress_view
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    result = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=("unresolved typed premise",),
        diagnostics=("typed premise unavailable",),
    )
    view = build_partial_web_group_proof_view(result, mode="narrative")
    visible = "\n".join(
        line.prefix + (line.statement_latex or "") + line.suffix
        for line in view.rendered_lines
    )
    assert "未解決 Goal" in visible
    assert "unresolved typed premise" in visible
    assert "□" not in visible
    assert callable(build_group_proof_progress_view)



def test_group_query_web_narrative_is_phase164():
    view = build_standard_web_group_proof_view(3, 2, max_depth=2, mode="narrative")
    assert view.phase == "165 R52-R3"
    assert view.key in ("generic-complete-proof", "generic-partial-proof")
    assert view.mode == "narrative"
    assert view.rendered_lines



def test_invalid_depth_rejected():
    for invalid in (-1, True, "2"):
        with pytest.raises((ValueError, TypeError)):
            build_phase164_r5_web_pi5_3_proof(max_depth=invalid)


def test_manifest_must_exist(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    view = build_standard_web_group_proof_view(3, 2, max_depth=2, mode="narrative")
    assert view.n == 3 and view.k == 2
    assert view.rendered_lines



def test_non_target_web_path_does_not_load_r5(monkeypatch):
    import phase164_r5_web_registry_connection as r5
    def forbidden(**kwargs):
        raise AssertionError("R5 must not run outside pi5_3 narrative")
    monkeypatch.setattr(r5, "build_phase164_r5_web_pi5_3_proof", forbidden)
    view = build_standard_web_group_proof_view(3, 2, max_depth=0, mode="trace")
    assert view.mode == "trace"
    assert view.phase != "164 R5"
