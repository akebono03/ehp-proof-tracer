"""Phase 162 R2: connect existing source-group and eta-family proof steps.

No completed target-group proof is consumed as a premise. The source structure
must be independently supplied as an already derived ProofStep. The bridge is
freshly derived from independently supplied eta-family definition steps.
"""

from dataclasses import dataclass

from homotopy_groups import FiniteCyclicGroup, TodaSuspensionMap
from phase161_r7_premise_provenance_validation import (
    PremiseProvenanceReport,
    validate_phase161_r7_provenance,
)
from phase162_group_structure_backward import (
    GroupStructureBackwardResult,
    expand_group_structure_goal,
    reconstruct_group_structure_goal,
)
from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from toda_rules import toda_prop53_n3_eta_square_suspension_bridge_inference_rule


@dataclass(frozen=True)
class ExistingProofConnectionResult:
    reconstruction: GroupStructureBackwardResult
    source_structure_step: ProofStep
    generator_image_step: ProofStep
    provenance: PremiseProvenanceReport


def reconstruct_phase162_r2_from_existing_proofs(
    goal: Relation,
    suspension_map: TodaSuspensionMap,
    source_structure_steps: tuple[ProofStep, ...],
    eta_definition_steps: tuple[ProofStep, ...],
    ehp_leaf_steps: tuple[ProofStep, ...],
    trusted_given_roots: tuple[ProofStep, ...],
) -> ExistingProofConnectionResult:
    """Resolve the root group goal using real source and eta-family evidence.

    The caller supplies existing proof steps, not a final pi_5^3 proof.
    Only a matching independently derived source-group relation is accepted.
    The eta-square bridge is executed from its original definition premises.
    All reachable inference ancestry is checked against explicit GIVEN roots.
    """
    if not isinstance(source_structure_steps, tuple) or any(
        not isinstance(step, ProofStep) for step in source_structure_steps
    ):
        raise TypeError("source_structure_steps must be tuple[ProofStep, ...]")
    if not isinstance(eta_definition_steps, tuple) or any(
        not isinstance(step, ProofStep) for step in eta_definition_steps
    ):
        raise TypeError("eta_definition_steps must be tuple[ProofStep, ...]")
    if not isinstance(ehp_leaf_steps, tuple) or any(
        not isinstance(step, ProofStep) for step in ehp_leaf_steps
    ):
        raise TypeError("ehp_leaf_steps must be tuple[ProofStep, ...]")

    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        raise ValueError("Expected target group equality goal")
    if not isinstance(goal.rhs, FiniteCyclicGroup):
        raise ValueError("Expected finite cyclic target group")

    candidates = tuple(
        step for step in source_structure_steps
        if step.rule is ProofRule.INFERENCE
        and isinstance(step.conclusion, Relation)
        and step.conclusion.relation_type is RelationType.EQUALITY
        and step.conclusion.lhs == suspension_map.source_group
        and isinstance(step.conclusion.rhs, FiniteCyclicGroup)
        and step.conclusion.rhs.order == goal.rhs.order
    )
    if len(candidates) != 1:
        raise ValueError("Missing or ambiguous derived source-group structure")
    source_step = candidates[0]
    source_generator = source_step.conclusion.rhs.generator
    plan = expand_group_structure_goal(goal, suspension_map, source_generator)
    if source_step.conclusion != plan.source_structure_goal:
        raise ValueError("Source structure does not match backward goal")

    bridge_rule = toda_prop53_n3_eta_square_suspension_bridge_inference_rule()
    bridge_matches = tuple(
        match for match in find_inference_matches_for_rule(
            bridge_rule, eta_definition_steps
        )
        if len(match.premises) == len(eta_definition_steps)
        and all(a is b for a, b in zip(match.premises, eta_definition_steps))
    )
    if len(bridge_matches) != 1:
        raise ValueError("Missing or ambiguous eta-family definition bridge")
    bridge_step = apply_inference_match(bridge_matches[0])
    if bridge_step.conclusion != plan.generator_image_goal:
        raise ValueError("Derived generator image does not match backward goal")

    result = reconstruct_group_structure_goal(
        goal=goal,
        suspension_map=suspension_map,
        source_generator=source_generator,
        ehp_leaf_steps=ehp_leaf_steps,
        group_leaf_steps=(source_step, bridge_step),
    )
    provenance = validate_phase161_r7_provenance(
        (result.final_step,), trusted_given_roots
    )
    return ExistingProofConnectionResult(
        reconstruction=result,
        source_structure_step=source_step,
        generator_image_step=bridge_step,
        provenance=provenance,
    )
