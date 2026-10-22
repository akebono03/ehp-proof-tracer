from pathlib import Path
from web_group_proof import build_standard_web_group_proof_view


def _rows(n):
    view = build_standard_web_group_proof_view(n, 1, max_depth=2, mode="narrative")
    return [(line.prefix, line.statement_latex or "", line.suffix) for line in view.rendered_lines]


def test_r410_both_toda51_consequences_cited():
    rows = _rows(3)
    headings = [prefix for prefix, _, _ in rows if "(5.1)" in prefix]
    assert len(headings) == 1, headings
    assert "[R1]" in headings[0]
    for latex in (
        r"\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}",
        r"\pi_{4}^{5} = 0",
    ):
        results = [(prefix, math) for prefix, math, _ in rows if math == latex]
        assert len(results) == 1, (latex, results)
        assert results[0][0].replace(" ", "") == "[R1]より,", results


def test_r410_pi32_still_cited():
    rows = _rows(2)
    assert any(math == r"\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}" for _, math, _ in rows)


def test_r410_no_specialization_name_or_math_recheck():
    source = Path("toda_group_proof_narrative_contribution_renderer.py").read_text(encoding="utf-8-sig")
    start = source.index("def link_toda_group_proof_narrative_reference_body_consumers(")
    end = source.index("\ndef ", start + 5)
    code = source[start:end]
    assert "specialize_typed_statement(" not in code
    assert "len(consumers) != 1" not in code
    assert "for index, derived_line in consumers:" in code
