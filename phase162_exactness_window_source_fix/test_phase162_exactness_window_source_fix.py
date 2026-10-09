import pytest

import toda_group_proof_narrative_exactness_display_contributions as display


@pytest.mark.parametrize(
    ('rendered', 'expected'),
    (
        (
            r'$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.',
            r'\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}',
        ),
        (
            r'$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2}$',
            r'\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2}',
        ),
        (
            r'\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2}',
            r'\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2}',
        ),
    ),
)
def test_exactness_window_returns_only_math(monkeypatch, rendered, expected):
    proof_step = object()
    monkeypatch.setattr(display, '_render_generic_narrative_step', lambda step: rendered)
    assert display._exactness_window_latex(proof_step) == expected


def test_phase162_pi5_3_has_no_doubled_exactness_math():
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
    assert r'$$\pi_' not in result.markdown
    assert '$ は完全である.$ は完全である.' not in result.markdown
    assert r'\pi_{5}^{3} = \mathbb{Z}/2' in result.markdown
