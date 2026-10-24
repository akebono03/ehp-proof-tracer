"""R3-41M2 focused audit: preserve reports without enforcing textual equality."""
from __future__ import annotations
from pathlib import Path
from phase168_r3_41i_renderer_closure_audit.audit import run_audit


def main() -> int:
    output = Path(__file__).resolve().parent / "output"
    report = run_audit(output=output)
    for case in report["cases"]:
        print(case["name"], "references", f'{case["references_with_bodies"]}/{case["references"]}',
              "unused", case["references_not_explicitly_tagged_in_proof"],
              "benchmark_gaps", case["missing_benchmark_explanations"],
              "proof_diff", case["proof_difference_lines"])
    print("R3-41M2", report["status"])
    print("UPLOAD_BUNDLE", output / "review_bundle.zip")
    print("FULL_PYTEST_NOT_RUN")
    if report["errors"] or not all(report["route_contract"].values()):
        return 1
    if any(row["missing_body_locators"] or row["missing_benchmark_explanations"]
           or row["references_not_explicitly_tagged_in_proof"]
           for row in report["cases"]):
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
