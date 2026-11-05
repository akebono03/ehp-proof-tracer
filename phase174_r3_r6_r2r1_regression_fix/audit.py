"""Run the historical Delta proof and new completed group proof on the same source path."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r4_public_delta_connection.audit import inspect_public_provider
from phase174_r3_r6_r2_prop44_lemma54.audit import inspect as inspect_group_root
from phase174_r3_r6_r2r1_regression_fix.patch import reviewed_changes


def main() -> int:
    reviewed_changes()
    delta = inspect_public_provider()
    if (delta.get("delta_zero_publicly_reconstructed") is not True
            or delta.get("source_ancestry_checked") is not True
            or delta.get("premises_both_inferred") is not True
            or delta.get("new_given") != 0):
        raise ValueError("EHP Delta source and inferred ancestry were not retained")
    root = inspect_group_root()
    if (root.get("root_status") != "complete"
            or root.get("hopf_invariant_condition_inferred") is not True
            or root.get("lemma54_is_root_ancestor") is not True
            or root.get("preprop44_is_root_ancestor") is not False
            or root.get("previous_pi6_4_still_complete") is not True
            or root.get("new_group_given") != 0):
        raise ValueError("The corrected public pi_8^5 proof regressed")
    output = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    output = output / "EHPProofTracerAudit" / "phase174_r3_r6_r2r1"
    output.mkdir(parents=True, exist_ok=True)
    report = {
        "phase": "174-R3-R6-R2R1",
        "historical_delta": delta,
        "root_status": root["root_status"],
        "root_steps": root["root_proven_steps"],
        "lemma54_root_ancestor": root["lemma54_is_root_ancestor"],
        "prelude_not_root_ancestor": not root["preprop44_is_root_ancestor"],
        "previous_pi6_4_still_complete": root["previous_pi6_4_still_complete"],
        "full_pytest_performed": False,
    }
    destination = output / "audit.json"
    destination.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("PHASE174_R3R6R2R1_DELTA_RECONSTRUCTED=True")
    print("PHASE174_R3R6R2R1_LEMMA54_DELTA_ANCESTRY=True")
    print("PHASE174_R3R6R2R1_PI85_COMPLETE=True")
    print("PHASE174_R3R6R2R1_PI64_PRESERVED=True")
    print("PHASE174_R3R6R2R1_PROVEN_STEPS=" + str(root["root_proven_steps"]))
    print("PHASE174_R3R6R2R1_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R6R2R1_REPORT=" + str(destination))
    print("PHASE174_R3R6R2R1_MATH_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
