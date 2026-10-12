"""Bounded goal-driven selection for the pi_5^3 cyclic group conclusion.

This uses existing production rules. It does not invent proof premises,
search for literature independently, or implement general theorem proving.
"""

from dataclasses import dataclass, replace

from expression import Composition
from homotopy_groups import (
    FiniteCyclicGroup,
    TodaPrimaryGroup,
)
from phase161_backward_goal_schema import BackwardGoalExpansion
from phase161_r5_backward_proof_reconstruction import (
    phase161_r5_target_goal,
    reconstruct_phase161_r5_goal,
)
from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from toda_rules import (
    toda_eta_family_definition_statement,
    toda_prop53_n3_eta_square_suspension_bridge_inference_rule,
    toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule,
)


@dataclass(frozen=True)
class Pi53BackwardResult:
    goal: Relation
    final_step: ProofStep
    bridge_step: ProofStep
    suspension_step: ProofStep
    pi4_2_step: ProofStep


def _canonical_goals():
    eta2 = toda_eta_family_definition_statement(2).element
    eta3 = toda_eta_family_definition_statement(3).element
    # Match the name used by the existing n=3 transport production.
    # The eta-family definition currently represents this element as "η_4".
    eta4 = replace(toda_eta_family_definition_statement(4).element, name="η₄")
    pi4_2 = Relation(
        lhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
        rhs=FiniteCyclicGroup(order=2, generator=Composition(left=eta2, right=eta3)),
        relation_type=RelationType.EQUALITY,
    )
    pi5_3 = Relation(
        lhs=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        rhs=FiniteCyclicGroup(order=2, generator=Composition(left=eta3, right=eta4)),
        relation_type=RelationType.EQUALITY,
    )
    # Derive the intermediate goal using the existing production, not a
    # separately assembled expression that might use different normalization.
    definition_steps = tuple(
        ProofStep(
            conclusion=toda_eta_family_definition_statement(i),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for i in (3, 4)
    )
    rule = toda_prop53_n3_eta_square_suspension_bridge_inference_rule()
    candidates = tuple(find_inference_matches_for_rule(rule, definition_steps))
    if len(candidates) != 1:
        raise ValueError("Unable to derive unique canonical eta-square bridge")
    bridge_step = apply_inference_match(candidates[0])
    bridge = bridge_step.conclusion
    if bridge_step.rule is not ProofRule.INFERENCE or not isinstance(bridge, Relation):
        raise ValueError("Canonical bridge production returned an invalid conclusion")
    return pi4_2, pi5_3, bridge


def expand_phase162_pi5_3_group_goal(goal: object) -> BackwardGoalExpansion | None:
    """Choose the existing transport production for the exact supported goal.

    The expansion describes required conclusions only; it creates no ProofSteps.
    """
    pi4_2, pi5_3, bridge = _canonical_goals()
    if type(goal) is not Relation or goal != pi5_3:
        return None
    rule = toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule()
    if rule.conclusion_builder is None or rule.match_guard is None:
        raise RuntimeError("Transport production is not executable")
    if len(rule.premise_patterns) != 3:
        raise RuntimeError("Transport production premise count changed")
    return BackwardGoalExpansion(
        goal=goal,
        inference_rule=rule,
        subgoals=(pi4_2, phase161_r5_target_goal(), bridge),
    )


def _apply_unique(rule, premises, goal):
    matches = tuple(
        match for match in find_inference_matches_for_rule(rule, premises)
        if len(match.premises) == len(premises)
        and all(a is b for a, b in zip(match.premises, premises))
    )
    if len(matches) != 1:
        raise ValueError(f"Exactly one inference match required for {goal!r}: {len(matches)}")
    step = apply_inference_match(matches[0])
    if step.rule is not ProofRule.INFERENCE or step.conclusion != goal:
        raise ValueError("Existing production did not prove the requested goal")
    return step


def reconstruct_phase162_pi5_3_group_goal(
    goal: object,
    pi4_2_step: ProofStep,
    eta_definition_steps: tuple[ProofStep, ...],
    ehp_leaf_steps: tuple[ProofStep, ...],
) -> Pi53BackwardResult:
    """Resolve the selected subgoals from independent steps and Phase 161 R5.

    The pi_4^2 proof and eta definitions remain independently supplied roots.
    The suspension isomorphism is reconstructed, never accepted as a leaf.
    """
    expansion = expand_phase162_pi5_3_group_goal(goal)
    if expansion is None:
        raise ValueError("Unsupported group goal")
    if not isinstance(pi4_2_step, ProofStep) or not isinstance(eta_definition_steps, tuple):
        raise TypeError("Expected independent ProofStep inputs")
    if len(eta_definition_steps) != 2 or any(not isinstance(s, ProofStep) for s in eta_definition_steps):
        raise ValueError("Exactly two eta definition steps required")
    if pi4_2_step.rule is not ProofRule.INFERENCE or pi4_2_step.conclusion != expansion.subgoals[0]:
        raise ValueError("Missing independently derived pi_4^2 relation")
    expected_definitions = tuple(toda_eta_family_definition_statement(i) for i in (3, 4))
    if any(s.rule is not ProofRule.GIVEN or s.premises or s.conclusion != expected
           for s, expected in zip(eta_definition_steps, expected_definitions)):
        raise ValueError("Missing or invalid eta definition roots")

    suspension = reconstruct_phase161_r5_goal(expansion.subgoals[1], ehp_leaf_steps).final_step
    bridge = _apply_unique(
        toda_prop53_n3_eta_square_suspension_bridge_inference_rule(),
        eta_definition_steps,
        expansion.subgoals[2],
    )
    final = _apply_unique(
        expansion.inference_rule,
        (pi4_2_step, suspension, bridge),
        goal,
    )
    return Pi53BackwardResult(
        goal=goal,
        final_step=final,
        bridge_step=bridge,
        suspension_step=suspension,
        pi4_2_step=pi4_2_step,
    )
