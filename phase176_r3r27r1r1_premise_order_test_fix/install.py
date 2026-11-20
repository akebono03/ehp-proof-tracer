"""Fail-closed test-only patch for Phase 176 R3R27R1."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase176_r3r27r1_toda55_quadruple_isolated" / "tests" / "test_source.py"
PAYLOAD = PACKAGE / "test_source_FULL.py"
OLD = "    assert find_inference_matches_for_rule(rule, (premise, eta, cited)) == ()"
NEW = (
    "    reordered = find_inference_matches_for_rule(rule, (premise, eta, cited))\n"
    "    assert len(reordered) == 1\n"
    "    assert reordered[0].premises == (premise, cited, eta)"
)


def apply(dry_run: bool) -> int:
    if not TARGET.is_file():
        raise RuntimeError("R3R27R1_TEST_FILE_MISSING")
    baseline = TARGET.read_text(encoding="utf-8")
    intended = PAYLOAD.read_text(encoding="utf-8")
    if baseline == intended:
        print("PHASE176_R3R27R1R1_GATE=PASS_ALREADY_PATCHED")
        return 0
    if baseline.count(OLD) != 1:
        raise RuntimeError("BASELINE_ASSERTION_NOT_UNIQUE")
    if baseline.replace(OLD, NEW) != intended:
        raise RuntimeError("TEST_BASELINE_DIFFERS_FROM_REVIEWED_SOURCE")
    if not dry_run:
        with TARGET.open("w", encoding="utf-8", newline="") as output:
            output.write(intended)
    print("PHASE176_R3R27R1R1_GATE=" +
          ("PASS_DRYRUN" if dry_run else "PASS_TEST_EXPECTATION_FIXED"))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        return apply(args.dry_run)
    except (OSError, RuntimeError) as error:
        print("PHASE176_R3R27R1R1_GATE=FAIL")
        print("PHASE176_R3R27R1R1_ERROR=" + str(error))
        return 1


if __name__ == "__main__":
    sys.exit(main())
