"""Production bridge from the bounded Phase 162 pi_5^3 reconstruction to Web replay."""

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase162_pi5_3_backward_selection import (
    _canonical_goals,
    reconstruct_phase162_pi5_3_group_goal,
)
from phase162_web_narrative_integration import _phase162_ehp_leaves
from probes.probe_phase50_capabilities import build_phase50_representative_result
from probes.probe_phase56_capabilities import build_phase56_representative_result
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_match
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_rules import (
    toda_52_pi4_2_finite_cyclic_transport_inference_rule,
    toda_eta_family_definition_statement,
)


def build_phase162_pi5_3_web_replay(max_depth: int = 40):
    """Construct a new, inference-backed root, then reuse the standard replay API."""
    phase50 = build_phase50_representative_result()
    phase56 = build_phase56_representative_result()
    pi4_3_steps = phase50["final_group_steps"]
    toda52_steps = phase56["composition_isomorphism_steps"]
    if len(pi4_3_steps) != 1 or len(toda52_steps) != 1:
        raise ValueError("Expected unique independently proved Toda (5.2) premises")

    match = find_inference_match(
        toda_52_pi4_2_finite_cyclic_transport_inference_rule(),
        (pi4_3_steps[0], toda52_steps[0]),
    )
    if match is None:
        raise ValueError("Could not prove source pi_4^2 group structure")
    source_step = apply_inference_match(match)
    eta_steps = tuple(
        ProofStep(
            conclusion=toda_eta_family_definition_statement(index),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for index in (3, 4)
    )
    prop51, hopf_eta5, exactness = _phase162_ehp_leaves()
    ehp_leaves = (prop51, hopf_eta5) + exactness
    _, goal, _ = _canonical_goals()
    reconstruction = reconstruct_phase162_pi5_3_group_goal(
        goal, source_step, eta_steps, ehp_leaves
    )
    root = reconstruction.final_step
    if root.conclusion != goal or root.rule is not ProofRule.INFERENCE:
        raise ValueError("The reconstructed root does not prove pi_5^3")
    if not isinstance(goal.rhs, FiniteCyclicGroup):
        raise ValueError("The reconstructed goal is not a finite cyclic group")
    entry = ProofRepositoryEntry(
        key="phase162-pi5-3-reconstructed-web",
        step=root,
        theorem="Toda Proposition 5.3",
        phase="162",
    )
    group_result = TodaGroupResult(
        target=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        group_structure=goal.rhs,
        generators=(goal.rhs.generator,),
        generator_orders=(goal.rhs.order,),
        source_entry=entry,
        proof_step=root,
    )
    replay = build_toda_group_result_proof_replay(group_result, max_depth=max_depth)
    if replay.root_step is not root:
        raise ValueError("Web replay replaced the newly constructed root")
    return replay
