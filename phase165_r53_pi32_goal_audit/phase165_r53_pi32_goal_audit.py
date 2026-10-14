"""Read-only audit of the explicit pi_3^2 goal via canonical shared search."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from hopf_facts import ETA_2
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge,
    search_shared_group_goal,
    shared_expansion_provider,
)
from proof import ProofRule, Relation


@dataclass(frozen=True)
class Pi32GoalAudit:
    phase: str
    goal: str
    status: str
    complete: bool
    root_expansion_count: int
    root_expansion_rules: tuple[str, ...]
    typed_given_count: int
    proven_step_count: int
    proof_step_rules: tuple[str, ...]
    open_goals: tuple[str, ...]
    diagnostics: tuple[str, ...]
    full_pytest_run: bool = False


def pi32_explicit_goal() -> Relation:
    return Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))


def audit_pi32_explicit_goal(bridge=None) -> Pi32GoalAudit:
    if bridge is None:
        bridge = build_shared_typed_bridge()
    goal = pi32_explicit_goal()
    before = tuple(bridge.proof_links)
    expansions = shared_expansion_provider(bridge)(goal)
    result = search_shared_group_goal(
        n=2, k=1, group_structure=goal.rhs, bridge=bridge
    )
    if tuple(bridge.proof_links) != before:
        raise AssertionError("read-only audit mutated source proof links")
    return Pi32GoalAudit(
        phase="165-R53",
        goal=repr(goal),
        status=result.status.value,
        complete=result.conclusion == goal and not result.open_goals,
        root_expansion_count=len(expansions),
        root_expansion_rules=tuple(
            getattr(option.rule, "name", type(option.rule).__name__)
            for option in expansions
        ),
        typed_given_count=sum(
            link.step is not None and link.step.rule is ProofRule.GIVEN
            for link in bridge.proof_links
        ),
        proven_step_count=len(result.proven_steps),
        proof_step_rules=tuple(step.rule.name for step in result.proven_steps),
        open_goals=tuple(repr(item) for item in result.open_goals),
        diagnostics=result.diagnostics,
    )


def main() -> None:
    print(json.dumps(asdict(audit_pi32_explicit_goal()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
