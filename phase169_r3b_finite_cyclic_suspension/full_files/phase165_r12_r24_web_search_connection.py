"""Generic backward presentation and evidenced suspension transport for cyclic groups.

Registered database group presentations are candidate Goals only. An isomorphism,
a source group relation, and a generator image must each be proved separately.
"""
from __future__ import annotations

from expression import Composition
from homotopy_groups import (
    FiniteCyclicGroup,
    TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement,
    TodaSuspensionMap,
)
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r12_r5_structure_bridge import finite_cyclic_structure_as_relation_inference_rule
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, Relation, RelationType


def finite_cyclic_suspension_transport_inference_rule() -> InferenceRule:
    """Transport a cyclic presentation only from three verified typed premises."""
    def guard(premises, bindings):
        if len(premises) != 3:
            return False
        source, isomorphism, image = (step.conclusion for step in premises)
        if (not isinstance(source, Relation)
                or source.relation_type is not RelationType.EQUALITY
                or not isinstance(source.rhs, FiniteCyclicGroup)
                or type(source.rhs.order) is not int
                or source.rhs.order < 1
                or not isinstance(isomorphism, TodaSuspensionIsomorphismStatement)
                or not isinstance(image, GeneratorImage)):
            return False
        mapping = isomorphism.map
        if not isinstance(mapping, TodaSuspensionMap):
            return False
        domain = mapping.source_group
        codomain = mapping.target_group
        if (not isinstance(domain, TodaPrimaryGroup)
                or not isinstance(codomain, TodaPrimaryGroup)
                or type(domain.group_dimension) is not int
                or type(domain.sphere_dimension) is not int
                or domain.group_dimension < domain.sphere_dimension
                or domain.sphere_dimension < 2):
            return False
        return (
            source.lhs == domain
            and codomain == TodaPrimaryGroup(
                domain.group_dimension + 1,
                domain.sphere_dimension + 1,
            )
            and image.map == mapping
            and image.source_generator == source.rhs.generator
        )

    def conclusion(premises):
        source, isomorphism, image = (step.conclusion for step in premises)
        return Relation(
            lhs=isomorphism.map.target_group,
            rhs=FiniteCyclicGroup(
                order=source.rhs.order,
                generator=image.target_generator,
            ),
            relation_type=RelationType.EQUALITY,
        )

    return InferenceRule(
        name="finite cyclic presentation transported by proved suspension isomorphism",
        description=(
            "Transport a finite cyclic group presentation by an actually proved "
            "suspension isomorphism and an actually proved generator image."
        ),
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(statement_type=TodaSuspensionIsomorphismStatement),
            PremisePattern(statement_type=GeneratorImage),
        ),
        match_guard=guard,
        conclusion_builder=conclusion,
    )


def expand_finite_cyclic_relation(goal: object) -> tuple[GoalExpansion, ...]:
    """Propose typed derivations; no source goal or map property is accepted as fact."""
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return ()
    if not isinstance(goal.rhs, FiniteCyclicGroup):
        return ()
    if type(goal.rhs.order) is not int or goal.rhs.order < 1:
        return ()
    source = CyclicStructureStatement(goal.lhs, goal.rhs.generator, goal.rhs.order)
    options = [GoalExpansion(finite_cyclic_structure_as_relation_inference_rule(), (source,))]

    # Phase 169: generate one structural 2-stem candidate from a separately
    # registered lower-dimensional Goal, not from a stored or assumed proof.
    if not isinstance(goal.lhs, TodaPrimaryGroup):
        return tuple(options)
    q = goal.lhs.group_dimension
    n = goal.lhs.sphere_dimension
    if (type(q) is not int or type(n) is not int
            or n < 3 or q != n + 2
            or not isinstance(goal.rhs.generator, Composition)):
        return tuple(options)

    from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
    candidates = database_structured_group_goal_candidates(n=n - 1, k=2)
    if len(candidates) != 1:
        return tuple(options)
    lower = candidates[0]
    if (not isinstance(lower, Relation)
            or lower.relation_type is not RelationType.EQUALITY
            or lower.lhs != TodaPrimaryGroup(q - 1, n - 1)
            or not isinstance(lower.rhs, FiniteCyclicGroup)
            or lower.rhs.order != goal.rhs.order
            or not isinstance(lower.rhs.generator, Composition)):
        return tuple(options)

    suspension = TodaSuspensionMap(source_group=lower.lhs, target_group=goal.lhs)
    options.append(GoalExpansion(
        finite_cyclic_suspension_transport_inference_rule(),
        (
            lower,
            TodaSuspensionIsomorphismStatement(map=suspension),
            GeneratorImage(
                map=suspension,
                source_generator=lower.rhs.generator,
                target_generator=goal.rhs.generator,
            ),
        ),
    ))
    return tuple(options)
