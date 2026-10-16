"""Focused tests of the shadowed module and the goal-only common entry."""
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase165_goal_only_search import GoalSearchIncompleteError
from phase165_r52_partial_proof import ProofSearchStatus


def test_two_sources_both_retired():
    from phase165_r6_1_module_shadow_fix.apply import ROOT_MODULE, PACKAGE_MODULE, inspect_module
    for path in (ROOT_MODULE, PACKAGE_MODULE):
        info = inspect_module(path)
        assert "RegisteredProofProvider" not in info["names"]
        assert "registered_proof_providers" not in info["names"]
        assert "providers" not in info["kwonlyargs"]


def test_imported_module_is_retired():
    import phase165_r52_r7_registered_common_proof as module
    assert not hasattr(module, "RegisteredProofProvider")
    assert not hasattr(module, "registered_proof_providers")


def test_common_search_receives_user_goal(monkeypatch):
    import phase165_r52_r9_shared_math as shared
    from phase165_r52_r7_registered_common_proof import build_registered_common_replay
    seen = []
    def fake_search(**kwargs):
        seen.append(kwargs)
        return SimpleNamespace(status=ProofSearchStatus.SEARCH_FAILED,
                               diagnostics=("unknown typed goal",))
    monkeypatch.setattr(shared, "search_shared_group_goal", fake_search)
    target = SimpleNamespace(group_dimension=3, sphere_dimension=2)
    group = SimpleNamespace(target=target, group_structure=object())
    with pytest.raises(GoalSearchIncompleteError, match="unknown typed goal"):
        build_registered_common_replay(group_result=group, max_depth=2, mode="narrative")
    assert len(seen) == 1
    assert seen[0]["n"] == 2 and seen[0]["k"] == 1
    assert seen[0]["group_structure"] is group.group_structure


def test_invalid_options_refused():
    from phase165_r52_r7_registered_common_proof import build_registered_common_replay
    for depth in (-1, True, "2"):
        with pytest.raises(ValueError):
            build_registered_common_replay(group_result=object(), max_depth=depth, mode="narrative")
    with pytest.raises(ValueError):
        build_registered_common_replay(group_result=object(), max_depth=2, mode="invalid")
