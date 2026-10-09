from toda_group_proof_narrative_renderer import (
    _phase159_consolidate_public_exactness_lines,
    _phase159_public_exactness_latex,
)


def test_phase162_exactness_parser_accepts_clean_inline_math():
    clean = r"$\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である."
    assert _phase159_public_exactness_latex(clean) == (
        r"\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}"
    )


def test_phase162_exactness_parser_rejects_double_delimiters_and_prose():
    malformed = r"$$\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2}$ は完全である.$ は完全である."
    assert _phase159_public_exactness_latex(malformed) is None
    assert _phase159_public_exactness_latex(
        r"$\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2}$ unrelated prose"
    ) is None


def test_phase162_exactness_consolidation_keeps_math_bounded():
    shorter = r"$\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2}$ は完全である."
    longer = r"$\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である."
    lines = _phase159_consolidate_public_exactness_lines([shorter, longer])
    assert lines == [longer]
    assert all('$$' not in line for line in lines)


def test_phase162_pi5_3_public_narrative_has_no_double_exactness_math():
    from phase162_pi5_3_renderer_audit import (
        render_phase162_pi5_3_reconstructed_proof,
    )
    from tests.test_phase59_pi5_3_eta3_squared import build_phase59_4_data

    data = build_phase59_4_data()
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
    leaves = build_phase59_3_data()['premise_steps']
    result = render_phase162_pi5_3_reconstructed_proof(
        data['pi4_2_step'],
        (data['eta3_definition_step'], data['eta4_definition_step']),
        leaves,
    )
    assert '$$\\pi_' not in result.markdown
    assert '$ は完全である.$ は完全である.' not in result.markdown
