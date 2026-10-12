"""Web proof entry point through the unified goal-only proof search boundary.

No Phase 162 replay, per-group premise selection, or fallback is permitted.
"""
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_goal_only_search import construct_registered_group_proof
from proof import ProofRule
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown


def build_phase164_r5_web_pi5_3_proof(*, max_depth: int = 2):
    """Ask the unified solver for pi_5^3; fail closed if it cannot prove it."""
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise TypeError("max_depth must be an integer")
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")

    group_step = construct_registered_group_proof(n=3, k=2)
    if group_step.rule is not ProofRule.INFERENCE:
        raise ValueError("goal-only search did not derive a proof")
    goal = group_step.conclusion
    if (goal.lhs != TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
            or not isinstance(goal.rhs, FiniteCyclicGroup)):
        raise ValueError("goal-only search returned the wrong group conclusion")

    entry = ProofRepositoryEntry(
        key="phase165-goal-only-pi5-3-web",
        step=group_step,
        theorem="Toda Proposition 5.3",
        phase="165 R1",
    )
    result = TodaGroupResult(
        target=goal.lhs,
        group_structure=goal.rhs,
        generators=(goal.rhs.generator,),
        generator_orders=(goal.rhs.order,),
        source_entry=entry,
        proof_step=group_step,
    )
    replay = build_toda_group_result_proof_replay(result, max_depth=max_depth)
    if replay.root_step is not group_step:
        raise ValueError("replay replaced the goal-only proof root")
    narrative = render_toda_group_proof_narrative_markdown(
        build_toda_group_proof_presentation(replay)
    )
    if not narrative or "## 証明" not in narrative:
        raise ValueError("common narrative rendering failed")
    return replay, narrative
