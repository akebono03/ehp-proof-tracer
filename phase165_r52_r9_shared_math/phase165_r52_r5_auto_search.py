"""R52-R5: start fresh, typed, registry-backed proof search for a group query.

No historical proof replay and no assumed group-structure answer. A structural
query with no typed conclusion candidate is searched as an open Goal and its
missing registration/rule coverage is reported honestly.
"""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    FreeCyclicGroup,
    TodaPrimaryGroup,
)
from phase165_r52_partial_proof import (
    GroupStructureStatus,
    PartialProofResult,
    ProofSearchStatus,
    make_partial_proof_result,
)
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from proof import Relation, RelationType
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class GroupStructureSearchGoal:
    """A request to determine a group, NOT an assertion that it has a structure."""
    group: TodaPrimaryGroup


def _same(left: object, right: object) -> bool:
    equality = type(left) is type(right) and left == right
    return type(equality) is bool and equality


def _typed_structure_candidates(bridge, group: TodaPrimaryGroup) -> tuple[object, ...]:
    """Select only concrete structural propositions actually present in the registry."""
    candidates: list[object] = []
    group_structures = (FiniteCyclicGroup, FreeCyclicGroup, DirectSumGroup)
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        statement = assertion.content
        if not isinstance(statement, Relation):
            continue
        if statement.relation_type is not RelationType.EQUALITY:
            continue
        if statement.lhs != group or not isinstance(statement.rhs, group_structures):
            continue
        if not any(_same(statement, existing) for existing in candidates):
            candidates.append(statement)
    return tuple(candidates)


def search_group_structure_automatically(
    *, n: int, k: int,
    discovery=None,
) -> PartialProofResult:
    """Discover registered typed propositions and run the canonical prover now.

    SOURCE_ARCHIVE text and pre-existing internal proof results are not premises.
    In particular, a TeX source that has not been typed does not count as a
    structure candidate.
    """
    # Enforce the public R52 domain before attempting any discovery.
    make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED)
    group = TodaPrimaryGroup(group_dimension=n + k, sphere_dimension=n)
    if discovery is None:
        from toda_calculation_facade import build_standard_toda_report
        from toda_calculation_result import TodaCalculationStatus
        from phase165_r52_r9_shared_math import search_shared_group_goal
        report = build_standard_toda_report(n=n, k=k)
        if report.status is TodaCalculationStatus.FOUND and len(report.candidates) == 1:
            group_result = report.candidates[0].source_candidate.group_result
            return search_shared_group_goal(
                n=n, k=k, group_structure=group_result.group_structure,
            )
        from phase165_r9_production_wiring import discover_goal_search_inputs
        discovery = discover_goal_search_inputs()
    bridge = discovery.bridge
    provider = discovery.expansion_provider
    assertions = tuple(bridge.registry._assertions.values())
    structural_candidates = _typed_structure_candidates(bridge, group)
    if not assertions:
        return make_partial_proof_result(
            n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
            open_goals=(GroupStructureSearchGoal(group),),
            diagnostics=("命題台帳に登録主張がなく、型付き探索を開始できない",),
        )

    # In typed_reference mode this id is required solely to validate a
    # registered context; it confers no right to cite that assertion.
    context_id = assertions[0].assertion_id
    goals = structural_candidates or (GroupStructureSearchGoal(group),)
    attempts = tuple(
        search_registered_partial_proof(
            n=n, k=k, goal=goal, bridge=bridge,
            citing_assertion_id=context_id,
            expansion_provider=provider,
            lookup_mode="typed_reference",
        )
        for goal in goals
    )
    unique_steps = []
    open_goals = []
    diagnostics = []
    complete = []
    for attempt in attempts:
        for step in attempt.proven_steps:
            if not any(step is found for found in unique_steps):
                unique_steps.append(step)
        for goal in attempt.open_goals:
            if not any(_same(goal, earlier) for earlier in open_goals):
                open_goals.append(goal)
        diagnostics.extend(attempt.diagnostics)
        if attempt.status is ProofSearchStatus.COMPLETE:
            complete.append(attempt)

    if len(complete) == 1 and len(structural_candidates) == 1:
        result = complete[0]
        return make_partial_proof_result(
            n=n, k=k, status=ProofSearchStatus.COMPLETE,
            structure_status=GroupStructureStatus.KNOWN,
            references=result.references,
            proven_steps=tuple(unique_steps),
            conclusion=result.conclusion,
        )
    if complete:
        diagnostics.append(
            "群構造の候補が複数あるため、一意の最終結論は認定しない"
        )
    if not structural_candidates:
        diagnostics.append(
            "群構造について型付きの具体的候補命題が未登録。"
            "SOURCE_ARCHIVE の文字列は証明前提に昇格させない"
        )
    return make_partial_proof_result(
        n=n, k=k,
        status=ProofSearchStatus.PARTIAL if unique_steps else ProofSearchStatus.SEARCH_FAILED,
        proven_steps=tuple(unique_steps),
        open_goals=tuple(open_goals) or (GroupStructureSearchGoal(group),),
        diagnostics=tuple(dict.fromkeys(diagnostics)),
    )
