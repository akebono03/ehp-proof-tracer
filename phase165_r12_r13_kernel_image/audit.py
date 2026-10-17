"""Read-only R12-R13 integration audit (no generated GIVEN leaves)."""
from __future__ import annotations

import json
from pathlib import Path
from expression import GeneratorSymbol, HomotopyElement, Multiple
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r13_kernel_image import (
    SuspensionKernelFreeCyclicStatement, build_concrete_kernel_provider,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from proof import Relation, RelationType


def main():
    bridge = build_shared_typed_bridge()
    eta2 = HomotopyElement("η₂", dimension=2, source=3, target=2,
                           generator=GeneratorSymbol("η", 2))
    goal = SuspensionKernelFreeCyclicStatement(
        TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3)),
        FreeCyclicGroup(Multiple(coefficient=2, expression=eta2)),
    )
    citing = next(iter(bridge.registry._assertions))
    proof_target = Relation(TodaPrimaryGroup(4, 3), object(), relation_type=RelationType.EQUALITY)
    screened = screen_shared_proof_context(bridge, goal=proof_target, citing_assertion_id=citing)
    proposals = build_concrete_kernel_provider(screened)(goal)
    report = {
        "phase": "165 R12-R13",
        "mode": "GENERIC_SIGNED_DELTA_TO_SUSPENSION_KERNEL",
        "screened_signed_delta_proposals": len(proposals),
        "kernel_goal": repr(goal),
        "subgoals": [repr(x) for x in proposals[0].subgoals] if proposals else [],
        "kernel_proof_certified": False,
        "pi43_proof_certified": False,
        "full_pytest_run": False,
    }
    out = Path(__file__).resolve().parent / "audit_result.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Audit saved:", out)


if __name__ == "__main__":
    main()
