"""Audit the actual citation-screened E surjectivity derivation."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r14_kernel_closure import summarize_proof_ancestry
from phase165_r12_r15_toda51 import (
    prove_surjectivity_in_screened_context, proof_has_toda51_zero_ancestor,
)
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from proof import Relation, RelationType


def main() -> None:
    bridge = build_shared_typed_bridge()
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3)))
    target = Relation(TodaPrimaryGroup(4, 3), object(), relation_type=RelationType.EQUALITY)
    result = prove_surjectivity_in_screened_context(
        goal, bridge,
        citing_assertion_id=next(iter(bridge.registry._assertions)),
        proof_target=target,
    )
    report = {
        "phase": "165 R12-R15",
        "mode": "TODA_51_CITED_ZERO_SPECIALIZATION_SURJECTIVITY",
        "status": result.status,
        "blocker": result.blocker,
        "surjectivity_proof_certified": result.status == "CERTIFIED",
        "toda51_zero_ancestor": proof_has_toda51_zero_ancestor(result.proof) if result.proof else False,
        "proof_ancestry": summarize_proof_ancestry(result.proof) if result.proof else None,
        "pi43_proof_certified": False,
        "full_pytest_run": False,
    }
    output = Path(__file__).resolve().parent / "audit_result.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Audit saved:", output)


if __name__ == "__main__":
    main()
