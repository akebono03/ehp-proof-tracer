"""Select typed group proof goals from registered fixed claims, never from legacy results."""
from __future__ import annotations

from dataclasses import fields, is_dataclass, replace

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r52_partial_proof import GroupStructureStatus, ProofSearchStatus, make_partial_proof_result
from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
from proof import Relation, RelationType
from unified_statement_registry import AssertionOrigin


_GROUP_STRUCTURES = (DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup)


def registered_group_goal_candidates(bridge, *, n: int, k: int) -> tuple[Relation, ...]:
    """Read concrete Relation components of fixed typed assertions as goals only."""
    target = TodaPrimaryGroup(group_dimension=n + k, sphere_dimension=n)
    candidates: list[Relation] = []

    def inspect(content: object) -> None:
        if isinstance(content, Relation):
            if (content.relation_type is RelationType.EQUALITY
                    and content.lhs == target
                    and isinstance(content.rhs, _GROUP_STRUCTURES)
                    and not any(candidate == content for candidate in candidates)):
                candidates.append(content)
            return
        if is_dataclass(content) and not isinstance(content, type):
            for part in fields(content):
                value = getattr(content, part.name)
                if isinstance(value, (Relation,)) or (is_dataclass(value) and not isinstance(value, type)):
                    inspect(value)
                elif isinstance(value, (tuple, list)):
                    for item in value:
                        if isinstance(item, Relation) or (is_dataclass(item) and not isinstance(item, type)):
                            inspect(item)

    for assertion in bridge.registry._assertions.values():
        if assertion.origin is AssertionOrigin.FIXED_STATEMENT:
            inspect(assertion.content)
    return tuple(candidates)


def search_group_from_registered_goal(*, n: int, k: int, bridge=None, proof_order_catalog=None, goal=None):
    """Search an explicitly supplied typed goal, without treating it as evidence.

    The optional goal is a Relation carrying the asserted structure and generator.
    Legacy n,k-only calls preserve the existing registered-goal selection path.
    """
    make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED)
    if goal is not None:
        if (not isinstance(goal, Relation)
                or goal.relation_type is not RelationType.EQUALITY
                or goal.lhs != TodaPrimaryGroup(n + k, n)
                or not isinstance(goal.rhs, _GROUP_STRUCTURES)):
            raise ValueError("goal must be a typed equality for the requested n,k")
    if bridge is None:
        bridge = build_shared_typed_bridge()
    if goal is None:
        candidates = registered_group_goal_candidates(bridge, n=n, k=k)
        if len(candidates) != 1:
            explanation = (
                "群構造・生成元の型付き証明目標を指定してください"
                if not candidates else
                "群構造の型付き候補が複数あり、証明目標を一意に選択できない"
            )
            return make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(TodaPrimaryGroup(n + k, n),),
                diagnostics=(explanation,),
            )
        candidate = candidates[0]
    else:
        candidate = goal
    if proof_order_catalog is None:
        from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog
        proof_order_catalog, order_diagnostic = resolve_reviewed_order_catalog(
            bridge, n=n, k=k,
        )
        if order_diagnostic is not None:
            return make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(candidate,), diagnostics=(order_diagnostic,),
            )
    # Phase 166 R3-I: select the exact registered source assertion as the
    # statement-order target. Do not reconstruct earlier completed group proofs.
    from phase165_r57_r8_eta_specialization import (
        _is_generic_eta_group_relation, specialize_eta_group_relation,
    )
    matches = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if assertion.component_position is None:
            continue
        if assertion.content == candidate:
            matches.append(assertion.assertion_id)
        elif _is_generic_eta_group_relation(assertion.content):
            try:
                if specialize_eta_group_relation(assertion.content, n) == candidate:
                    matches.append(assertion.assertion_id)
            except ValueError:
                pass
    if len(matches) == 1:
        result = search_shared_group_goal(
            n=n, k=k, group_structure=candidate.rhs, bridge=bridge,
            citing_assertion_id=matches[0],
        )
    else:
        # Preserve the existing fallback for targets without a uniquely
        # registered source assertion; do not infer an artificial position.
        result = search_shared_group_goal(
            n=n, k=k, group_structure=candidate.rhs, bridge=bridge,
            proof_order_catalog=proof_order_catalog,
        )
    if result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate:
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    return result


# R57-R8 REGISTERED GENERIC GOAL SPECIALIZATION
_phase165_r57_r8_previous_registered_group_goal_candidates = registered_group_goal_candidates

def registered_group_goal_candidates(bridge, *, n: int, k: int):
    """Extend the previous R55 selection with derived symbolic-reference goals."""
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r57_r8_eta_specialization import specialized_eta_group_goal_candidates
    existing = _phase165_r57_r8_previous_registered_group_goal_candidates(bridge=bridge, n=n, k=k)
    if not isinstance(existing, tuple):
        raise TypeError("R55 selector must return a tuple")
    group = TodaPrimaryGroup(group_dimension=n+k, sphere_dimension=n)
    typed_bridge = bridge
    candidates = specialized_eta_group_goal_candidates(group, typed_bridge)
    output = list(existing)
    for candidate in candidates:
        if not any(type(candidate) is type(old) and candidate == old for old in output):
            output.append(candidate)
    return tuple(output)
