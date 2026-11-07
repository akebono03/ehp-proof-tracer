"""Check the completed R18 gate and truthful, profile-local evidence revalidation."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from phase174_r3_r7_r18r2_local_evidence_recovery.patch import (
    verify_git_and_source,
)

PHASE = "174-R3-R7-R18R2"
EXPECTED_R18_GATE = "PASS_ISOLATED_GENERIC_DELTA_IMAGE_SURJECTIVITY_FRONTIER"
EXPECTED_REPORT = (
    Path("EHPProofTracerAudit") / "phase174_r3_r7_r18" / "delta_image_frontier.json"
)


def verify_public_report(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R18"
            or report.get("gate") != EXPECTED_R18_GATE
            or report.get("new_group_given") != 0
            or report.get("new_math_rules_in_production") != 0
            or report.get("full_pytest_run") is not False
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R18 public mathematical boundary did not pass")
    prior = report.get("prior_evidence")
    live = report.get("live")
    if not isinstance(prior, dict) or not isinstance(live, dict):
        raise RuntimeError("R18 prior evidence or live frontier missing")
    expected_prior = ("174-R3-R7-R17", "174-R3-R7-R17R1")
    if not all(key in prior for key in expected_prior):
        raise RuntimeError("R17 and historical source cannot be silently omitted")
    recovery = prior.get("recovery")
    if recovery is not None:
        if (not isinstance(recovery, dict)
                or recovery.get("mode") != "LIVE_REVALIDATED_NO_SYNTHETIC_REPORT"
                or recovery.get("public_root_candidates") != 1
                or recovery.get("delta_surjectivity_candidates") != 0
                or recovery.get("verified_steps") != 0
                or recovery.get("corrected_historical_test_pinned_by_source_guard") is not True
                or not recovery.get("missing_local_reports")):
            raise RuntimeError("R17 live evidence recovery was not verified")
    if (live.get("public_root_proposals") != 1
            or live.get("public_delta_surjectivity_proposals") != 0
            or live.get("isolated_delta_surjectivity_proposals") != 1
            or live.get("new_proof_steps_created") != 0
            or live.get("completion_claimed") is not False
            or live.get("production_provider_changed") is not False
            or live.get("search_status") == "complete"):
        raise RuntimeError("R18 has lost its unfinished-proof boundary")
    return {
        "phase": PHASE,
        "r18_gate": report["gate"],
        "evidence_mode": "LIVE_RECOVERY" if recovery is not None else "VALIDATED_LOCAL_REPORTS",
        "missing_local_r17_reports": recovery.get("missing_local_reports", []) if recovery is not None else [],
        "public_root_candidates": live["public_root_proposals"],
        "public_delta_surjectivity_candidates": live["public_delta_surjectivity_proposals"],
        "isolated_delta_surjectivity_candidates": live["isolated_delta_surjectivity_proposals"],
        "root_complete": False,
        "new_group_given": 0,
        "new_production_rules": 0,
        "full_pytest_run": False,
        "gate": "PASS_R18_LIVE_R17_BOUNDARY_REVALIDATED_NO_PRIOR_JSON_COPY",
    }


def audit_path() -> Path:
    local = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return local / EXPECTED_REPORT


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    state = verify_git_and_source()
    if state["source_state"] != "R18R2_EVIDENCE_REVALIDATION_INSTALLED":
        raise RuntimeError("R18R2 source correction is not installed")
    report_file = audit_path()
    if not report_file.is_file():
        raise RuntimeError("R18 final live report is missing: " + str(report_file))
    report = json.loads(report_file.read_text(encoding="utf-8-sig"))
    verified = verify_public_report(report)
    print("PHASE174_R3R7R18R2_SOURCE_GUARD=PASS")
    print("PHASE174_R3R7R18R2_EVIDENCE_MODE=" + verified["evidence_mode"])
    print("PHASE174_R3R7R18R2_PUBLIC_ROOT_CANDIDATES=" + str(verified["public_root_candidates"]))
    print("PHASE174_R3R7R18R2_PUBLIC_DELTA_CANDIDATES=" + str(verified["public_delta_surjectivity_candidates"]))
    print("PHASE174_R3R7R18R2_ISOLATED_DELTA_CANDIDATES=" + str(verified["isolated_delta_surjectivity_candidates"]))
    print("PHASE174_R3R7R18R2_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R7R18R2_NEW_PRODUCTION_RULES=0")
    print("PHASE174_R3R7R18R2_FULL_PYTEST=False")
    print("PHASE174_R3R7R18R2_ROOT_COMPLETE=False")
    print("PHASE174_R3R7R18R2_GATE=" + verified["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
