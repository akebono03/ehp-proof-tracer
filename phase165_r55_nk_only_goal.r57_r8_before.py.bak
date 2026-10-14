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


def search_group_from_registered_goal(*, n: int, k: int, bridge=None):
    """Resolve a unique sourced target and run the existing screened backward search."""
    make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED)
    if bridge is None:
        bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=n, k=k)
    if len(candidates) != 1:
        explanation = (
            "群構造・生成元の型付き証明目標が文献命題台帳に未登録"
            if not candidates else
            "群構造の型付き候補が複数あり、証明目標を一意に選択できない"
        )
        return make_partial_proof_result(
            n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
            open_goals=(TodaPrimaryGroup(n + k, n),),
            diagnostics=(explanation,),
        )
    candidate = candidates[0]
    # The candidate is a requested conclusion, NEVER a GIVEN proof premise.
    # search_shared_group_goal screens exact-root fixed assertions.
    result = search_shared_group_goal(n=n, k=k, group_structure=candidate.rhs, bridge=bridge)
    if (result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate):
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    return result
