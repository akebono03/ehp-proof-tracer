"""R52-R4 targeted Flask routing and result-integrity tests."""
import pytest

from web_app import create_app
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r52_r4_flask_bridge import build_group_proof_progress_view


def test_progress_form_available_for_arbitrary_group():
    response = create_app().test_client().get("/")
    assert response.status_code == 200
    assert b'name="form_kind"' in response.data
    assert b'value="group_proof_progress"' in response.data


def test_group_progress_runs_automatic_search_outside_112(monkeypatch):
    import phase165_r52_r4_flask_bridge as bridge
    monkeypatch.setattr(bridge, "search_group_structure_automatically", lambda n, k: make_partial_proof_result(
        n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=("unresolved group structure",),
        diagnostics=("typed group statement unavailable",),
    ))
    response = create_app().test_client().post("/", data={
        "form_kind": "group_proof_progress", "n": "100", "k": "20",
    })
    assert response.status_code == 200
    assert b"search_failed" in response.data
    assert b"\\pi_{120}^{100}" in response.data
    assert b"Proof target" in response.data
    assert b"<h3>\n          Conclusion" not in response.data
    assert "□".encode("utf-8") not in response.data


def test_bad_indices_cannot_be_displayed_as_valid_targets():
    response = create_app().test_client().post("/", data={
        "form_kind": "group_proof_progress", "n": "1", "k": "0",
    })
    assert response.status_code == 200
    assert b"n must be an integer" in response.data


def test_failed_search_state_is_not_presented_as_conclusion(monkeypatch):
    import phase165_r52_r4_flask_bridge as bridge
    def failed(**kwargs):
        return make_partial_proof_result(
            n=kwargs["n"], k=kwargs["k"],
            status=ProofSearchStatus.SEARCH_FAILED,
            open_goals=("unproved",),
            diagnostics=("No registered rule",),
        )
    monkeypatch.setattr(bridge, "search_group_structure_automatically", failed)
    response = create_app().test_client().post("/", data={
        "form_kind": "group_proof_progress", "n": "17", "k": "4",
    })
    assert response.status_code == 200
    assert b"search_failed" in response.data
    assert b"No registered rule" in response.data
    assert b"Proof target" in response.data
    assert "□".encode("utf-8") not in response.data


def test_bridge_passes_genuine_search_inputs_without_creating_goal(monkeypatch):
    import phase165_r52_r4_flask_bridge as bridge
    seen = []
    def observed(**kwargs):
        seen.append(kwargs)
        return make_partial_proof_result(
            n=kwargs["n"], k=kwargs["k"],
            status=ProofSearchStatus.NOT_SEARCHED,
            open_goals=(kwargs["goal"],),
        )
    monkeypatch.setattr(bridge, "search_registered_partial_proof", observed)
    goal = object()
    provider = lambda target: ()
    result = build_group_proof_progress_view(
        n=200, k=15, goal=goal, bridge=object(),
        citing_assertion_id="registered", expansion_provider=provider,
    )
    assert result.partial_result is True
    assert result.n == 200 and result.k == 15
    assert seen[0]["goal"] is goal
    assert seen[0]["expansion_provider"] is provider


def test_existing_group_query_route_still_available():
    response = create_app().test_client().get("/")
    assert b'value="group"' in response.data
    assert b'Generator proof' in response.data
