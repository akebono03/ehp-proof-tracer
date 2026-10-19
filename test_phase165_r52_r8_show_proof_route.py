"""R52-R8 targeted regression: Show proof starts a real known/partial path."""
from types import SimpleNamespace

import pytest

import web_app
from web_app import create_app
from phase165_goal_only_search import GoalSearchIncompleteError


def _post(n, k):
    return create_app().test_client().post(
        "/",
        data={
            "form_kind": "group_proof",
            "n": str(n),
            "k": str(k),
            "group_proof_depth": "2",
            "group_proof_mode": "narrative",
        },
    )


def test_r8_unconfigured_proof_calls_partial_search(monkeypatch):
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    called = []

    def partial(**kwargs):
        called.append(kwargs)
        return build_partial_web_group_proof_view(
            make_partial_proof_result(
                n=kwargs["n"], k=kwargs["k"],
                status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=("missing proof",),
                diagnostics=("Typed goal has no registered derivation",),
            ), max_depth=kwargs["max_depth"],
        )

    monkeypatch.setattr(web_app, "build_group_proof_progress_view", partial)
    response = _post(3, 1)
    assert response.status_code == 200
    assert called == [{"n": 3, "k": 1, "max_depth": 2}]
    assert "証明未完成".encode("utf-8") in response.data


def test_r8_registered_proof_does_not_fall_back(monkeypatch):
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    calls = []
    def registered(**kwargs):
        calls.append(kwargs)
        return build_partial_web_group_proof_view(
            make_partial_proof_result(
                n=kwargs["n"], k=kwargs["k"],
                status=ProofSearchStatus.SEARCH_FAILED,
                diagnostics=("Registered proof test fixture",),
            ), max_depth=kwargs["max_depth"],
        )
    monkeypatch.setattr(web_app, "build_group_proof_progress_view", registered)
    assert _post(2, 1).status_code == 200
    assert calls == [{"n": 2, "k": 1, "max_depth": 2}]


def test_r8_actual_pi32_registered_narrative_unchanged():
    from web_group_proof import build_standard_web_group_proof_view
    view = build_standard_web_group_proof_view(
        2, 1, max_depth=2, mode="narrative"
    )
    assert view.phase.startswith("165")
    body = "\n".join(
        line.prefix + " " + " ".join(
            segment.value for segment in line.segments
        ) for line in view.rendered_lines
    )
    assert "証明対象" in body
    assert "使用する結果" in body
    assert "証明" in body
