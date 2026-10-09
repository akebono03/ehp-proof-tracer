"""Focused, read-only renderer integration checks for the Phase162 proof tree."""

from proof import ProofRule, ProofStep
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from tests.test_phase59_toda52_pi4_2_transport import build_phase59_2_data
from toda_rules import toda_eta_family_definition_statement
from phase162_pi5_3_renderer_audit import render_phase162_pi5_3_reconstructed_proof


def _inputs():
    pi4_2_step = build_phase59_2_data()["result_steps"][0]
    definitions = tuple(
        ProofStep(
            conclusion=toda_eta_family_definition_statement(index),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for index in (3, 4)
    )
    ehp_leaves = build_phase59_3_data()["premise_steps"]
    return pi4_2_step, definitions, ehp_leaves


def test_renderer_receives_reconstructed_pi5_3_root():
    result = render_phase162_pi5_3_reconstructed_proof(*_inputs())
    assert result.presentation.root_step is result.final_step
    assert result.presentation.source_entry.step is result.final_step
    assert result.final_step.rule is ProofRule.INFERENCE
    assert len(result.final_step.premises) == 3
    assert any(
        node.proof_step is result.final_step for node in result.presentation.nodes
    )


def test_existing_renderer_returns_nonempty_markdown():
    result = render_phase162_pi5_3_reconstructed_proof(*_inputs())
    assert isinstance(result.markdown, str)
    assert result.markdown.strip()
    assert result.presentation.edges
