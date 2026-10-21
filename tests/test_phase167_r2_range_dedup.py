from web_group_proof import build_standard_web_group_proof_view


def _reference_text(n: int, k: int) -> str:
    view = build_standard_web_group_proof_view(n, k, 2, "narrative")
    assert view.key == "generic-complete-proof"
    lines = view.rendered_lines
    first = next(
        i for i, line in enumerate(lines)
        if line.kind == "heading" and line.prefix == "使用する結果"
    )
    last = next(
        i for i, line in enumerate(lines)
        if i > first and line.kind == "heading" and line.prefix == "証明"
    )
    return "\n".join(
        " ".join((line.prefix, line.statement_latex or "", line.suffix))
        for line in lines[first + 1:last]
    )


def test_phase167_r2_pi32_diagonal_range_once():
    reference = _reference_text(2, 1)
    diagonal = next(line for line in reference.splitlines() if r"\pi_{n}^{n}" in line)
    assert diagonal.count(r"n \ge 1") == 1
    assert reference.count(r"\pi_{n}^{n}") == 1
    assert r"\pi_{i}^{1}" in reference
    assert "Proposition 5.1" in reference


def test_phase167_r2_pi43_diagonal_range_once():
    reference = _reference_text(3, 1)
    diagonal = next(line for line in reference.splitlines() if r"\pi_{n}^{n}" in line)
    assert diagonal.count(r"n \ge 1") == 1
    assert reference.count(r"\pi_{n}^{n}") == 1
    assert r"\pi_{i}^{n}" in reference
    assert "Proposition 5.1" in reference
