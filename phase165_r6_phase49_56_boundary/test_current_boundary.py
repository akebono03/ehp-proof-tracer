"""Phase 165 R6: current path must not silently recover retired Phase 49/56 replay."""
import inspect

from phase165_r52_partial_proof import ProofSearchStatus, PartialProofResult
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_r4_flask_bridge import build_group_proof_progress_view


def test_current_goal_search_has_no_phase49_or_phase56_probe_import():
    source = inspect.getsource(search_group_from_registered_goal)
    assert "build_phase49_representative_result" not in source
    assert "build_phase56_representative_result" not in source
    assert "run_inference_until_stable_with_history" not in source


def test_web_bridge_uses_registered_goal_search():
    source = inspect.getsource(build_group_proof_progress_view)
    assert "search_group_from_registered_goal" in source
    assert "build_phase49_representative_result" not in source
    assert "build_phase56_representative_result" not in source


def test_modern_search_is_typed_and_never_claims_unproved_completion(monkeypatch):
    import phase165_r55_nk_only_goal as modern
    from phase165_r52_partial_proof import make_partial_proof_result
    called = []

    def no_candidate(bridge, *, n, k):
        called.append((n, k))
        return ()

    monkeypatch.setattr(modern, "registered_group_goal_candidates", no_candidate)
    monkeypatch.setattr(modern, "build_shared_typed_bridge", lambda: object())
    result = search_group_from_registered_goal(n=2, k=1)
    assert isinstance(result, PartialProofResult)
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None
    assert result.open_goals
    assert called == [(2, 1)]
