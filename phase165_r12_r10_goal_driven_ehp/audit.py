"""Read-only audit of goal-derived Proposition 4.2 EHP windows."""
from __future__ import annotations

import json
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r10_goal_driven_ehp import (
    exactness_goals_in_context, goal_exactness_obligations,
)
from phase165_r14_r26_prop42_typed import bind_proposition42
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from proof import Relation, RelationType


def main() -> None:
    goal = Relation(
        lhs=TodaPrimaryGroup(4, 3),
        rhs=FiniteCyclicGroup(2, HomotopyElement(
            name="η_3", dimension=3, source=4, target=3,
            generator=GeneratorSymbol(family="η", index=3),
        )),
        relation_type=RelationType.EQUALITY,
    )
    requested = goal_exactness_obligations(goal)
    # R7 has its own proof-use screening. Never treat this raw/shared bridge
    # as a screened citation context or promote its matches to proof leaves.
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    shared = build_shared_typed_bridge()
    raw_matches = exactness_goals_in_context(requested, shared)
    source, _ = build_phase165_r5_manifest_bridge()
    binding = bind_proposition42(source, n=requested.prop42_n, i=requested.prop42_i)
    report = {
        "phase": "165 R12-R10",
        "mode": "READ_ONLY_GOAL_DRIVEN_EHP_SOURCE_MATCH",
        "goal": repr(goal),
        "source_locator": "Proposition 4.2 (4.4)",
        "specialization_n": requested.prop42_n,
        "specialization_i": requested.prop42_i,
        "required_delta_e": repr(requested.delta_e),
        "required_e_h": repr(requested.e_h),
        "source_delta_e_formula_matches": binding.typed_statement == requested.delta_e,
        "source_tex_checked": binding.adopted_tex_matched,
        "source_strict_citation_eligible": binding.proof_eligible_in_strict_search,
        "raw_shared_exact_window_matches_not_citation_approved": raw_matches,
        "r7_proof_order_reapplied_in_audit": False,
        "unrelated_previous_windows_selected": False,
        "proof_steps_created": 0,
        "exactness_certified": False,
        "pi43_proof_certified": False,
        "full_pytest_run": False,
    }
    out = Path(__file__).with_name("audit_result.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Audit saved:", out)


if __name__ == "__main__":
    main()
