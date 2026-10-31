"""Phase 171 R20R11 canonical public-search audit with local, visible output."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase171_r20r10_read_only_frontier_audit.audit import audit_public
from toda_rules import TodaDeltaZeroStatement

HERE = Path(__file__).resolve().parent
REPORT = HERE / "output" / "audit.json"


def run() -> dict[str, object]:
    public, trace = audit_public()
    h7 = MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))
    delta0 = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 5), TodaPrimaryGroup(5, 2),
    ))
    e_injective = MapInjective(TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 3),
    ))
    report = {
        "phase": "171-R20R11",
        "mode": "CANONICAL_PUBLIC_SEARCH_AFTER_VERIFIED_PRIOR_HOPF_RULE",
        "public_status": public["public_status"],
        "public_complete": public["public_complete"],
        "h7_surjectivity_proved": trace.has("proved", h7),
        "delta_zero_proved": trace.has("proved", delta0),
        "e_injectivity_proved": trace.has("proved", e_injective),
        "public_open_goals": public["public_open_goals"],
        "public_diagnostics": public["public_diagnostics"],
        "unresolved_details": public["unresolved_details"],
        "public_accepted_steps": public["public_accepted_steps"],
        "trace_events": public["traced_events"],
        "new_given_added_by_patch": 0,
        "completed_proofs_imported": False,
        "full_pytest": False,
        "web_verified": False,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R20R11_H7_SURJECTIVE=" + str(report["h7_surjectivity_proved"]), flush=True)
    print("PHASE171_R20R11_DELTA_ZERO=" + str(report["delta_zero_proved"]), flush=True)
    print("PHASE171_R20R11_E_INJECTIVE=" + str(report["e_injectivity_proved"]), flush=True)
    print("PHASE171_R20R11_PUBLIC_STATUS=" + str(report["public_status"]), flush=True)
    print("PHASE171_R20R11_PUBLIC_COMPLETE=" + str(report["public_complete"]), flush=True)
    print("PHASE171_R20R11_UNRESOLVED=" + str(len(report["unresolved_details"])), flush=True)
    print("PHASE171_R20R11_REPORT=" + str(REPORT), flush=True)
    print("PHASE171_R20R11_NEW_GIVEN=0", flush=True)
    print("PHASE171_R20R11_COMPLETED_PROOFS_IMPORTED=False", flush=True)
    if not report["h7_surjectivity_proved"]:
        print("PHASE171_R20R11_RESULT=FAIL_FIRST_HOPF_FRONTIER", flush=True)
        raise RuntimeError("first public-search Hopf frontier remains unresolved; inspect local audit.json")
    print("PHASE171_R20R11_RESULT=PASS_FIRST_HOPF_FRONTIER", flush=True)
    return report


if __name__ == "__main__":
    run()
