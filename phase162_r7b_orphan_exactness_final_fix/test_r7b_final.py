from toda_group_proof_narrative_contribution_renderer import (
    suppress_toda_group_proof_narrative_dangling_connectors,
)
from toda_group_proof_narrative_renderer import (
    render_toda_group_proof_narrative_markdown,
)


def test_r7b_final_preserves_valid_exactness_intro():
    original = (
        '次の完全列を考える.\n\n'
        '\\[\nA \\xrightarrow{E} B \\xrightarrow{H} C\n\\]'
    )
    assert suppress_toda_group_proof_narrative_dangling_connectors(original) == original


def test_r7b_final_cleanup_is_idempotent():
    original = (
        '次の完全列を考える.\n\n'
        '次の完全列を考える.\n\n'
        '完全性より, $E$ は単射.'
    )
    cleaned = suppress_toda_group_proof_narrative_dangling_connectors(original)
    assert cleaned == '完全性より, $E$ は単射.'
    assert suppress_toda_group_proof_narrative_dangling_connectors(cleaned) == cleaned


def test_r7b_final_public_narrative_has_no_orphan_intro():
    from phase162_pi5_3_renderer_audit import render_phase162_pi5_3_reconstructed_proof
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
        if paragraph == '次の完全列を考える.':
            assert index + 1 < len(paragraphs)
            following = paragraphs[index + 1]
            assert (r'\xrightarrow{' in following or r'\longrightarrow' in following)
    assert r'\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}' in result.markdown
    assert result.markdown.rstrip().endswith('□')
