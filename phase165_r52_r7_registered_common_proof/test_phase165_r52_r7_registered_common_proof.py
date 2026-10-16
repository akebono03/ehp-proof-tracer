"""Focused regression tests for the common-only proof replay entrance."""
from pathlib import Path
from types import SimpleNamespace

import pytest

from homotopy_groups import TodaPrimaryGroup
from phase165_goal_only_search import GoalSearchIncompleteError
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r7_registered_common_proof import build_registered_common_replay


def _fake_group_result():
    return SimpleNamespace(
        target=TodaPrimaryGroup(3, 2),
        group_structure=object(),
        source_entry=SimpleNamespace(),
    )


def test_retired_provider_symbols_absent():
    import phase165_r52_r7_registered_common_proof as module
    assert not hasattr(module, "RegisteredProofProvider")
    assert not hasattr(module, "registered_proof_providers")
    source = Path(module.__file__).read_text(encoding="utf-8-sig")
    assert "reconstruct_registered_pi32" not in source
    assert "pi32_goal" not in source


def test_common_search_receives_input_goal_and_rejects_incomplete(monkeypatch):
    import phase165_r52_r9_shared_math as shared
    seen = []

    def fake_search(**kwargs):
        seen.append(kwargs)
        return SimpleNamespace(status=ProofSearchStatus.SEARCH_FAILED,
                               diagnostics=("unknown typed goal",))

    monkeypatch.setattr(shared, "search_shared_group_goal", fake_search)
    with pytest.raises(GoalSearchIncompleteError, match="unknown typed goal"):
        build_registered_common_replay(
            group_result=_fake_group_result(), max_depth=1, mode="trace"
        )
    assert len(seen) == 1
    assert seen[0]["n"] == 2
    assert seen[0]["k"] == 1
    assert seen[0]["group_structure"] is not None


def test_invalid_depth_and_mode_rejected_without_search(monkeypatch):
    import phase165_r52_r9_shared_math as shared

    def forbidden_search(**kwargs):
        raise AssertionError("search should not execute for invalid arguments")

    monkeypatch.setattr(shared, "search_shared_group_goal", forbidden_search)
    for depth in (True, -1, "2"):
        with pytest.raises(ValueError):
            build_registered_common_replay(
                group_result=_fake_group_result(), max_depth=depth, mode="trace"
            )
    with pytest.raises(ValueError):
        build_registered_common_replay(
            group_result=_fake_group_result(), max_depth=1, mode="invalid"
        )


def test_no_legacy_provider_parameter():
    import inspect
    parameters = inspect.signature(build_registered_common_replay).parameters
    assert "providers" not in parameters
