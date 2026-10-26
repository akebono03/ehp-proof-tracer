"""Cited Toda (4.5) transport of a composite eta generator, one suspension.

A literature-positioned source relation is a premise without requiring its
proof to be complete. The one-step composite image is independently derived
from the cited eta-family definition. Neither proof nor a source leaf is forged.
"""
from __future__ import annotations

from homotopy_groups import (
    FiniteCyclicGroup, TodaIteratedSuspensionMap, TodaPrimaryGroup,
    TodaSuspensionMap,
)
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement


def toda45_composite_transport_rule(goal: Relation) -> InferenceRule:
    """Conclude precisely the group transferred by a proven E image and (4.5)."""
    if not (isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and isinstance(goal.lhs, TodaPrimaryGroup)
            and isinstance(goal.rhs, FiniteCyclicGroup)):
        raise TypeError("a concrete finite-cyclic group goal is required")

    def guard(premises, bindings):
        if len(premises) != 3:
            return False
        source, stable_iso, image = (step.conclusion for step in premises)
        if (not isinstance(source, Relation)
                or source.relation_type is not RelationType.EQUALITY
                or not isinstance(source.rhs, FiniteCyclicGroup)
                or not isinstance(source.lhs, TodaPrimaryGroup)
                or not isinstance(stable_iso, Toda45IsomorphismStatement)
                or not isinstance(image, GeneratorImage)
                or premises[1].rule is not ProofRule.INFERENCE
                or premises[2].rule is not ProofRule.INFERENCE):
            return False
        mapping = stable_iso.map
        if not isinstance(mapping, TodaIteratedSuspensionMap):
            return False
        base_n = source.lhs.sphere_dimension
        base_q = source.lhs.group_dimension
        if (type(base_n) is not int or type(base_q) is not int
                or base_n < 2 or base_q < base_n
                or base_n < (base_q - base_n) + 2):
            return False
        target = TodaPrimaryGroup(base_q + 1, base_n + 1)
        if not (mapping.exponent == 1
                and mapping.source_group == source.lhs
                and mapping.target_group == target == goal.lhs
                and source.rhs.order == goal.rhs.order
                and image.map == TodaSuspensionMap(source.lhs, target)
                and image.source_generator == source.rhs.generator
                and image.target_generator == goal.rhs.generator):
            return False
        from phase165_r12_r21_eta_generator_chain import _composition_eta_suspensions
        return _composition_eta_suspensions(image) is not None

    return InferenceRule(
        name="cited Toda (4.5) finite-cyclic composite generator transport",
        description=(
            "Transfer a prior, citation-screened group result by the specialized "
            "Toda (4.5) isomorphism and the independently proved eta composite image."
        ),
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=Toda45IsomorphismStatement),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=GeneratorImage),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_toda45_composite_transport(
    goal: object, available: tuple[object, ...]
) -> tuple[GoalExpansion, ...]:
    """Propose a checked three-premise transport, never a manufactured result.

    Candidate source relations and the (4.5) schema come only from source
    statements that have already passed the ordinary publication screening.
    The backward search must still prove all three concrete premises.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not (isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and isinstance(goal.lhs, TodaPrimaryGroup)
            and isinstance(goal.rhs, FiniteCyclicGroup)):
        return ()
    target_n = goal.lhs.sphere_dimension
    target_q = goal.lhs.group_dimension
    if (type(target_n) is not int or type(target_q) is not int
            or target_n < 3 or target_q < target_n):
        return ()

    from phase165_r12_r21_eta_generator_chain import _composition_eta_suspensions
    from phase165_r57_r20_general_specialization import specialize_typed_statement

    options = []
    for source in available:
        if not (isinstance(source, Relation)
                and source.relation_type is RelationType.EQUALITY
                and isinstance(source.lhs, TodaPrimaryGroup)
                and isinstance(source.rhs, FiniteCyclicGroup)
                and source.rhs.order == goal.rhs.order):
            continue
        base_n = source.lhs.sphere_dimension
        base_q = source.lhs.group_dimension
        if (type(base_n) is not int or type(base_q) is not int
                or base_n + 1 != target_n or base_q + 1 != target_q
                or base_n < (base_q - base_n) + 2):
            continue
        image = GeneratorImage(
            map=TodaSuspensionMap(source.lhs, goal.lhs),
            source_generator=source.rhs.generator,
            target_generator=goal.rhs.generator,
        )
        if _composition_eta_suspensions(image) is None:
            continue
        iso = Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(
            exponent=1, source_group=source.lhs, target_group=goal.lhs,
        ))
        if not any(
            isinstance(schema, Toda45IsomorphismStatement)
            and (schema == iso or specialize_typed_statement(schema, iso) is not None)
            for schema in available
        ):
            continue
        candidate = GoalExpansion(toda45_composite_transport_rule(goal),
                                  (source, iso, image))
        if all(item.subgoals != candidate.subgoals for item in options):
            options.append(candidate)
    return tuple(options)
