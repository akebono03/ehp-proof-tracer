"""Phase 165 R52-R20: read-only inspection of pi_4^3 search readiness.

No ProofStep is created or certified by this audit.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider
from proof import ProofRule, Relation


@dataclass(frozen=True)
class Pi43Audit:
    target: str
    status: str
    proof_complete: bool
    root_expansion_count: int
    root_expansion_rule_names: tuple[str, ...]
    registered_pi32_claims: tuple[str, ...]
    registered_delta_iota5_claims: tuple[str, ...]
    linked_pi32_given_count: int
    linked_delta_iota5_given_count: int
    proven_step_count: int
    open_goals: tuple[str, ...]
    diagnostics: tuple[str, ...]
    missing_obligations: tuple[str, ...]
    full_pytest_run: bool = False


def pi43_goal() -> Relation:
    eta3 = HomotopyElement(
        name="η₃", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="η", index=3),
    )
    return Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(order=2, generator=eta3))


def audit_pi43(bridge=None) -> Pi43Audit:
    """Observe existing typed claims, links, expansions and search without mutation."""
    if bridge is None:
        bridge = build_shared_typed_bridge()
    goal = pi43_goal()
    entries = tuple(bridge.registry._assertions.values())
    pi32 = tuple(a for a in entries if (
        "pi3_2_group_relation" in a.assertion_id or
        (isinstance(a.content, Relation) and a.content.lhs == TodaPrimaryGroup(3, 2))
    ))
    delta = tuple(a for a in entries if "delta_iota5_relation" in a.assertion_id)
    given_ids = {
        link.assertion_id for link in bridge.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    }
    expansions = shared_expansion_provider(bridge)(goal)
    result = search_shared_group_goal(n=3, k=1, group_structure=goal.rhs, bridge=bridge)
    missing = []
    if not any(a.assertion_id in given_ids for a in pi32):
        missing.append("pi3_2_typed_given_not_linked_in_current_bridge")
    if not any(a.assertion_id in given_ids for a in delta):
        missing.append("delta_iota5_typed_given_not_linked_in_current_bridge")
    if not expansions:
        missing.append("no_backward_expansion_for_pi43_group_goal")
    if result.conclusion is None:
        missing.append("pi43_proof_not_completed")
    return Pi43Audit(
        target=repr(goal), status=result.status.value,
        proof_complete=result.conclusion == goal,
        root_expansion_count=len(expansions),
        root_expansion_rule_names=tuple(getattr(x.rule, "name", type(x.rule).__name__) for x in expansions),
        registered_pi32_claims=tuple(a.assertion_id for a in pi32),
        registered_delta_iota5_claims=tuple(a.assertion_id for a in delta),
        linked_pi32_given_count=sum(a.assertion_id in given_ids for a in pi32),
        linked_delta_iota5_given_count=sum(a.assertion_id in given_ids for a in delta),
        proven_step_count=len(result.proven_steps),
        open_goals=tuple(repr(x) for x in result.open_goals),
        diagnostics=result.diagnostics,
        missing_obligations=tuple(missing),
    )


def main() -> None:
    print(json.dumps(asdict(audit_pi43()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
