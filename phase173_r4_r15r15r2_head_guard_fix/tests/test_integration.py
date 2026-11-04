"""Real Web proof state, typed certificate, and Flask result banner regressions."""
from __future__ import annotations

from dataclasses import replace

import pytest

import web_app
from toda_calculation_result import TodaCalculationStatus
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import WebGroupProofView
from web_group_query import WebGroupQueryView


@pytest.mark.parametrize("n,k,certified", (
    (4, 3, False),
    (4, 8, True),
    (4, 31, True),
))
def test_certificate_flag_comes_from_actual_verified_partial_result(
    n: int, k: int, certified: bool,
) -> None:
    view = build_standard_web_group_proof_view(
        n=n, k=k, mode="narrative", citation_source="model",
    )
    assert view.abstract_structure_certified is certified
    if certified:
        assert view.partial_result
        assert view.key == "generic-partial-proof"
        assert any(
            line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
            for line in view.rendered_lines
        )
    else:
        assert not view.partial_result
        assert view.key == "generic-complete-proof"


def test_complete_view_cannot_be_promoted_to_abstract_only() -> None:
    view = build_standard_web_group_proof_view(
        n=4, k=4, mode="narrative", citation_source="model",
    )
    assert not view.abstract_structure_certified
    assert not view.partial_result
    with pytest.raises(ValueError, match="cannot mark a complete named proof"):
        replace(view, abstract_structure_certified=True)
    with pytest.raises(TypeError, match="abstract_structure_certified must be a bool"):
        replace(view, abstract_structure_certified="yes")


def test_real_flask_result_explains_abstract_only_status(monkeypatch) -> None:
    # Avoid repeating the distinct old group-query search. The *real* typed
    # proof search and certificate-bound Web adapter remain in this test.
    def query_not_found(n: int, k: int) -> WebGroupQueryView:
        assert (n, k) == (4, 8)
        return WebGroupQueryView(
            n=n, k=k, status=TodaCalculationStatus.NOT_FOUND,
            result_latex=None, proof_available=False,
        )

    monkeypatch.setattr(web_app, "build_standard_web_group_query_view", query_not_found)
    app = web_app.create_app()
    app.config.update(TESTING=True)
    response = app.test_client().post("/", data={"n": "4", "k": "8"})
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "A verified abstract group structure is available" in text
    assert "named-generator proof is incomplete" in text
    assert "No proof-backed result found for this query" not in text
    assert "generic-partial-proof" in text
    assert "証明済みの抽象群構造" in text


def test_no_certificate_preserves_not_found_banner(monkeypatch) -> None:
    def query_not_found(n: int, k: int) -> WebGroupQueryView:
        return WebGroupQueryView(
            n=n, k=k, status=TodaCalculationStatus.NOT_FOUND,
            result_latex=None,
        )

    partial = WebGroupProofView(
        n=5, k=8, conclusion_latex=r"\pi_{13}^{5}",
        theorem=None, phase=None, key="generic-partial-proof",
        steps=(), max_depth=2, mode="trace", partial_result=True,
    )
    monkeypatch.setattr(web_app, "build_standard_web_group_query_view", query_not_found)
    monkeypatch.setattr(
        web_app, "build_group_proof_progress_view", lambda **kwargs: partial,
    )
    app = web_app.create_app()
    app.config.update(TESTING=True)
    response = app.test_client().post("/", data={"n": "5", "k": "8"})
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "No proof-backed result found for this query" in text
    assert "A verified abstract group structure is available" not in text
    assert "generic-partial-proof" in text
