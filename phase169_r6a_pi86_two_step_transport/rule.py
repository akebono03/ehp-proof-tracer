"""Phase 169 R6A: sourced E^2 transfer via two proved eta-square images.

The only group presentation premise is the prior positioned pi_6^4 result.
The intermediate eta_5^2 is a typed generator expression, not a claim that
pi_7^5 has a cited group structure. All map/image steps remain search goals.
"""
from __future__ import annotations

from expression import Composition
from homotopy_groups import (
    FiniteCyclicGroup,
    TodaIteratedSuspensionMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement


def _two_step_eta_square_images(source: Relation, goal: Relation) -> tuple[GeneratorImage, GeneratorImage] | None:
    """Identify an intermediate eta-square without importing its group answer."""
    if not (
        isinstance(source, Relation)
        and isinstance(goal, Relation)
        and isinstance(source.rhs, FiniteCyclicGroup)
        and isinstance(goal.rhs, FiniteCyclicGroup)
        and isinstance(source.rhs.generator, Composition)
        and isinstance(goal.rhs.generator, Composition)
        and source.lhs == TodaPrimaryGroup(6, 4)
        and goal.lhs == TodaPrimaryGroup(8, 6)
    ):
        return None
    middle = TodaPrimaryGroup(7, 5)
    # These are the middle factors of the two given eta-square expressions,
    # not a database fact or an assertion of pi_7^5 group structure.
    middle_generator = Composition(
        source.rhs.generator.right,
        goal.rhs.generator.left,
    )
    first = GeneratorImage(
        TodaSuspensionMap(source.lhs, middle),
        source.rhs.generator,
        middle_generator,
    )
    second = GeneratorImage(
        TodaSuspensionMap(middle, goal.lhs),
        middle_generator,
        goal.rhs.generator,
    )
    from phase165_r12_r21_eta_generator_chain import _composition_eta_suspensions
    if _composition_eta_suspensions(first) is None:
        return None
    if _composition_eta_suspensions(second) is None:
        return None
    return first, second


def two_step_eta_square_transport_rule(goal: Relation) -> InferenceRule:
    """Transfer a cyclic presentation only when four typed premises are proved."""
    if not (
        isinstance(goal, Relation)
        and goal.relation_type is RelationType.EQUALITY
        and goal.lhs == TodaPrimaryGroup(8, 6)
        and isinstance(goal.rhs, FiniteCyclicGroup)
        and goal.rhs.order == 2
    ):
        raise ValueError("a concrete pi_8^6 eta-square goal is required")

    def guard(premises, bindings):
        if len(premises) != 4:
            return False
        lower_step, iso_step, image1_step, image2_step = premises
        if not all(step.rule is ProofRule.INFERENCE for step in premises[1:]):
            return False
        lower, iso, image1, image2 = (step.conclusion for step in premises)
        if not (
            isinstance(lower, Relation)
            and lower.relation_type is RelationType.EQUALITY
            and lower.lhs == TodaPrimaryGroup(6, 4)
            and isinstance(lower.rhs, FiniteCyclicGroup)
            and lower.rhs.order == goal.rhs.order
            and isinstance(iso, Toda45IsomorphismStatement)
            and isinstance(iso.map, TodaIteratedSuspensionMap)
            and iso.map.exponent == 2
            and iso.map.source_group == lower.lhs
            and iso.map.target_group == goal.lhs
            and isinstance(image1, GeneratorImage)
            and isinstance(image2, GeneratorImage)
        ):
            return False
        # Stable range n >= k+2, checked independently of the cited theorem.
        n = lower.lhs.sphere_dimension
        q = lower.lhs.group_dimension
        if type(n) is not int or type(q) is not int or n < q - n + 2:
            return False
        expected_images = _two_step_eta_square_images(lower, goal)
        return expected_images is not None and (image1, image2) == expected_images

    return InferenceRule(
        name="prior Toda (4.5) E2 transport through two proved eta-square images",
        description=(
            "Transfer the earlier positioned pi_6^4 presentation using an actually "
            "proved Toda (4.5) E^2 isomorphism and two independently proved "
            "consecutive eta-square generator images."
        ),
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=Toda45IsomorphismStatement),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=GeneratorImage),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=GeneratorImage),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_prior_two_step_eta_square_transport(
    goal: object,
    available: tuple[object, ...],
    bridge: RegistryBridgeResult,
    *,
    proof_target: object,
) -> tuple[GoalExpansion, ...]:
    """Add a root candidate, never a ProofStep or unpositioned GIVEN."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be a RegistryBridgeResult")
    if goal != proof_target or not (
        isinstance(goal, Relation)
        and goal.relation_type is RelationType.EQUALITY
        and goal.lhs == TodaPrimaryGroup(8, 6)
        and isinstance(goal.rhs, FiniteCyclicGroup)
        and goal.rhs.order == 2
    ):
        return ()
    citing_id = resolve_specialized_goal_citing_id(bridge, proof_target)
    if citing_id is None:
        return ()
    prior = resolve_prior_group_result(
        bridge, source_n=4, source_k=2, citing_assertion_id=citing_id,
    )
    if not prior.eligible or prior.source_assertion_id is None or prior.relation is None:
        return ()
    source = prior.relation
    if not (
        source.lhs == TodaPrimaryGroup(6, 4)
        and source.relation_type is RelationType.EQUALITY
        and isinstance(source.rhs, FiniteCyclicGroup)
        and source.rhs.order == goal.rhs.order
    ):
        return ()
    images = _two_step_eta_square_images(source, goal)
    if images is None:
        return ()
    iso = Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(
        exponent=2, source_group=source.lhs, target_group=goal.lhs,
    ))
    if not any(
        isinstance(schema, Toda45IsomorphismStatement)
        and (schema == iso or specialize_typed_statement(schema, iso) is not None)
        for schema in available
    ):
        return ()
    # The recursive search must derive all four subgoals in the screened
    # context. In particular the intermediate pi_7^5 is not taken as a fact.
    return (GoalExpansion(
        two_step_eta_square_transport_rule(goal),
        (source, iso, images[0], images[1]),
    ),)
