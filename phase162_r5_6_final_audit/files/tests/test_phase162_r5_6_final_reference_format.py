"""Phase 162 R5-6: ensure (4.5) LaTeX macro boundaries are valid."""

from toda_general_reference_schema import render_general_reference_statement_lines


def test_phase162_r5_6_45_condition_spacing():
    lines = render_general_reference_statement_lines("(4.5)")
    assert lines is not None
    assert len(lines) == 1
    assert r"n\ge k+2,\quad m\ge n" in lines[0]
    assert r"\quadm" not in lines[0]
    assert r"E^{m-n}:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{m+k}^{m}" in lines[0]
