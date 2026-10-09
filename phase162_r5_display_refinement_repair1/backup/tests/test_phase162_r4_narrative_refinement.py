"""Phase 162 R4: semantic duplication and justified exactness prose."""

from phase162_validated_proof_presentation import (
    _validated_proof_body_lines,
    _render_validated_reference_section,
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from proof import ProofRule, Relation, RelationType
from tests.test_phase162_r2_validated_proof_presentation import _validated_fixture
from toda_rules import (
    TodaProp42ExactnessStatement,
    TodaSuspensionInjectiveStatement,
    TodaSuspensionSurjectiveStatement,
)


def test_phase162_r4_no_duplicate_semantic_conclusion_or_tautology():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    _, fixed_ids = _render_validated_reference_section(presentation)
    previous = []
    expected_lines = []
    for step in presentation.nodes:
        if step.rule is ProofRule.GIVEN or id(step) in fixed_ids:
            continue
        conclusion = step.conclusion
        if (
            isinstance(conclusion, Relation)
            and conclusion.relation_type is RelationType.EQUALITY
            and conclusion.lhs == conclusion.rhs
        ):
            continue
        if any(conclusion == item for item in previous):
            continue
        previous.append(conclusion)
        expected_lines.append(step)
    actual_lines = _validated_proof_body_lines(presentation, fixed_ids)
    assert len(actual_lines) == len(expected_lines)
    assert len(previous) == len(actual_lines)


def test_phase162_r4_exactness_connector_only_when_premise_is_exactness():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    _, fixed_ids = _render_validated_reference_section(presentation)
    lines = _validated_proof_body_lines(presentation, fixed_ids)
    expected_count = sum(
        1 for step in presentation.nodes
        if step.rule is ProofRule.INFERENCE and id(step) not in fixed_ids
        and isinstance(
            step.conclusion,
            (TodaSuspensionInjectiveStatement, TodaSuspensionSurjectiveStatement),
        )
        and any(
            isinstance(p.conclusion, TodaProp42ExactnessStatement)
            for p in step.premises
        )
    )
    assert sum(line.startswith("完全性より、") for line in lines) <= expected_count
    assert all("完全性より、これより" not in line for line in lines)


def test_phase162_r4_preserves_verified_root_and_reference_boundary():
    validated = _validated_fixture()
    presentation = build_validated_backward_proof_presentation(validated)
    text = render_validated_backward_proof_markdown(presentation)
    assert presentation.root_step is validated.reconstruction.final_step
    assert "## 使用する結果" in text
    assert "---\n\n## 証明" in text
    assert r"E: \pi_{4}^{2} \to \pi_{5}^{3}" in text
    assert text.rstrip().endswith("□")
