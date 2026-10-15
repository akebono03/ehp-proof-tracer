"""Focused tests for the Phase 162 R2 proof-presentation boundary."""

from dataclasses import replace

import pytest

from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import (
    reconstruct_phase161_r7_validated_goal,
)
from phase162_validated_proof_presentation import (
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import (
    TodaSuspensionInjectiveStatement,
    TodaSuspensionSurjectiveStatement,
)


def _validated_fixture():
    leaves = build_phase59_3_data()["premise_steps"]
    roots = {}
    visited = set()

    def visit(step):
        if id(step) in visited:
            return
        visited.add(id(step))
        if step.rule is ProofRule.GIVEN:
            roots[id(step)] = step
        for premise in step.premises:
            visit(premise)

    for leaf in leaves:
        visit(leaf)
    return reconstruct_phase161_r7_validated_goal(
        phase161_r5_target_goal(), leaves, tuple(roots.values())
    )


def test_phase162_r2_reuses_exact_verified_root_and_dependencies():
    validated = _validated_fixture()
    presentation = build_validated_backward_proof_presentation(validated)
    assert presentation.root_step is validated.reconstruction.final_step
    assert presentation.nodes[-1] is presentation.root_step
    assert all(edge.parent_step.premises[edge.premise_index] is edge.premise_step
               for edge in presentation.edges)
    assert {id(step) for step in validated.reconstruction.derived_steps}.issubset(
        {id(step) for step in presentation.nodes}
    )


def test_phase162_r2_injectivity_and_surjectivity_precede_isomorphism():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    conclusions = [step.conclusion for step in presentation.nodes]
    injective_index = next(i for i, s in enumerate(conclusions)
                           if isinstance(s, TodaSuspensionInjectiveStatement)
                           and s.map == presentation.root_step.conclusion.map)
    surjective_index = next(i for i, s in enumerate(conclusions)
                            if isinstance(s, TodaSuspensionSurjectiveStatement)
                            and s.map == presentation.root_step.conclusion.map)
    assert injective_index < surjective_index < len(conclusions) - 1


def test_phase162_r2_text_is_rendered_by_common_step_renderer():
    from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    text = render_validated_backward_proof_markdown(presentation)
    for step in presentation.nodes:
        if step.rule is ProofRule.INFERENCE:
            assert _render_generic_narrative_step(step) in text
    assert text.rstrip().endswith("□")


def test_phase162_r2_rejects_modified_reconstructed_goal():
    validated = _validated_fixture()
    changed = replace(
        validated,
        reconstruction=replace(validated.reconstruction, goal=object()),
    )
    with pytest.raises(ValueError, match="does not prove"):
        build_validated_backward_proof_presentation(changed)


def test_phase162_r2_rejects_untrusted_given_identity():
    validated = _validated_fixture()
    assert validated.provenance.trusted_roots_used
    altered = replace(
        validated,
        provenance=replace(validated.provenance, trusted_roots_used=()),
    )
    with pytest.raises(ValueError, match="Untrusted GIVEN"):
        build_validated_backward_proof_presentation(altered)
