"""Read-only check of the cited (5.1) specialization through shared search."""
from __future__ import annotations

import json
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
from phase165_r52_partial_proof import ProofSearchStatus


def main() -> None:
    bridge = build_shared_typed_bridge()
    generator = HomotopyElement(
        name="ι_5", dimension=5,
        generator=GeneratorSymbol(family="ι", index=5),
    )
    result = search_shared_group_goal(
        n=5, k=0, group_structure=FreeCyclicGroup(generator), bridge=bridge,
    )
    state = getattr(result.status, "value", str(result.status))
    report = {
        "phase": "165 R57-R20",
        "target": "pi_5^5",
        "status": state,
        "proven_step_count": len(result.proven_steps),
        "open_goals": [repr(goal) for goal in result.open_goals],
        "diagnostics": list(result.diagnostics),
        "full_pytest_run": False,
    }
    dest = Path(__file__).with_name("specialization_audit.json")
    dest.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf8")
    print("R57-R20 pi_5^5 search status:", state)
    print("R57-R20 proven steps:", len(result.proven_steps))
    print("R57-R20 unresolved goals:", len(result.open_goals))
    print("R57-R20 audit:", dest)


if __name__ == "__main__":
    main()
