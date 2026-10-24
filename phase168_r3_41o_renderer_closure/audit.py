"""After-install frozen and structural proof review. No source mutation."""
from __future__ import annotations
from pathlib import Path
from phase168_r3_41i_renderer_closure_audit.audit import run_audit


def main():
    out = Path(__file__).resolve().parent / "output"
    report = run_audit(output=out)
    for row in report["cases"]:
        print(row["name"], "reference_bodies",
              f'{row["references_with_bodies"]}/{row["references"]}',
              "unused", row["references_not_explicitly_tagged_in_proof"],
              "benchmark_gaps", row["missing_benchmark_explanations"],
              "proof_diff", row["proof_difference_lines"])
    print("AUDIT_STATUS", report["status"])
    print("REVIEW_BUNDLE", out / "review_bundle.zip")
    print("FULL_PYTEST_NOT_RUN")
    if report["errors"] or not all(report["route_contract"].values()):
        raise RuntimeError("Web narrative route or audit failure")
    for row in report["cases"]:
        if (row["missing_body_locators"] or row["missing_benchmark_explanations"]
            or row["references_not_explicitly_tagged_in_proof"]):
            raise RuntimeError("Proof source, benchmark or body gap: " + row["name"])


if __name__ == "__main__":
    main()
