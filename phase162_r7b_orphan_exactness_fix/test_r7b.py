from toda_group_proof_narrative_contribution_renderer import (
    suppress_toda_group_proof_narrative_dangling_connectors,
)


def test_r7b_removes_orphan_before_explanation():
    original = '次の完全列を考える.\n\n完全性より, $E$ は単射.'
    assert suppress_toda_group_proof_narrative_dangling_connectors(original) == '完全性より, $E$ は単射.'


def test_r7b_removes_repeated_orphan_introductions():
    original = '次の完全列を考える.\n\n次の完全列を考える.\n\n$A=B$.'
    assert suppress_toda_group_proof_narrative_dangling_connectors(original) == '$A=B$.'


def test_r7b_preserves_valid_exactness_display():
    original = '次の完全列を考える.\n\n\\[\nA \\xrightarrow{E} B \\xrightarrow{H} C.\n\\]'
    assert suppress_toda_group_proof_narrative_dangling_connectors(original) == original


def test_r7b_preserves_valid_inline_exactness_display():
    original = r'次の完全列を考える.' + '\n\n' + r'$A \xrightarrow{E} B \xrightarrow{H} C$ は完全である.'
    assert suppress_toda_group_proof_narrative_dangling_connectors(original) == original


def test_r7b_does_not_change_mathematical_derivations():
    original = r'$\Delta(\iota_5)=2\eta_2$.\n\n$E$ は同型.'
    assert suppress_toda_group_proof_narrative_dangling_connectors(original) == original


def test_r7b_pi5_3_public_narrative_has_no_orphan_exactness_intro():
    from phase162_pi5_3_renderer_audit import (
        render_phase162_pi5_3_reconstructed_proof,
    )
    from tests.test_phase59_pi5_3_eta3_squared import build_phase59_4_data
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data

    data = build_phase59_4_data()
    result = render_phase162_pi5_3_reconstructed_proof(
        data['pi4_2_step'],
        (data['eta3_definition_step'], data['eta4_definition_step']),
        build_phase59_3_data()['premise_steps'],
    )
    paragraphs = [p.strip() for p in result.markdown.split('\n\n') if p.strip()]
    for index, paragraph in enumerate(paragraphs):
        if paragraph != '次の完全列を考える.':
            continue
        assert index + 1 < len(paragraphs)
        next_paragraph = paragraphs[index + 1]
        assert r'\xrightarrow{' in next_paragraph or r'\longrightarrow' in next_paragraph
