"""Audit unique η proof and finite cardinality after the guarded R20 patch."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase171_r2j_r4_r9_r20_eta_route_precedence.install import git_read, preflight

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output" / "audit.json"


def probe_right_and_cardinality() -> dict:
    """Independently reconstruct goals in actual public and R2I source contexts."""
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    from phase171_r2j_r4_r9_r18_cardinality_premise_audit.audit import (
        cardinality_route, probe_premise,
    )
    from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
    from phase171_r2j_r4_r9_r20_eta_route_precedence.source import (
        ETA_RULE, SCALAR_RULE,
    )

    screened, group_goal, citing = _screened_context()
    contexts: list[object] = []
    public = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=group_goal,
        context_sink=contexts.append,
    )
    if len(contexts) != 1:
        raise RuntimeError("expected one public proof context")
    records = {}
    for label, context in (("screened", screened), ("public", contexts[0])):
        provider = shared_expansion_provider(context, proof_target=group_goal)
        cardinality = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
        route = cardinality_route(provider, cardinality)
        right = route.subgoals[2]
        candidates = provider(right)
        rule_names = [getattr(item.rule, "name", "") for item in candidates]
        right_result, _ = probe_premise(right, provider, context, citing, group_goal)
        cardinality_result, _ = probe_premise(cardinality, provider, context, citing, group_goal)
        records[label] = {
            "rule_names": rule_names,
            "eta_routes": rule_names.count(ETA_RULE),
            "redundant_scalar_routes": rule_names.count(SCALAR_RULE),
            "right_status": right_result["status"],
            "right_error": right_result["error"],
            "cardinality_status": cardinality_result["status"],
            "cardinality_error": cardinality_result["error"],
            "given_source_ids": right_result.get("source_ids"),
        }
    return {
        "phase": "171-R2J-R4-R9-R20",
        "mode": "GUARDED_ETA_SPECIALIZATION_ROUTE_PRECEDENCE",
        "public_root_status": public.status.value,
        "contexts": records,
        "new_given": 0,
        "trust_boundary_modified": False,
        "completed_proof_imported": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    ready = preflight()
    before = git_read("status", "--porcelain", "--untracked-files=no")
    report = probe_right_and_cardinality()
    after = git_read("status", "--porcelain", "--untracked-files=no")
    if before != after:
        raise RuntimeError("tracked working files changed during R20 read-only audit")
    report["head"] = ready["head"]
    report["tracked_source_status_unchanged"] = True
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R20_PUBLIC_ROOT=" + report["public_root_status"], flush=True)
    for name, value in report["contexts"].items():
        print("PHASE171_R20_" + name.upper() + "_RIGHT=" + value["right_status"], flush=True)
        print("PHASE171_R20_" + name.upper() + "_CARDINALITY=" + value["cardinality_status"], flush=True)
        print("PHASE171_R20_" + name.upper() + "_ETA_ROUTES=" + str(value["eta_routes"]), flush=True)
        print("PHASE171_R20_" + name.upper() + "_SCALAR_ROUTES=" + str(value["redundant_scalar_routes"]), flush=True)
    assert all(x["eta_routes"] == 1 and x["redundant_scalar_routes"] == 0
               and x["right_status"] == "proved" for x in report["contexts"].values()), (
        "R20 did not uniquely reconstruct the cited right group")
    print("PHASE171_R20_NEW_GIVEN=0", flush=True)
    print("PHASE171_R20_RESULT=PASS_GUARDED_PATCH_AUDIT", flush=True)


if __name__ == "__main__":
    main()
