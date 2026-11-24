"""Replay typed right-Hopf equality transport using existing general rules.

This isolated helper neither registers a new inference rule nor modifies a
shared provider.  Both input steps must already be independent inferences.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, MapApplication, Suspension
from hopf_rules import ehp_h_preserves_equality_inference_rule
from map_facts import EHP_H_MAP
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from relation_rules import (
    equality_preserved_under_left_composition_inference_rule,
    equality_symmetry_inference_rule,
    equality_transitivity_inference_rule,
)


def right_hopf_transport_inputs(
    goal: object, beta: object,
) -> tuple[Relation, Relation] | None:
    """Build the two exact independent premises for a typed H right transport.

    From H(alpha o E beta)=delta o E beta and E beta=gamma, the desired
    conclusion is H(alpha o gamma)=delta o gamma. No textual name matching
    or unverified relation is admitted.
    """
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, MapApplication)
            or goal.lhs.map != EHP_H_MAP
            or not isinstance(goal.lhs.expression, Composition)
            or not isinstance(goal.rhs, Composition)
            or not isinstance(beta, Composition)):
        return None
    alpha = goal.lhs.expression.left
    gamma = goal.lhs.expression.right
    delta = goal.rhs.left
    if (not isinstance(alpha, (HomotopyElement, Composition))
            or not isinstance(gamma, Composition)
            or not isinstance(delta, (HomotopyElement, Composition))
            or goal.rhs.right != gamma):
        return None
    alpha_span = expression_endpoints(alpha)
    beta_span = expression_endpoints(beta)
    gamma_span = expression_endpoints(gamma)
    delta_span = expression_endpoints(delta)
    if (alpha_span is None or beta_span is None or gamma_span is None
            or delta_span is None
            or gamma_span != (beta_span[0] + 1, beta_span[1] + 1)
            or alpha_span[0] != gamma_span[1]
            or delta_span != (alpha_span[0], 2 * alpha_span[1] - 1)):
        return None
    suspended = Suspension(beta)
    substituted = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, suspended)),
        Composition(delta, suspended),
        RelationType.EQUALITY,
    )
    suspension = Relation(suspended, gamma, RelationType.EQUALITY)
    return substituted, suspension


def _derive_existing_step(
    inference_rule: object,
    premises: tuple[ProofStep, ...],
    expected: Relation,
) -> ProofStep:
    """Replay an actual existing rule and fail closed if its result differs."""
    matches = find_inference_matches_for_rule(inference_rule, premises)
    if len(matches) != 1:
        raise ValueError("EXISTING_RULE_MATCH_NOT_UNIQUE")
    derived = apply_inference_match(matches[0])
    if (derived.rule is not ProofRule.INFERENCE
            or derived.conclusion != expected
            or derived.premises != premises
            or derived.inference_rule is not inference_rule):
        raise ValueError("EXISTING_RULE_REPLAY_MISMATCH")
    return derived


def replay_right_hopf_transport(
    goal: Relation,
    beta: Composition,
    substituted_step: ProofStep,
    suspension_step: ProofStep,
) -> tuple[ProofStep, ...]:
    """Return six inferred steps using only pre-existing congruence rules.

    The returned final step has a complete two-branch premise tree.  Neither
    independent input is manufactured; callers must obtain them from their
    ordinary source-screened proof process.
    """
    required = right_hopf_transport_inputs(goal, beta)
    if required is None:
        raise ValueError("INVALID_TYPED_HOPF_TRANSPORT_GOAL")
    substituted, suspension = required
    if (not isinstance(substituted_step, ProofStep)
            or not isinstance(suspension_step, ProofStep)
            or substituted_step.rule is not ProofRule.INFERENCE
            or suspension_step.rule is not ProofRule.INFERENCE
            or substituted_step.conclusion != substituted
            or suspension_step.conclusion != suspension):
        raise ValueError("INDEPENDENT_INFERENCE_PREMISES_REQUIRED")

    alpha = goal.lhs.expression.left
    gamma = goal.lhs.expression.right
    delta = goal.rhs.left
    suspended = Suspension(beta)
    alpha_comp = _derive_existing_step(
        equality_preserved_under_left_composition_inference_rule(alpha),
        (suspension_step,),
        Relation(Composition(alpha, suspended), Composition(alpha, gamma),
                 RelationType.EQUALITY),
    )
    hopf_comp = _derive_existing_step(
        ehp_h_preserves_equality_inference_rule(),
        (alpha_comp,),
        Relation(substituted.lhs, goal.lhs, RelationType.EQUALITY),
    )
    reverse_hopf_comp = _derive_existing_step(
        equality_symmetry_inference_rule(),
        (hopf_comp,),
        Relation(goal.lhs, substituted.lhs, RelationType.EQUALITY),
    )
    delta_comp = _derive_existing_step(
        equality_preserved_under_left_composition_inference_rule(delta),
        (suspension_step,),
        Relation(substituted.rhs, goal.rhs, RelationType.EQUALITY),
    )
    intermediate = _derive_existing_step(
        equality_transitivity_inference_rule(),
        (reverse_hopf_comp, substituted_step),
        Relation(goal.lhs, substituted.rhs, RelationType.EQUALITY),
    )
    result = _derive_existing_step(
        equality_transitivity_inference_rule(),
        (intermediate, delta_comp),
        goal,
    )
    return alpha_comp, hopf_comp, reverse_hopf_comp, delta_comp, intermediate, result
