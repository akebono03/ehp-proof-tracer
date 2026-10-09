from phase162_r3_narrative_connection import (
    _phase162_web_display_math_delimiters,
)
from web_group_proof import _build_group_proof_rendered_lines


def test_r3_web_display_math_is_parsed_as_math():
    source = (
        "# Group proof narrative\n\n## 証明\n\n"
        "ゆえに\n\n$$\n"
        r"E:\pi_{4}^{2}\xrightarrow{\cong}\pi_{5}^{3}"
        "\n$$\n\n"
        "以上より\n\n$$\n"
        r"\pi_{5}^{3}=\mathbb{Z}/2\{\eta_{3}^{2}\}"
        "\n$$\n\n□\n"
    )
    fixed = _phase162_web_display_math_delimiters(source)
    assert "$$" not in fixed
    assert fixed.count(r"\[") == 2
    assert fixed.count(r"\]") == 2
    lines = _build_group_proof_rendered_lines(fixed)
    math = [
        segment.value
        for line in lines
        for segment in line.segments
        if segment.kind == "display_math"
    ]
    assert len(math) == 2
    assert math[0] == r"E:\pi_{4}^{2}\xrightarrow{\cong}\pi_{5}^{3}"
    assert math[1] == r"\pi_{5}^{3}=\mathbb{Z}/2\{\eta_{3}^{2}\}"


def test_r3_inline_math_and_reference_punctuation_unchanged():
    source = (
        "**[R1] Proposition 5.1.**\n"
        r"$\Delta(\iota_5)=\pm2\eta_2$."
        "\n\n$$\n"
        r"\pi_{5}^{3}=\mathbb{Z}/2\{\eta_{3}^{2}\}"
        "\n$$\n"
    )
    fixed = _phase162_web_display_math_delimiters(source)
    assert "**[R1] Proposition 5.1.**" in fixed
    assert r"$\Delta(\iota_5)=\pm2\eta_2$." in fixed
    assert r"\pi_{5}^{3}=\mathbb{Z}/2\{\eta_{3}^{2}\}" in fixed


def test_r3_web_display_math_rejects_unclosed_block():
    import pytest
    with pytest.raises(ValueError, match="Unterminated"):
        _phase162_web_display_math_delimiters("## 証明\n\n$$\nE\n")
