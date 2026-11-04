"""Real Flask HTML (with real typed proof search) after unified Narrative work.

Only the unrelated group-structure query is stubbed to NOT_FOUND, matching the
existing Flask banner regression. The group proof search, Model, Renderer, Web
adapter and Jinja template are never mocked.
"""
from __future__ import annotations

import json

import pytest

import web_app
from phase173_r4_r15r17r3r5_public_http_gate.html_probe import (
    parse_narrative_html,
)
from toda_calculation_result import TodaCalculationStatus
from web_group_query import WebGroupQueryView


@pytest.mark.parametrize(
    "n,k,has_certificate,named_complete,pending_count",
    (
        (4, 8, True, False, 3),
        (4, 9, True, False, 2),
        (5, 3, False, False, 3),
        (4, 4, False, True, 0),
    ),
)
def test_real_flask_html_preserves_unified_narrative_contract(
    monkeypatch: pytest.MonkeyPatch,
    n: int,
    k: int,
    has_certificate: bool,
    named_complete: bool,
    pending_count: int,
) -> None:
    # The group query database is a separate route. Avoid invoking it twice.
    # Unlike that query, the proof search remains real and source-verified.
    def unrelated_query_not_found(n: int, k: int) -> WebGroupQueryView:
        return WebGroupQueryView(
            n=n,
            k=k,
            status=TodaCalculationStatus.NOT_FOUND,
            result_latex=None,
            proof_available=False,
        )

    monkeypatch.setattr(
        web_app, "build_standard_web_group_query_view", unrelated_query_not_found,
    )
    app = web_app.create_app()
    app.config.update(TESTING=True)
    response = app.test_client().post(
        "/",
        data={"form_kind": "group", "n": str(n), "k": str(k)},
    )
    assert response.status_code == 200
    document = response.get_data(as_text=True)
    narrative = parse_narrative_html(document)
    assert narrative.found
    assert narrative.headings.count("使用する結果") == 1
    assert "検証済みの途中経過" not in narrative.headings
    assert "検証済み証明木の Reference" not in narrative.headings
    assert "証明済みの抽象群構造" not in narrative.headings
    assert "Relation(lhs=" not in narrative.visible_text
    assert "数式表示未対応" not in narrative.visible_text

    if named_complete:
        assert "generic-complete-proof" in document
        assert "Typed proof search completed" in document
        assert "未解決 Goal" not in narrative.headings
        assert "探索診断" not in narrative.headings
        assert "確認済み ProofStep（与件を含む）" not in narrative.headings
        assert "[R" in narrative.visible_text
    else:
        assert "generic-partial-proof" in document
        assert "未解決 Goal" in narrative.headings
        assert narrative.headings.count("未解決 Goal") == 1
        assert "探索診断" in narrative.headings
        assert f"未解決 Goal {pending_count} 件" in narrative.visible_text
        assert "未解決 Goal は証明済みの結論ではありません" in narrative.visible_text
        if has_certificate:
            assert "A verified abstract group structure is available" in document
            assert "named-generator proof is incomplete" in document
            assert "確認済み ProofStep（与件を含む）" in narrative.headings
            assert "Proposition 4.4" in narrative.visible_text
            assert "Lemma 5.4" in narrative.visible_text
            assert any(r"\cong" in latex for latex in narrative.math_latex)
        else:
            assert "No proof-backed result found for this query" in document
            assert "確認済み ProofStep（与件を含む）" not in narrative.headings
            assert "Proposition 4.4" not in narrative.visible_text
            assert "参照情報を持つ ProofStep はありません" in narrative.visible_text
    print("R15R17R3R5_HTTP_CASE=" + json.dumps({
        "n": n,
        "k": k,
        "http": response.status_code,
        "named_complete": named_complete,
        "abstract_certificate": has_certificate,
        "headings": narrative.headings,
        "expected_internal_pending_count": pending_count,
        "single_reference_section": narrative.headings.count("使用する結果") == 1,
        "model_sidecar_absent": "検証済みの途中経過" not in narrative.headings,
    }, ensure_ascii=False, sort_keys=True))
