"""Phase 162 R3 prose regression for the verified lower panel."""

from phase162_r3_narrative_connection import render_phase162_r3_narrative
from tests.test_phase162_r3_narrative_connection import _validated_connection


def test_r3_detailed_ehp_prose_is_preserved_without_section_headings():
    old = (
        "## 使用する結果\n\n**[R1] (5.3).**\n\n"
        "**[R2] Proposition 5.1.**\n\n"
        "## 証明\n\nEHP 完全列を考える.\n\n"
        "### 準備\n\n[R1]より, $H(\\nu')=\\eta_5$.\n\n"
        "### 単射性\n\n[R2]より, Proposition 5.1 の適用で $H$ は全射である.\n\n"
        "### 全射性\n\n[R2]より, Proposition 5.1 の適用で $\\Delta$ は単射である.\n\n"
        "### 結論\n\n旧結論.\n\n□"
    )
    result = render_phase162_r3_narrative(_validated_connection(), old)
    proof = result.markdown.split("## 証明\n", 1)[1]
    assert "[R1]より" in proof
    assert proof.count("Proposition 5.1 の適用") == 2
    assert "### 単射性" not in proof
    assert "### 全射性" not in proof
    assert "旧結論" not in proof
    assert "既存の証明規則から" not in proof
    assert "群構造移送規則" not in proof
    assert proof.rstrip().endswith("□")
    assert proof.count("□") == 1


def test_r3_standard_eta_square_and_ascii_punctuation():
    result = render_phase162_r3_narrative(_validated_connection())
    assert r"\eta_{2}^{2}" in result.markdown
    assert r"\eta_{3}^{2}" in result.markdown
    assert r"\eta_{3}\circ \eta_{4}" not in result.markdown
    assert "。" not in result.markdown
    assert "群構造移送規則" not in result.markdown
    assert "H(\\nu')" not in result.markdown or "(5.3)" in result.markdown


def test_r3_known_source_is_reference_not_duplicated_derivation():
    old = (
        "## 使用する結果\n\n**[R1] (5.3).**\n\n"
        "## 証明\n\nEHP 完全列を考える.\n\n"
        "### 単射性\n\nProposition 5.1 により $H$ は全射である.\n\n"
        "### 全射性\n\nProposition 5.1 により $\\Delta$ は単射である.\n\n"
        "### 結論\n\n旧結論."
    )
    result = render_phase162_r3_narrative(_validated_connection(), old)
    assert "**[R4] 既証明の群構造.**" in result.markdown
    assert "[R4] より" in result.markdown
    assert r"\pi_{4}^{2}=\mathbb{Z}/2" in result.markdown
