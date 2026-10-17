"""Report actual recursive proof certification; fail closed on missing sources."""
from __future__ import annotations
import json
from pathlib import Path
from expression import GeneratorSymbol, HomotopyElement, Multiple
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
from phase165_r12_r14_kernel_closure import prove_kernel_in_screened_context, summarize_proof_ancestry
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from proof import Relation, RelationType


def main() -> None:
    bridge = build_shared_typed_bridge()
    eta = HomotopyElement("η₂", dimension=2, source=3, target=2, generator=GeneratorSymbol("η", 2))
    goal = SuspensionKernelFreeCyclicStatement(
        TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3)),
        FreeCyclicGroup(Multiple(coefficient=2, expression=eta)),
    )
    target = Relation(TodaPrimaryGroup(4, 3), object(), relation_type=RelationType.EQUALITY)
    result = prove_kernel_in_screened_context(
        goal, bridge, citing_assertion_id=next(iter(bridge.registry._assertions)),
        proof_target=target,
    )
    report = {
        "phase": "165 R12-R14",
        "mode": "ACTUAL_SCREENED_RECURSIVE_KERNEL_PROOF",
        "status": result.status,
        "blocker": result.blocker,
        "kernel_goal": repr(goal),
        "kernel_proof_certified": result.status == "CERTIFIED",
        "proof_ancestry": summarize_proof_ancestry(result.proof) if result.proof is not None else None,
        "pi43_proof_certified": False,
        "full_pytest_run": False,
    }
    destination = Path(__file__).resolve().parent / "audit_result.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Audit saved:", destination)


if __name__ == "__main__":
    main()
