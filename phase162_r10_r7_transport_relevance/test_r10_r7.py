from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay
from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_renderer import _render_group_proof_narrative_latex
from toda_group_proof_narrative_transport_facts import extract_suspension_transport_facts
from toda_group_proof_narrative_transport_link import (
    add_transport_link_to_common_markdown,
    render_suspension_transport_link,
)


def test_r10_r7_unrelated_ancestor_transport_not_appended():
    replay = build_phase162_pi5_3_web_replay()
    root = replay.root_step
    assert extract_suspension_transport_facts(root) is not None
    assert render_suspension_transport_link(root, _render_group_proof_narrative_latex) is None
    content = '## 証明\n\n本文。\n\n□\n'
    assert add_transport_link_to_common_markdown(root,content,_render_group_proof_narrative_latex) == content


def test_r10_r7_stable_transport_preserved():
    presentation, _, _, _ = _method_evidence_data(4, 1)
    paragraph = render_suspension_transport_link(presentation.root_step,_render_group_proof_narrative_latex)
    assert paragraph is not None
    assert '証明木に記録された群構造の移送' in paragraph


def test_r10_r7_stable_base_does_not_append():
    presentation, _, _, _ = _method_evidence_data(3, 1)
    assert render_suspension_transport_link(presentation.root_step,_render_group_proof_narrative_latex) is None
