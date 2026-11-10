"""Small, reproducible test fixtures for the HTML contract only."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from phase174_r3_r7_r54_public_http_narrative_audit.audit import (
    ProofHTMLParser, observe_response,
)


@dataclass
class FakeResponse:
    status_code: int
    data: bytes


def fixture_response(*, key: str = "generic-complete-proof", conclusion: str = r"\pi_{12}^{7}=0", duplicated: bool = False) -> FakeResponse:
    extra = " の群構造を決定するために" if duplicated else ""
    html = (
        "<html><body><h3>Conclusion</h3>"
        '<div id="group-proof-conclusion" data-latex="' + conclusion + '">result</div>'
        "<p>" + key + "</p>"
        '<div id="group-proof-rendered-lines" data-proof-mode="narrative">'
        "<h4>証明</h4><div><span>Proposition 2.7</span>"
        "<span>Proposition 4.2</span><span>(5.10)</span>"
        "<span>の群構造を決定するために</span>"
        "<span>" + extra + "</span>"
        '<span data-latex="\\pi_{12}^{13}=0">tex</span>'
        "<span>以上より</span><span>□</span></div></div></body></html>"
    )
    return FakeResponse(200, html.encode("utf-8"))


def test_html_parser_recovers_one_conclusion_and_section() -> None:
    parser = ProofHTMLParser()
    parser.feed(fixture_response().data.decode("utf-8"))
    assert parser.verified_section()
    assert parser.conclusion_latex == r"\pi_{12}^{7}=0"
    assert parser.proof_mode == "narrative"
    assert "Proposition 2.7" in parser.proof_fragments


def test_complete_html_contract_and_duplicate_reporting() -> None:
    outcome = observe_response(fixture_response(duplicated=True), form_kind="group")
    assert outcome["verified_conclusion"] is True
    assert outcome["duplicate_intro_observed"] is True
    assert outcome["repeated_intro_count"] == 2
    assert outcome["browser_katex_checked"] is False


def test_partial_proof_not_accepted_as_verified_completion() -> None:
    with pytest.raises(RuntimeError):
        observe_response(fixture_response(key="generic-partial-proof"), form_kind="group")


def test_wrong_conclusion_or_http_status_rejected() -> None:
    with pytest.raises(RuntimeError):
        observe_response(fixture_response(conclusion=r"\pi_{13}^{7}=0"), form_kind="group")
    page = fixture_response()
    page.status_code = 500
    with pytest.raises(RuntimeError):
        observe_response(page, form_kind="group")
