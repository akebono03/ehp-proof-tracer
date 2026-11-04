"""Fast, standalone tests for the actual HTML container parser."""
from __future__ import annotations

import pytest

from phase173_r4_r15r17r3r5_public_http_gate.html_probe import (
    parse_narrative_html,
)


def test_reads_only_proof_area_and_nested_math() -> None:
    document = (
        '<h4>outside</h4>'
        '<div id="group-proof-rendered-lines">'
        '<h4>使用する結果</h4>'
        '<div class="group-proof-rendered-line">'
        '<span data-latex="\\pi_{12}^{4}">\\pi_{12}^{4}</span>'
        '</div>'
        '<h4>未解決 Goal</h4>'
        '</div>'
        '<h4>outside again</h4>'
    )
    result = parse_narrative_html(document)
    assert result.found
    assert result.headings == ("使用する結果", "未解決 Goal")
    assert result.math_latex == (r"\pi_{12}^{4}",)
    assert r"\pi_{12}^{4}" in result.visible_text
    assert "outside" not in result.visible_text


def test_missing_rendered_container_is_not_invented() -> None:
    result = parse_narrative_html("<h4>使用する結果</h4>")
    assert not result.found
    assert result.headings == ()
    assert result.math_latex == ()
    assert result.visible_text == ""


def test_duplicate_rendered_container_is_rejected() -> None:
    markup = (
        '<div id="group-proof-rendered-lines"></div>'
        '<div id="group-proof-rendered-lines"></div>'
    )
    with pytest.raises(ValueError, match="duplicate rendered Narrative containers"):
        parse_narrative_html(markup)


def test_malformed_rendered_container_is_rejected() -> None:
    with pytest.raises(ValueError, match="incomplete Narrative HTML container"):
        parse_narrative_html('<div id="group-proof-rendered-lines"><div>')
