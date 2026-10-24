def test_web_heading_without_segments_is_included_in_capture():
    """Heading text belongs to prefix, unlike segmented ordinary lines."""
    from types import SimpleNamespace
    from web_group_proof_common import WebGroupProofRenderedLineView

    heading = WebGroupProofRenderedLineView(
        kind="heading", indent_level=0, prefix="探索診断",
        statement_latex=None, suffix="",
    )
    ordinary = WebGroupProofRenderedLineView(
        kind="text", indent_level=0, prefix="- No applicable typed rule",
        statement_latex=None, suffix="",
    )
    view = SimpleNamespace(rendered_lines=(heading, ordinary))
    assert _text(view) == "探索診断\n- No applicable typed rule"
