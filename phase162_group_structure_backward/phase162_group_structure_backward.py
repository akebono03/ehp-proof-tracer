"""Phase 162: group-structure-first backward proof reconstruction.

No premises are invented. The seven Phase 161 EHP inferences remain unchanged.
The new transport is a real InferenceRule validated by the existing matcher.
"""

from dataclasses import dataclass

from expression import MapApplication, MapSymbol
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap
from phase161_backward_goal_schema import BackwardGoalExpansion
from phase161_r5_backward_proof_reconstruction import reconstruct_phase161_r5_goal
from proof import (
    InferenceRule,
    PremisePattern,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    apply_inference_match,
    find_inference_matches_for_rule,
)


@dataclass(frozen=True)
class GroupStructureBackwardPlan:
    goal: Relation
    suspension_map: TodaSuspensionMap
    source_structure_goal: Relation
    generator_image_goal: Relation
    expansion: BackwardGoalExpansion


@dataclass(frozen=True)
class GroupStructureBackwardResult:
    goal: Relation
    final_step: ProofStep
    derived_steps: tuple[ProofStep, ...]
    leaf_steps: tuple[ProofStep, ...]
    plan: GroupStructureBackwardPlan


def _transport_conclusion(premises: tuple[ProofStep, ...]) -> Relation:
    isomorphism, structure, image = (step.conclusion for step in premises)
    return Relation(
        lhs=isomorphism.map.target_group,
        rhs=FiniteCyclicGroup(order=structure.rhs.order, generator=image.rhs),
        relation_type=RelationType.EQUALITY,
    )


def _transport_guard(premises, bindings=()) -> bool:
    if len(premises) != 3:
        return False
    isomorphism, structure, image = (step.conclusion for step in premises)
    if not isinstance(isomorphism, TodaSuspensionIsomorphismStatement):
        return False
    if not isinstance(structure, Relation) or not isinstance(image, Relation):
        return False
    if structure.relation_type is not RelationType.EQUALITY or image.relation_type is not RelationType.EQUALITY:
        return False
    if not isinstance(structure.rhs, FiniteCyclicGroup):
        return False
    if not isinstance(structure.rhs.order, int) or isinstance(structure.rhs.order, bool) or structure.rhs.order <= 0:
        return False
    if structure.lhs != isomorphism.map.source_group:
        return False
    if image.lhs != MapApplication(map=MapSymbol(name="E"), expression=structure.rhs.generator):
        return False
    return True


def group_structure_transport_inference_rule() -> InferenceRule:
    """Transport a finite cyclic presentation along a proved suspension isomorphism."""
    return InferenceRule(
        name="phase162_group_structure_transport",
        description="Transport a finite cyclic generator under a proven suspension isomorphism",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=TodaSuspensionIsomorphismStatement),
            PremisePattern(relation_type=RelationType.EQUALITY),
            PremisePattern(relation_type=RelationType.EQUALITY),
        ),
        match_guard=_transport_guard,
        conclusion_builder=_transport_conclusion,
    )


def expand_group_structure_goal(
    goal: Relation,
    suspension_map: TodaSuspensionMap,
    source_generator: object,
) -> GroupStructureBackwardPlan:
    """Expand the final group goal before resolving any child proofs."""
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        raise ValueError("Goal must be an equality relation")
    if not isinstance(goal.rhs, FiniteCyclicGroup) or goal.lhs != suspension_map.target_group:
        raise ValueError("Goal must describe target finite cyclic group")
    source_structure = Relation(
        lhs=suspension_map.source_group,
        rhs=FiniteCyclicGroup(order=goal.rhs.order, generator=source_generator),
        relation_type=RelationType.EQUALITY,
    )
    generator_image = Relation(
        lhs=MapApplication(map=MapSymbol(name="E"), expression=source_generator),
        rhs=goal.rhs.generator,
        relation_type=RelationType.EQUALITY,
    )
    isomorphism = TodaSuspensionIsomorphismStatement(map=suspension_map)
    expansion = BackwardGoalExpansion(
        goal=goal,
        inference_rule=group_structure_transport_inference_rule(),
        subgoals=(isomorphism, source_structure, generator_image),
    )
    return GroupStructureBackwardPlan(goal, suspension_map, source_structure, generator_image, expansion)


def reconstruct_group_structure_goal(
    goal: Relation,
    suspension_map: TodaSuspensionMap,
    source_generator: object,
    ehp_leaf_steps: tuple[ProofStep, ...],
    group_leaf_steps: tuple[ProofStep, ...],
) -> GroupStructureBackwardResult:
    """Resolve goal-derived children and execute the registered transport rule.

    The two group leaves must already exist as supplied ProofSteps. Their
    provenance should be validated at the calling boundary; none is fabricated.
    """
    plan = expand_group_structure_goal(goal, suspension_map, source_generator)
    if not isinstance(group_leaf_steps, tuple) or any(not isinstance(s, ProofStep) for s in group_leaf_steps):
        raise TypeError("group_leaf_steps must be tuple[ProofStep, ...]")
    resolved = []
    for subgoal in plan.expansion.subgoals:
        if isinstance(subgoal, TodaSuspensionIsomorphismStatement):
            reconstructed = reconstruct_phase161_r5_goal(subgoal, ehp_leaf_steps)
            resolved.append(reconstructed.final_step)
        else:
            candidates = tuple(s for s in group_leaf_steps if s.conclusion == subgoal)
            if len(candidates) != 1:
                raise ValueError(f"Missing or ambiguous independent group premise: {subgoal!r}")
            resolved.append(candidates[0])
    matches = tuple(m for m in find_inference_matches_for_rule(plan.expansion.inference_rule, tuple(resolved)) if all(a is b for a, b in zip(m.premises, resolved)))
    if len(matches) != 1:
        raise ValueError("Group structure transport inference rejected its premises")
    final = apply_inference_match(matches[0])
    if final.conclusion != goal or final.rule is not ProofRule.INFERENCE:
        raise ValueError("Group structure transport did not prove requested goal")
    return GroupStructureBackwardResult(
        goal=goal,
        final_step=final,
        derived_steps=reconstructed.derived_steps + (final,),
        leaf_steps=reconstructed.leaf_steps + tuple(resolved[1:]),
        plan=plan,
    )
