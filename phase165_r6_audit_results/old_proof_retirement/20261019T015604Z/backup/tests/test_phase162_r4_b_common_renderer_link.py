from dataclasses import replace

from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_renderer import (
    _phase158_baseline_render_toda_group_proof_narrative_markdown,
    _render_group_proof_narrative_latex,
)
from toda_group_proof_narrative_transport_facts import (
    extract_suspension_transport_facts,
)
from toda_group_proof_narrative_transport_link import (
    render_suspension_transport_link,
    add_transport_link_to_common_markdown,
)


def test_phase162_r4_b_common_baseline_contains_tree_backed_link():
    presentation, _, _, _ = _method_evidence_data(4, 1)
    paragraph = render_suspension_transport_link(
        presentation.root_step, _render_group_proof_narrative_latex,
    )
    assert paragraph is not None
    assert r'\eta' in paragraph
    assert '証明木に記録された群構造の移送' in paragraph
    rendered = _phase158_baseline_render_toda_group_proof_narrative_markdown(presentation)
    assert paragraph in rendered
    assert '## 証明' in rendered


def test_phase162_r4_b_no_isomorphism_means_no_added_prose():
    presentation, _, _, _ = _method_evidence_data(4, 1)
    facts = extract_suspension_transport_facts(presentation.root_step)
    assert facts is not None
    # A new tree root containing only the final statement is not a valid
    # witness for the transport; the renderer cannot recover the missing map.
    disconnected = replace(presentation.root_step, premises=())
    assert render_suspension_transport_link(
        disconnected, _render_group_proof_narrative_latex,
    ) is None
    original = '## 証明\n\n導出不能。\n\n$\\square$\n'
    assert add_transport_link_to_common_markdown(
        disconnected, original, _render_group_proof_narrative_latex,
    ) == original


def test_phase162_r4_b_link_idempotent_and_nonstable_unchanged():
    presentation, _, _, _ = _method_evidence_data(4, 1)
    root = presentation.root_step
    text = '## 証明\n\n根拠。\n\n$\\square$\n'
    once = add_transport_link_to_common_markdown(
        root, text, _render_group_proof_narrative_latex,
    )
    twice = add_transport_link_to_common_markdown(
        root, once, _render_group_proof_narrative_latex,
    )
    assert once == twice
    assert once != text
    other_presentation, _, _, _ = _method_evidence_data(3, 1)
    assert render_suspension_transport_link(
        other_presentation.root_step, _render_group_proof_narrative_latex,
    ) is None
    assert add_transport_link_to_common_markdown(
        other_presentation.root_step, text, _render_group_proof_narrative_latex,
    ) == text


def test_phase162_r4_b_stable_base_has_no_transported_target_paragraph():
    base, _, _, _ = _method_evidence_data(3, 1)
    target, _, _, _ = _method_evidence_data(4, 1)
    assert extract_suspension_transport_facts(base.root_step) is not None
    assert render_suspension_transport_link(
        base.root_step, _render_group_proof_narrative_latex,
    ) is None
    assert render_suspension_transport_link(
        target.root_step, _render_group_proof_narrative_latex,
    ) is not None
