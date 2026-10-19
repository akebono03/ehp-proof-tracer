"""Phase 162 R5-6: causal preparation and literature attribution."""

from homotopy_groups import TodaSuspensionIsomorphismStatement
from phase162_validated_proof_presentation import (
    _composed_validated_proof_sections,
    _render_validated_reference_section,
    _validated_ancestral_reference_numbers,
    _validated_main_proof_steps,
    _validated_proof_body_step_lines,
    _validated_reference_number_by_step_id,
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from toda_rules import TodaHopfInvariantSurjectiveStatement
from tests.test_phase162_r2_validated_proof_presentation import _validated_fixture


def test_phase162_r5_6_preparatory_delta_relations_not_in_injectivity_section():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    reference, fixed_ids = _render_validated_reference_section(presentation)
    sections = dict(_composed_validated_proof_sections(presentation, fixed_ids))
    preparation = "\n".join(sections["準備"])
    injectivity = "\n".join(sections["単射性"])
    surjectivity = "\n".join(sections["全射性"])
    # Under fixed-source reuse, the delta(iota5) computation may be hidden
    # behind Proposition 5.1 instead of being repeated in preparation.
    delta_formula = r"\Delta(\iota_{5})=\pm2\eta_{2}"
    assert delta_formula in reference
    if r"\Delta\left(\iota_{5}\right)" in preparation:
        assert r"\Delta\left(\iota_{5}\right)" not in injectivity
    assert r"\Delta\left(\iota_{5}\right)" not in injectivity
    assert "Proposition 5.1" in surjectivity
    assert "は単射" in injectivity
    assert "は全射" in surjectivity


def test_phase162_r5_6_core_uses_actual_map_goal_ancestry():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    core = _validated_main_proof_steps(presentation)
    assert id(presentation.root_step) in core
    assert isinstance(presentation.root_step.conclusion, TodaSuspensionIsomorphismStatement)
    assert len(core) == 7
    assert any(
        isinstance(step.conclusion, TodaHopfInvariantSurjectiveStatement)
        and id(step) in core
        for step in presentation.nodes
    )


def test_phase162_r5_6_reference_ancestry_has_no_fabricated_markers():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    reference_map = _validated_reference_number_by_step_id(presentation)
    _, fixed_ids = _render_validated_reference_section(presentation)
    sections = _composed_validated_proof_sections(presentation, fixed_ids)
    emitted = tuple(text for _, lines in sections for text in lines)
    original = tuple(text for _, text in _validated_proof_body_step_lines(presentation, fixed_ids))
    assert len(emitted) == len(original)
    for step in presentation.nodes:
        ancestry = _validated_ancestral_reference_numbers(step, reference_map)
        assert set(ancestry).issubset(set(reference_map.values()))
    assert render_validated_backward_proof_markdown(presentation).rstrip().endswith("□")
