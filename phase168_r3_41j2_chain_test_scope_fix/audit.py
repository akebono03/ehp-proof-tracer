"""Scoped renderer audit that preserves the frozen-text review requirement."""
from __future__ import annotations

import sys
from pathlib import Path

from phase168_r3_41i_renderer_closure_audit.audit import run_audit


def main() -> int:
    output = Path(__file__).resolve().parent / "output"
    report = run_audit(output=output)
    for row in report["cases"]:
        print(
            row["name"],
            "reference_bodies", f'{row["references_with_bodies"]}/{row["references"]}',
            "unused_reference_numbers", row["references_not_explicitly_tagged_in_proof"],
            "benchmark_gaps", row["missing_benchmark_explanations"],
            "proof_diff", row["proof_difference_lines"],
            "reference_diff", row["reference_difference_lines"],
        )
    print("AUDIT_STATUS", report["status"])
    print("REPORT", output / "audit.md")
    print("UPLOAD_BUNDLE", output / "review_bundle.zip")
    print("FULL_PYTEST_NOT_RUN")
    if report["errors"] or not all(report["route_contract"].values()):
        return 1
    if any(
        row["references_not_explicitly_tagged_in_proof"]
        or row["missing_benchmark_explanations"]
        or row["missing_body_locators"]
        for row in report["cases"]
    ):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
