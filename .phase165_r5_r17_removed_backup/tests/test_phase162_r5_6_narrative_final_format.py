"""Focused Phase 162 Web presentation formatting contracts."""

from phase162_web_narrative_integration import (
    _compose_phase162_group_conclusion,
    _format_phase162_proof_sentences,
    build_phase162_web_validated_isomorphism_markdown,
)


def test_phase162_web_proof_has_ehp_sequence_and_group_conclusion():
    markdown = build_phase162_web_validated_isomorphism_markdown()
    proof = markdown.split("## 証明", 1)[1]
    assert "EHP 完全列を考える." in proof
    assert r"\pi_{6}^{3}\xrightarrow{H}\pi_{6}^{5}" in proof
    assert r"\xrightarrow{\Delta}\pi_{4}^{2}" in proof
    assert r"\xrightarrow{E}\pi_{5}^{3}" in proof
    assert r"\xrightarrow{H}\pi_{5}^{5}" in proof
    assert r"\xrightarrow{\Delta}\pi_{3}^{2}" in proof
    assert r"\pi_{4}^{2}=\mathbb{Z}/2\{\eta_{2}^{2}\}" in proof
    assert r"E(\eta_{2}^{2})=\eta_{3}^{2}" in proof
    assert r"\pi_{5}^{3}=\mathbb{Z}/2\{\eta_{3}^{2}\}" in proof
    assert proof.rstrip().endswith("□")
    assert r"E: \pi_{4}^{2} \to \pi_{5}^{3}" in proof


def test_phase162_web_prose_uses_ascii_punctuation_and_one_sentence_per_paragraph():
    sample = (
        "## 使用する結果\n\n[R1] (5.3).\n\n"
        "## 証明\n\n"
        "### 単射性\n\n"
        "[R1]より、第一文である。第二文である。\n\n"
        "### 結論\n\n$E: A \\to B$ は同型である。\n\n□\n"
    )
    actual = _format_phase162_proof_sentences(sample)
    assert "[R1] (5.3)." in actual
    assert "[R1]より, 第一文である.\n\n第二文である." in actual
    assert "$E: A \\to B$ は同型である." in actual
    body = actual.split("## 証明", 1)[1]
    assert "。" not in body
    assert "、" not in body


def test_phase162_group_conclusion_only_changes_validated_web_markdown():
    original = (
        "# Backward proof narrative\n\n"
        "## 使用する結果\n\n[R1] (5.3).\n\n"
        "## 証明\n\n### 結論\n\n"
        "$E: \\pi_{4}^{2} \\to \\pi_{5}^{3}$ は同型写像である.\n\n□\n"
    )
    composed = _compose_phase162_group_conclusion(original)
    assert composed.count("EHP 完全列を考える.") == 1
    assert composed.count(r"\pi_{5}^{3}=\mathbb{Z}/2\{\eta_{3}^{2}\}") == 1
    assert "[R1] (5.3)." in composed
    assert "同型写像である." in composed
    assert _compose_phase162_group_conclusion("## 証明\n\n□\n") == "## 証明\n\n□\n"
