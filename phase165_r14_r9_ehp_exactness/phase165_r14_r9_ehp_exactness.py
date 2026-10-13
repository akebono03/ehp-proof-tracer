"""Phase 165 R14-R9: typed EHP exactness consequences, no unverified leaves."""
from __future__ import annotations

from homotopy_groups import (
    TodaPrimaryGroup, TodaHopfInvariantMap, TodaSuspensionMap,
    TodaDeltaMap, TodaEHPExactnessWindow, TodaPrimaryGroupZeroStatement,
)
from map_facts import EHP_E_MAP, EHP_H_MAP, EHP_DELTA_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from proof import InferenceRule, PremisePattern
from toda_rules import TodaProp42ExactnessStatement, TodaDeltaZeroStatement


def _ehp_data(h):
    if not isinstance(h, TodaHopfInvariantMap):
        return None
    source, target = h.source_group, h.target_group
    q, n = source.group_dimension, source.sphere_dimension
    if (type(q) is not int or type(n) is not int
            or n < 2 or q < n
            or target != TodaPrimaryGroup(q, 2 * n - 1)):
        return None
    left = TodaPrimaryGroup(q - 1, n - 1)
    right = TodaPrimaryGroup(q - 2, n - 1)
    return left, right


def _injective_inputs(h):
    terms = _ehp_data(h)
    if terms is None:
        return None
    left, _ = terms
    exact = TodaProp42ExactnessStatement(
        TodaEHPExactnessWindow(
            source_term=left,
            middle_term=h.source_group,
            target_term=h.target_group,
            first_map=EHP_E_MAP,
            second_map=EHP_H_MAP,
        )
    )
    return TodaPrimaryGroupZeroStatement(left), exact


def _surjective_inputs(h):
    terms = _ehp_data(h)
    if terms is None:
        return None
    _, right = terms
    delta = TodaDeltaMap(h.target_group, right)
    exact = TodaProp42ExactnessStatement(
        TodaEHPExactnessWindow(
            source_term=h.source_group,
            middle_term=h.target_group,
            target_term=right,
            first_map=EHP_H_MAP,
            second_map=EHP_DELTA_MAP,
        )
    )
    return TodaDeltaZeroStatement(delta), exact


def _guard_injective(premises, bindings):
    zero, exact = (p.conclusion for p in premises)
    w = exact.window
    return (
        isinstance(zero, TodaPrimaryGroupZeroStatement)
        and isinstance(exact, TodaProp42ExactnessStatement)
        and w.first_map == EHP_E_MAP
        and w.second_map == EHP_H_MAP
        and w.source_term == zero.group
        and w.middle_term == TodaPrimaryGroup(
            zero.group.group_dimension + 1,
            zero.group.sphere_dimension + 1,
        )
        and w.target_term == TodaPrimaryGroup(
            w.middle_term.group_dimension,
            2 * w.middle_term.sphere_dimension - 1,
        )
        and _ehp_data(TodaHopfInvariantMap(w.middle_term, w.target_term)) is not None
    )


def _build_injective(premises):
    w = premises[1].conclusion.window
    return MapInjective(TodaHopfInvariantMap(w.middle_term, w.target_term))


def hopf_injective_from_exactness_rule():
    return InferenceRule(
        name="EHP: preceding zero group and exactness imply Hopf injectivity",
        premise_patterns=(
            PremisePattern(statement_type=TodaPrimaryGroupZeroStatement),
            PremisePattern(statement_type=TodaProp42ExactnessStatement),
        ),
        match_guard=_guard_injective,
        conclusion_builder=_build_injective,
    )


def _guard_surjective(premises, bindings):
    delta_zero, exact = (p.conclusion for p in premises)
    w = exact.window
    h = TodaHopfInvariantMap(w.source_term, w.middle_term)
    return (
        isinstance(delta_zero, TodaDeltaZeroStatement)
        and isinstance(exact, TodaProp42ExactnessStatement)
        and _ehp_data(h) is not None
        and w.first_map == EHP_H_MAP
        and w.second_map == EHP_DELTA_MAP
        and delta_zero.map == TodaDeltaMap(w.middle_term, w.target_term)
        and _ehp_data(h)[1] == w.target_term
    )


def _build_surjective(premises):
    w = premises[1].conclusion.window
    return MapSurjective(TodaHopfInvariantMap(w.source_term, w.middle_term))


def hopf_surjective_from_exactness_rule():
    return InferenceRule(
        name="EHP: subsequent zero delta and exactness imply Hopf surjectivity",
        premise_patterns=(
            PremisePattern(statement_type=TodaDeltaZeroStatement),
            PremisePattern(statement_type=TodaProp42ExactnessStatement),
        ),
        match_guard=_guard_surjective,
        conclusion_builder=_build_surjective,
    )


def expand_generic_ehp_hopf_goal(goal):
    if isinstance(goal, MapInjective):
        inputs = _injective_inputs(goal.map)
        if inputs is not None:
            return (GoalExpansion(hopf_injective_from_exactness_rule(), inputs),)
    if isinstance(goal, MapSurjective):
        inputs = _surjective_inputs(goal.map)
        if inputs is not None:
            return (GoalExpansion(hopf_surjective_from_exactness_rule(), inputs),)
    return ()


def audit_pi32_hopf_exactness():
    h = TodaHopfInvariantMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(3, 3))
    injective = expand_generic_ehp_hopf_goal(MapInjective(h))
    surjective = expand_generic_ehp_hopf_goal(MapSurjective(h))
    return {
        "phase": "165 R14-R9",
        "hopf_map": repr(h),
        "injectivity_expansions": len(injective),
        "surjectivity_expansions": len(surjective),
        "injectivity_subgoals": [repr(x) for x in injective[0].subgoals] if injective else [],
        "surjectivity_subgoals": [repr(x) for x in surjective[0].subgoals] if surjective else [],
        "source_certified": False,
        "proof_steps_created_for_toda": 0,
        "full_pytest_run": False,
        "status": "EXACTNESS_OBLIGATIONS_MAPPED_NOT_CERTIFIED",
    }
