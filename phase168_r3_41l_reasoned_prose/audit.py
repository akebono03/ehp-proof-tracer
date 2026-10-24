"""Limited frozen-comparison gate; remaining textual differences remain visible."""
from __future__ import annotations

from pathlib import Path

from phase168_r3_41i_renderer_closure_audit.audit import run_audit


def main() -> int:
    output = Path(__file__).resolve().parent / "output"
    report = run_audit(output=output)
    for case in report["cases"]:
        print(
            case["name"],
            "Reference bodies", str(case["references_with_bodies"]) + "/" + str(case["references"]),
            "unused citations", case["references_not_explicitly_tagged_in_proof"],
            "benchmark gaps", case["missing_benchmark_explanations"],
            "proof_diff", case["proof_difference_lines"],
        )
    print("R3-41L AUDIT STATUS", report["status"])
    print("REPORT", output / "audit.md")
    print("UPLOAD_BUNDLE", output / "review_bundle.zip")
    print("FULL_PYTEST_NOT_RUN")
    if report["errors"] or not all(report["route_contract"].values()):
        return 1
    if any(
        row["missing_body_locators"] or row["missing_benchmark_explanations"]
        or row["references_not_explicitly_tagged_in_proof"]
        for row in report["cases"]
    ):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
