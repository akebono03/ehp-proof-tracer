"""R14-R14: generic diagonal suspension isomorphism and Prop.4.2 scope review."""
from __future__ import annotations
from dataclasses import dataclass

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import (
    FreeCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap,
    TodaSuspensionIsomorphismStatement,
)
from proof import InferenceRule, PremisePattern, Relation, RelationType
from phase165_r3_recursive_search import GoalExpansion
from phase165_r14_r13_source_review import collect_prop42_source_reviews
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge


@dataclass(frozen=True)
class GeneratorSuspension:
    map: TodaSuspensionMap
    source_generator: HomotopyElement
    target_generator: HomotopyElement


def _diagonal_shape(suspension):
    if not isinstance(suspension, TodaSuspensionMap):
        return False
    a, b = suspension.source_group, suspension.target_group
    n = a.sphere_dimension
    return (
        type(n) is int and n >= 1
        and a == TodaPrimaryGroup(n, n)
        and b == TodaPrimaryGroup(n + 1, n + 1)
    )


def _iota(n):
    return HomotopyElement(
        name="ι" + str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")),
        dimension=n, source=n, target=n,
        generator=GeneratorSymbol(family="ι", index=n),
    )


def diagonal_suspension_subgoals(suspension):
    if not _diagonal_shape(suspension):
        return None
    a, b = suspension.source_group, suspension.target_group
    iota_a = _iota(a.sphere_dimension)
    iota_b = _iota(b.sphere_dimension)
    return (
        Relation(a, FreeCyclicGroup(iota_a)),
        Relation(b, FreeCyclicGroup(iota_b)),
        GeneratorSuspension(suspension, iota_a, iota_b),
    )


def _diagonal_guard(premises, bindings):
    source, target, generator_map = (x.conclusion for x in premises)
    if not isinstance(generator_map, GeneratorSuspension):
        return False
    f = generator_map.map
    return (
        _diagonal_shape(f)
        and isinstance(source, Relation)
        and isinstance(target, Relation)
        and source.relation_type is RelationType.EQUALITY
        and target.relation_type is RelationType.EQUALITY
        and isinstance(source.rhs, FreeCyclicGroup)
        and isinstance(target.rhs, FreeCyclicGroup)
        and source.lhs == f.source_group
        and target.lhs == f.target_group
        and source.rhs.generator == generator_map.source_generator
        and target.rhs.generator == generator_map.target_generator
        and generator_map.source_generator == _iota(f.source_group.sphere_dimension)
        and generator_map.target_generator == _iota(f.target_group.sphere_dimension)
    )


def _build_diagonal_iso(premises):
    return TodaSuspensionIsomorphismStatement(map=premises[2].conclusion.map)


def diagonal_suspension_isomorphism_rule():
    return InferenceRule(
        name="diagonal free cyclic suspension on generators implies isomorphism",
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(statement_type=GeneratorSuspension),
        ),
        match_guard=_diagonal_guard,
        conclusion_builder=_build_diagonal_iso,
    )


def expand_diagonal_suspension(goal):
    if not isinstance(goal, TodaSuspensionIsomorphismStatement):
        return ()
    subgoals = diagonal_suspension_subgoals(goal.map)
    if subgoals is None:
        return ()
    return (GoalExpansion(diagonal_suspension_isomorphism_rule(), subgoals),)


def review_prop42_scope(bridge):
    """Preserve both original source candidates without asserting a false clause."""
    reviews = collect_prop42_source_reviews(bridge)
    return tuple({
        "assertion_id": r.assertion_id,
        "locator": r.locator,
        "source_text": r.source_text,
        "exactness_words_found": r.exactness_words_found,
        "mathematical_clause_selected": False,
        "applicability_verified": False,
        "proof_eligible": False,
    } for r in reviews)


def audit_r14(bridge=None):
    if bridge is None:
        bridge, _ = build_phase165_r5_manifest_bridge()
    goal = TodaSuspensionIsomorphismStatement(
        TodaSuspensionMap(TodaPrimaryGroup(1,1), TodaPrimaryGroup(2,2))
    )
    candidates = review_prop42_scope(bridge)
    expansions = expand_diagonal_suspension(goal)
    return {
        "phase": "165 R14-R14",
        "prop42_source_candidates": candidates,
        "prop42_single_clause_selected": False,
        "prop42_applicability_certified": False,
        "diagonal_goal": repr(goal),
        "diagonal_expansions": len(expansions),
        "diagonal_subgoals": [repr(g) for g in expansions[0].subgoals] if expansions else [],
        "certified_new_leaves": 0,
        "toda_proof_steps_created": 0,
        "pi32_proved": False,
        "status": "DIAGONAL_INFERENCE_READY_PROP42_SOURCE_REVIEW_UNRESOLVED",
        "full_pytest_run": False,
    }
