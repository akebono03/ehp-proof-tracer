"""Focused R54 regressions for explicit group-structure Web goals."""
from types import SimpleNamespace

import pytest

import phase165_r54_explicit_web_goal as goal_web
from homotopy_groups import FreeCyclicGroup
from phase165_r54_explicit_web_goal import parse_explicit_free_cyclic_eta_goal


def test_r54_eta_goal_is_a_typed_free_cyclic_claim():
    target = parse_explicit_free_cyclic_eta_goal(n=2, k=1, generator="eta_2")
    assert isinstance(target, FreeCyclicGroup)
    assert target.generator.generator.family == "η"
    assert target.generator.generator.index == 2


def test_r54_rejects_generator_dimension_mismatch():
    with pytest.raises(ValueError, match="require k=1"):
        parse_explicit_free_cyclic_eta_goal(n=3, k=2, generator="eta_3")
    with pytest.raises(ValueError, match="require k=1"):
        parse_explicit_free_cyclic_eta_goal(n=3, k=1, generator="eta_2")


def test_r54_web_adapter_uses_actual_shared_search(monkeypatch):
    captured = []
    expected = object()
    monkeypatch.setattr(goal_web, "search_shared_group_goal", lambda **kw: (captured.append(kw), expected)[1])
    monkeypatch.setattr(goal_web, "build_partial_web_group_proof_view", lambda value, **kw: (value, kw))
    result = goal_web.build_explicit_free_cyclic_eta_web_view(
        n=2, k=1, generator="eta_2", max_depth=2, mode="narrative"
    )
    assert result == (expected, {"max_depth": 2, "mode": "narrative"})
    assert captured[0]["n"] == 2 and captured[0]["k"] == 1
    assert captured[0]["group_structure"].generator.generator.index == 2


def test_r54_flask_explicit_goal_form(monkeypatch):
    import web_app
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

    observed = []
    def fake_explicit(**kwargs):
        observed.append(kwargs)
        return build_partial_web_group_proof_view(make_partial_proof_result(
            n=kwargs["n"], k=kwargs["k"], status=ProofSearchStatus.SEARCH_FAILED,
            diagnostics=("test search exercised",), open_goals=("unproved",),
        ))
    monkeypatch.setattr(web_app, "build_explicit_free_cyclic_eta_web_view", fake_explicit)
    response = web_app.create_app().test_client().post("/", data={
        "form_kind": "explicit_group_proof", "n": "2", "k": "1", "goal_generator": "eta_2",
        "group_proof_depth": "2", "group_proof_mode": "narrative",
    })
    assert response.status_code == 200
    assert observed == [{"n": 2, "k": 1, "generator": "eta_2", "max_depth": 2, "mode": "narrative"}]
    assert "test search exercised".encode("utf-8") in response.data
