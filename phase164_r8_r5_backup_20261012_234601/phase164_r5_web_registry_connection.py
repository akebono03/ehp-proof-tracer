"""Phase 164 R5: live registry-backed pi_5^3 group proof for the Web narrative."""
from __future__ import annotations

from pathlib import Path

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from phase162_web_narrative_integration import _phase162_ehp_leaves
from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r8_registry_reconstruction import (
    _known_trusted_roots,
    reconstruct_phase164_r4_r8_pi5_3,
)
from proof import ProofRule, apply_inference_match, find_inference_matches_for_rule
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_rules import toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule


def build_phase164_r5_web_pi5_3_proof(*, max_depth: int = 2):
    """Build the group root using an R4-R8-validated, registry-backed map proof.

    The original group/source and generator-bridge subproofs stay INFERENCE.
    R4-R8 supplies the *same* typed literature-connected isomorphism step,
    not a display-only replacement. No test fixture is imported.
    """
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise TypeError("max_depth must be an integer")
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    manifest = Path("phase163_r4_r94_output/manifest.json")
    if not manifest.is_file():
        raise ValueError("R4-R8 source manifest missing; Web proof cannot be certified")

    prop51, hopf, exactness = _phase162_ehp_leaves()
    ehp_leaves = (prop51, hopf) + exactness
    fixed = reconstruct_phase164_r4_r8_pi5_3(
        audit_current_repository(manifest),
        ehp_leaves,
        _known_trusted_roots(ehp_leaves),
        user_confirmed_original=True,
    )
    isomorphism_step = fixed.validated.reconstruction.final_step
    if isomorphism_step.rule is not ProofRule.INFERENCE:
        raise ValueError("R4-R8 did not derive an isomorphism")

    previous_replay = build_phase162_pi5_3_web_replay(max_depth=2)
    previous_root = previous_replay.root_step
    if previous_root.rule is not ProofRule.INFERENCE or len(previous_root.premises) != 3:
        raise ValueError("Phase 162 group root structure changed")
    source_step, prior_isomorphism, generator_bridge = previous_root.premises
    if prior_isomorphism.conclusion != isomorphism_step.conclusion:
        raise ValueError("registry-backed isomorphism differs from group requirement")
    if source_step.rule is not ProofRule.INFERENCE or generator_bridge.rule is not ProofRule.INFERENCE:
        raise ValueError("group source or generator bridge is not inferred")

    rule = toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule()
    premises = (source_step, isomorphism_step, generator_bridge)
    matches = tuple(
        match for match in find_inference_matches_for_rule(rule, premises)
        if len(match.premises) == len(premises)
        and all(actual is expected for actual, expected in zip(match.premises, premises))
    )
    if len(matches) != 1:
        raise ValueError("registry-backed group transport has no unique match")
    group_step = apply_inference_match(matches[0])
    if group_step.rule is not ProofRule.INFERENCE or group_step.conclusion != previous_root.conclusion:
        raise ValueError("group conclusion did not match the original group result")
    if tuple(group_step.premises) != premises:
        raise ValueError("group proof lost the registry-backed isomorphism")

    goal = group_step.conclusion
    if not isinstance(goal.rhs, FiniteCyclicGroup):
        raise ValueError("unexpected target group structure")
    entry = ProofRepositoryEntry(
        key="phase164-r5-registry-backed-pi5-3-web",
        step=group_step,
        theorem="Toda Proposition 5.3",
        phase="164 R5",
    )
    result = TodaGroupResult(
        target=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        group_structure=goal.rhs,
        generators=(goal.rhs.generator,),
        generator_orders=(goal.rhs.order,),
        source_entry=entry,
        proof_step=group_step,
    )
    replay = build_toda_group_result_proof_replay(result, max_depth=max_depth)
    if replay.root_step is not group_step:
        raise ValueError("replay did not preserve the registry-backed group root")

    # Render the actual group-root proof through the shared pipeline.
    # No pi_5^3-specific sentences or concatenated markdown are permitted.
    presentation = build_toda_group_proof_presentation(replay)
    narrative = render_toda_group_proof_narrative_markdown(presentation)
    if not narrative or "## 証明" not in narrative:
        raise ValueError("common group narrative unavailable")
    return replay, narrative
