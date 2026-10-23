from web_group_proof import build_standard_web_group_proof_view


def _text(view):
    return "\n".join(
        line.prefix + (line.statement_latex or "") + line.suffix
        for line in view.rendered_lines
    )


def test_r319_default_web_uses_model_for_pi42():
    default = build_standard_web_group_proof_view(2, 2)
    explicit = build_standard_web_group_proof_view(2, 2, citation_source="model")
    assert default.rendered_lines == explicit.rendered_lines
    content = _text(default)
    assert "**[R1] Proposition 5.1.**" in content
    assert "**[R2] (5.2).**" in content


def test_r319_legacy_remains_explicitly_available_for_pi32():
    view = build_standard_web_group_proof_view(2, 1, citation_source="legacy")
    content = _text(view)
    assert "Proposition 4.2" in content
    assert "H:" in content
    assert len(view.rendered_lines) >= 20


def test_r319_default_trace_contract():
    view = build_standard_web_group_proof_view(2, 2, mode="trace")
    assert view.rendered_lines == ()
