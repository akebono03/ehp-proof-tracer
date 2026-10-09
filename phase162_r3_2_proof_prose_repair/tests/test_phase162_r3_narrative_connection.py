from dataclasses import replace

import pytest

from phase162_r2_existing_proof_connection import reconstruct_phase162_r2_from_existing_proofs
from phase162_r3_narrative_connection import render_phase162_r3_narrative
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from tests.test_phase59_pi5_3_eta3_squared import build_phase59_4_data
from tests.test_phase59_toda52_pi4_2_transport import build_phase59_2_data


def _validated_connection():
    source = build_phase59_2_data()["result_steps"][0]
    target = build_phase59_4_data()
    ehp = build_phase59_3_data()
    definitions = (target["eta3_definition_step"], target["eta4_definition_step"])
    roots = {}

    def visit(step):
        if step.rule is ProofRule.GIVEN:
            roots[id(step)] = step
        else:
            for premise in step.premises:
                visit(premise)

    for step in (source,) + definitions + ehp["premise_steps"]:
        visit(step)
    return reconstruct_phase162_r2_from_existing_proofs(
        target["expected_pi5_3_relation"],
        ehp["expected_suspension_isomorphism"].map,
        (source,),
        definitions,
        ehp["premise_steps"],
        tuple(roots.values()),
    )


def test_r3_group_goal_is_final_and_no_map_headings():
    connection = _validated_connection()
    result = render_phase162_r3_narrative(connection)
    assert result.root_step is connection.reconstruction.final_step
    assert result.ordered_steps[-1] is result.root_step
    assert "\\pi_{5}^{3}=\\mathbb{Z}/2" in result.markdown
    assert "## 単射性" not in result.markdown
    assert "## 全射性" not in result.markdown
    assert "## 結論" not in result.markdown
    assert result.markdown.count("## 証明\n") == 1


def test_r3_final_claim_is_derived_from_proof_root():
    result = render_phase162_r3_narrative(_validated_connection())
    assert result.root_step.conclusion == result.ordered_steps[-1].conclusion
    assert result.markdown.count(r"\pi_{5}^{3}=\mathbb{Z}/2") == 2
    assert "\\ker E=" in result.markdown
    assert "\\operatorname{im}E=" in result.markdown
    assert result.markdown.rstrip().endswith("□")


def test_r3_reference_section_is_preserved_verbatim():
    ref = "# Group proof narrative\n\n## 証明対象\n\nold\n\n## 使用する結果\n\n**[R1] Proposition 5.1.**\n$\\pi_6^5$\n\n## 証明\nold body\n"
    text = render_phase162_r3_narrative(_validated_connection(), ref).markdown
    assert "**[R1] Proposition 5.1.**\n$\\pi_6^5$" in text
    assert "old body" not in text


def test_r3_rejects_invalid_root_rule():
    connection = _validated_connection()
    wrong_root = replace(connection.reconstruction.final_step, rule=ProofRule.GIVEN)
    wrong_reconstruction = replace(connection.reconstruction, final_step=wrong_root)
    wrong_connection = replace(connection, reconstruction=wrong_reconstruction)
    with pytest.raises(ValueError, match="derived group-structure"):
        render_phase162_r3_narrative(wrong_connection)


def test_r3_rejects_missing_proof_premise():
    connection = _validated_connection()
    wrong_root = replace(connection.reconstruction.final_step, premises=connection.reconstruction.final_step.premises[:2])
    wrong_connection = replace(connection, reconstruction=replace(connection.reconstruction, final_step=wrong_root))
    with pytest.raises(ValueError, match="three premises"):
        render_phase162_r3_narrative(wrong_connection)


def test_r3_public_reference_adapter_uses_existing_renderer(monkeypatch):
    from phase162_r3_narrative_connection import render_phase162_r3_with_public_references
    import toda_group_proof_narrative_renderer

    calls = []

    def fake_public_renderer(presentation):
        calls.append(presentation)
        return "## 使用する結果\n\n**[R1] Proposition 5.1.**\n\n## 証明\nold body"

    monkeypatch.setattr(
        toda_group_proof_narrative_renderer,
        "render_toda_group_proof_narrative_markdown",
        fake_public_renderer,
    )
    presentation = object()
    result = render_phase162_r3_with_public_references(_validated_connection(), presentation)
    assert calls == [presentation]
    assert "**[R1] Proposition 5.1.**" in result.markdown
    assert "old body" not in result.markdown
