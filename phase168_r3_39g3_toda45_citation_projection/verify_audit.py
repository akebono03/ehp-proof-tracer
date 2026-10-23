"""Require the existing frozen audit's explanation checks for all three cases."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "phase168_r3_39f_frozen_comparison" / "output" / "audit.json"


def main() -> None:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    expected = {"pi3_2", "pi4_3", "pi5_4"}
    observed = {row["name"] for row in data["cases"]}
    if observed != expected:
        raise RuntimeError(f"Audit case mismatch: expected {expected}, got {observed}")
    for row in data["cases"]:
        failed = [check["key"] for check in row["benchmark_explanations"]
                  if not check["present"]]
        passed = len(row["benchmark_explanations"]) - len(failed)
        print(f'{row["name"]}: {passed}/{len(row["benchmark_explanations"])}'
              f' (reference_diff={row["reference_diff_lines"]},'
              f' proof_diff={row["proof_diff_lines"]})')
        if failed:
            raise RuntimeError(f'{row["name"]}: benchmark mismatches: {failed}')
        if not row["reference_bodies_complete"]:
            raise RuntimeError(f'{row["name"]}: missing reference body')
    print("12/12 explanation checks PASS. Full-text differences still require review.")


if __name__ == "__main__":
    main()
