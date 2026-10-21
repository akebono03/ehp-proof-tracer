"""Select typed group proof goals from registered fixed claims, never from legacy results."""
from __future__ import annotations

from dataclasses import fields, is_dataclass, replace

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r52_partial_proof import GroupStructureStatus, ProofSearchStatus, make_partial_proof_result
from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
from proof import Relation, RelationType
from unified_statement_registry import AssertionOrigin
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id


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
    """Search typed goals. Zero goals use the same evidenced backward engine."""
    from homotopy_groups import TodaPrimaryGroupZeroStatement
    from phase166_r3af_goal_adapter import database_zero_group_goal_candidates

    target = TodaPrimaryGroup(n + k, n)
    make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED)

    if goal is not None:
        valid_relation = (
            isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and goal.lhs == target
            and isinstance(goal.rhs, _GROUP_STRUCTURES)
        )
        valid_zero = (
            isinstance(goal, TodaPrimaryGroupZeroStatement)
            and goal.group == target
        )
        if not valid_relation and not valid_zero:
            raise ValueError("goal must be a typed group statement for the requested n,k")

    if goal is None:
        zeros = database_zero_group_goal_candidates(n=n, k=k)
        if len(zeros) == 1:
            candidate = zeros[0]
        else:
            if bridge is None:
                bridge = build_shared_typed_bridge()
            candidates = registered_group_goal_candidates(bridge, n=n, k=k)
            if len(candidates) != 1:
                explanation = (
                    "群構造・生成元の型付き証明目標を指定してください"
                    if not candidates else
                    "群構造の型付き候補が複数あり、証明目標を一意に選択できない"
                )
                return make_partial_proof_result(
                    n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                    open_goals=(target,), diagnostics=(explanation,),
                )
            candidate = candidates[0]
    else:
        candidate = goal

    if bridge is None:
        bridge = build_shared_typed_bridge()

    if isinstance(candidate, TodaPrimaryGroupZeroStatement):
        from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
        from phase165_r52_r2_search_adapter import search_registered_partial_proof
        from phase165_r52_r9_shared_math import shared_expansion_provider
        assertions = tuple(bridge.registry._assertions.values())
        if not assertions:
            return make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(candidate,), diagnostics=("型付き命題台帳が空です",),
            )
        # DB goals have no publication assertion. Preserve the existing
        # implicit-target citation policy without inventing a citing ID.
        context_id = assertions[0].assertion_id
        screened = screen_shared_proof_context(
            bridge, goal=candidate, citing_assertion_id=context_id,
        )
        provider = shared_expansion_provider(
            screened, proof_target=candidate,
        )
        return search_registered_partial_proof(
            n=n, k=k, goal=candidate, bridge=screened,
            citing_assertion_id=context_id,
            expansion_provider=provider, lookup_mode="typed_reference",
        )

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
    citing_id = resolve_specialized_goal_citing_id(bridge, candidate)
    search_kwargs = dict(
        n=n, k=k, group_structure=candidate.rhs, bridge=bridge,
        proof_order_catalog=proof_order_catalog,
    )
    if citing_id is not None:
        search_kwargs["citing_assertion_id"] = citing_id
    result = search_shared_group_goal(**search_kwargs)
    if result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate:
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    return result




# R57-R8 REGISTERED GENERIC GOAL SPECIALIZATION
_phase165_r57_r8_previous_registered_group_goal_candidates = registered_group_goal_candidates

def registered_group_goal_candidates(bridge, *, n: int, k: int):
    """Prefer typed DB targets; retain registry fallback for unsupported rows.

    DB data define the goal only, and are never inserted as ProofSteps or
    GIVEN evidence. The registry remains the source of proof premises.
    """
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r57_r8_eta_specialization import specialized_eta_group_goal_candidates
    from phase166_r3af_goal_adapter import database_group_goal_candidates

    database = database_group_goal_candidates(n=n, k=k)
    if database:
        return database
    existing = _phase165_r57_r8_previous_registered_group_goal_candidates(
        bridge=bridge, n=n, k=k,
    )
    if not isinstance(existing, tuple):
        raise TypeError("R55 selector must return a tuple")
    group = TodaPrimaryGroup(group_dimension=n+k, sphere_dimension=n)
    symbolic = specialized_eta_group_goal_candidates(group, bridge)
    output = list(existing)
    for candidate in symbolic:
        if not any(type(candidate) is type(old) and candidate == old for old in output):
            output.append(candidate)
    return tuple(output)

