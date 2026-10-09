from toda_group_proof_narrative_contribution_renderer import (
    normalize_toda_group_proof_narrative_connectors,
)


def test_r7_collapses_repeated_connector_and_preserves_math():
    original = r"これより, これより, $E:\pi_4^2\to\pi_5^3$ は同型."
    rendered = normalize_toda_group_proof_narrative_connectors(original)
    assert rendered == r"これより, $E:\pi_4^2\to\pi_5^3$ は同型."


def test_r7_preserves_different_connectors_and_references():
    original = "したがって, これより, [R2] の適用である."
    assert normalize_toda_group_proof_narrative_connectors(original) == original


def test_r7_joins_standalone_connector_without_duplicate():
    original = "これより,\n\nこれより, $H$ は全射."
    assert normalize_toda_group_proof_narrative_connectors(original) == "これより, $H$ は全射."


def test_r7_does_not_touch_math_or_exactness_reason():
    original = "これより,\n\n完全性より, $E$ は単射."
    assert normalize_toda_group_proof_narrative_connectors(original) == "完全性より, $E$ は単射."


def test_r7_pi5_3_public_narrative_connector_regression():
    from phase162_pi5_3_renderer_audit import render_phase162_pi5_3_reconstructed_proof
    from tests.test_phase59_pi5_3_eta3_squared import build_phase59_4_data
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data

    data = build_phase59_4_data()
    leaves = build_phase59_3_data()['premise_steps']
    result = render_phase162_pi5_3_reconstructed_proof(
        data['pi4_2_step'],
        (data['eta3_definition_step'], data['eta4_definition_step']),
        leaves,
    )
    assert 'これより, これより,' not in result.markdown
