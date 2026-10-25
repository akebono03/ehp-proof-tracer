"""Phase 167 general references against the current common Renderer output."""
from web_group_proof import build_standard_web_group_proof_view


def _reference_text(n: int, k: int) -> str:
    view = build_standard_web_group_proof_view(n, k, 2, "narrative")
    assert view.key == "generic-complete-proof"
    lines = view.rendered_lines

    def is_section(line, title):
        return (line.kind in ("text", "heading")
                and line.prefix == title and line.statement_latex is None
                and line.suffix == "")

    first = next(i for i, line in enumerate(lines)
                 if is_section(line, "使用する結果"))
    last = next(i for i, line in enumerate(lines)
                if i > first and is_section(line, "証明"))
    assert first < last
    return "\n".join(
        " ".join((line.prefix, line.statement_latex or "", line.suffix))
        for line in lines[first + 1:last]
    )


def test_phase167_r2_pi32_reference_uses_general_form():
    text = _reference_text(2, 1)
    assert r"\pi_i^1=0" in text
    assert r"\pi_{n}^{n}" in text
    assert r"\pi_{3}^{3}" not in text
    assert r"\pi_{2}^{1}" not in text
    assert "Proposition 5.1" in text


def test_phase167_r2_pi43_reference_uses_general_form():
    text = _reference_text(3, 1)
    assert r"\pi_{n}^{n}" in text
    assert r"\pi_i^n=0" in text
    assert text.count(r"\pi_{n}^{n}") == 1
    assert "Proposition 5.1" in text
