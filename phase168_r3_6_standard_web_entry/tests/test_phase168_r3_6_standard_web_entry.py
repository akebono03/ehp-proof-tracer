import pytest

from web_group_proof import build_standard_web_group_proof_view


def _text(view):
    return "\n".join(
        line.prefix + (line.statement_latex or "") + line.suffix
        for line in view.rendered_lines
    )


def test_r36_public_entry_model_pi42_has_two_sources():
    view = build_standard_web_group_proof_view(2, 2, citation_source="model")
    content = _text(view)
    assert view.partial_result is False
    assert content.count("**[R1] Proposition 5.1.**") == 1
    assert content.count("**[R2] (5.2).**") == 1
    assert "[R1]より" in content
    assert "[R2]を用いて" in content


def test_r36_default_pi32_preserves_long_form():
    view = build_standard_web_group_proof_view(2, 1, citation_source="legacy")
    content = _text(view)
    assert "Proposition 4.2" in content
    assert "H:" in content
    assert len(view.rendered_lines) >= 20


def test_r36_model_trace_keeps_trace_contract():
    view = build_standard_web_group_proof_view(2, 2, mode="trace", citation_source="model")
    assert view.rendered_lines == ()


def test_r36_reject_unknown_citation_source():
    with pytest.raises(ValueError, match="citation_source"):
        build_standard_web_group_proof_view(2, 2, citation_source="invented")
