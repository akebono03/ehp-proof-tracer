"""Report common EHP proof ancestry and the intentionally unresolved zero target."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup, TodaSuspensionMap
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import build_adopted_prop42_general_reference, build_prop42_specialization_provider
from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement, expand_ehp_exactness_consequences, proof_has_general_prop42_ancestor
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from proof import ProofRule


def main() -> None:
    bridge = build_adopted_prop42_general_reference()
    source_id = next(iter(bridge.registry._assertions))
    specialize = build_prop42_specialization_provider(bridge)

    def provider(goal):
        return expand_ehp_exactness_consequences(goal) + specialize(goal)

    windows = {
        "pi32_e_h": TodaEHPExactnessWindow(TodaPrimaryGroup(2, 1), TodaPrimaryGroup(3, 2), TodaPrimaryGroup(3, 3), EHP_E_MAP, EHP_H_MAP),
        "pi43_delta_e": TodaEHPExactnessWindow(TodaPrimaryGroup(5, 5), TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3), EHP_DELTA_MAP, EHP_E_MAP),
        "pi43_e_h": TodaEHPExactnessWindow(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3), TodaPrimaryGroup(4, 5), EHP_E_MAP, EHP_H_MAP),
    }
    results = {}
    for name, window in windows.items():
        step = reconstruct_registered_goal(
            EHPImageEqualsKernelStatement(window), bridge,
            citing_assertion_id=source_id, expansion_provider=provider,
            lookup_mode="typed_reference",
        )
        results[name] = {
            "inference": step.rule is ProofRule.INFERENCE,
            "specialization_inference": step.premises[0].rule is ProofRule.INFERENCE,
            "has_general_prop42_given_ancestor": proof_has_general_prop42_ancestor(step),
        }
    e_surj = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3)))
    required = expand_ehp_exactness_consequences(e_surj)[0].subgoals
    report = {
        "phase": "165 R12-R12",
        "mode": "GENERIC_EHP_CONSEQUENCE_AND_PROVENANCE",
        "results": results,
        "surjectivity_zero_target_subgoal": repr(required[1]),
        "surjectivity_certified": False,
        "specific_kernel_multiple_derived": False,
        "pi43_proof_certified": False,
        "full_pytest_run": False,
    }
    path = Path(__file__).resolve().parent / "audit_result.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Audit saved:", path)


if __name__ == "__main__":
    main()
