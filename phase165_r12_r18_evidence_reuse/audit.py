"""Run canonical pi3^2 search and audit eligible generator evidence without shortcuts."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from hopf_facts import ETA_2
from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
from phase165_r12_r18_evidence_reuse import extract_completed_root, find_screened_generator_witness
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from proof import Relation, RelationType


def main() -> None:
    bridge = build_shared_typed_bridge()
    source, target = TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3)
    mapping = TodaSuspensionMap(source, target)
    structure = FreeCyclicGroup(ETA_2)
    goal = Relation(source, structure, RelationType.EQUALITY)
    result = search_shared_group_goal(n=2, k=1, group_structure=structure, bridge=bridge)
    pi32 = extract_completed_root(result, goal)
    from expression import eta
    eta3 = eta(3)
    suspension = find_screened_generator_witness(bridge, GeneratorSuspension(mapping, ETA_2, eta3))
    image = find_screened_generator_witness(bridge, GeneratorImage(mapping, ETA_2, eta3))
    report = {
        "phase": "165 R12-R18",
        "canonical_pi32_search_status": result.status.value,
        "pi32_root_status": pi32.status,
        "pi32_blocker": pi32.reason,
        "pi32_root_inference": pi32.proof is not None,
        "generator_suspension_fixed_witness": suspension.status,
        "generator_image_fixed_witness": image.status,
        "generator_evidence_verified": any(x.proof is not None for x in (suspension, image)),
        "homomorphism_presentation_certified": False,
        "pi43_proof_certified": False,
        "full_pytest_run": False,
    }
    report["status"] = ("PI32_PROOF_REUSABLE" if pi32.proof is not None
                        else "PI32_PROOF_REUSE_UNRESOLVED")
    path = Path(__file__).with_name("audit_result.json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Audit saved:", path)


if __name__ == "__main__":
    main()
