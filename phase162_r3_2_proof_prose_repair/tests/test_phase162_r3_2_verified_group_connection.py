"""Phase 162 R3-2: Web lower-panel integration tests."""

from phase162_web_narrative_integration import (
    _build_phase162_existing_group_connection,
    build_phase162_web_validated_isomorphism_markdown,
)
from phase162_r3_narrative_connection import render_phase162_r3_narrative
from proof import ProofRule


def test_r3_2_uses_a_derived_group_goal():
    result = _build_phase162_existing_group_connection()
    assert result.reconstruction.final_step.rule is ProofRule.INFERENCE
    assert result.reconstruction.final_step.conclusion == result.reconstruction.goal
    assert len(result.reconstruction.derived_steps) == 8
    assert result.provenance.verified_inferences >= 9


def test_r3_2_uses_r3_group_narrative():
    connection = _build_phase162_existing_group_connection()
    rendered = render_phase162_r3_narrative(connection)
    assert rendered.root_step is connection.reconstruction.final_step
    assert r"\pi_{5}^{3}=\mathbb{Z}/2" in rendered.markdown
    assert "### 単射性" not in rendered.markdown
    assert "### 全射性" not in rendered.markdown


def test_r3_2_web_output_uses_group_root_without_old_headings():
    text = build_phase162_web_validated_isomorphism_markdown()
    assert "## 証明対象" in text
    assert r"\pi_{5}^{3}=\mathbb{Z}/2" in text
    assert "### 準備" not in text
    assert "### 単射性" not in text
    assert "### 全射性" not in text
    assert "### 結論" not in text
    assert "群構造移送規則" not in text
    assert text.count("## 証明\n") == 1


def test_r3_2_web_keeps_legacy_references_for_next_audit():
    text = build_phase162_web_validated_isomorphism_markdown()
    assert "## 使用する結果" in text
    assert "## 証明" in text
    assert text.rstrip().endswith("□")
    assert text.count("□") == 1
    assert "Proposition 5.1" in text
    assert r"\eta_{3}^{2}" in text


def test_r3_2_only_lower_panel_label_is_changed():
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    text = (root / "web_group_proof.py").read_text(encoding="utf-8-sig")
    assert "## 群構造の検証済み証明" in text
    assert "build_phase162_web_validated_isomorphism_markdown" in text


def test_r3_2_generator_is_derived_from_eta_bridge():
    from expression import Composition, Suspension
    from proof import Relation, RelationType

    connection = _build_phase162_existing_group_connection()
    source = connection.source_structure_step.conclusion.rhs.generator
    image = connection.generator_image_step.conclusion
    target = connection.reconstruction.goal.rhs.generator
    assert isinstance(image, Relation)
    assert image.relation_type is RelationType.EQUALITY
    assert image.lhs == Suspension(expression=source)
    assert isinstance(target, Composition)
    assert image.rhs == target
    assert connection.generator_image_step.rule is ProofRule.INFERENCE
