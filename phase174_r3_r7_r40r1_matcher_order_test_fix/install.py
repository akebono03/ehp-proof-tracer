"""R40R1: correct one reviewed R40 test expectation without changing math."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r40_adopted_db_zero_image_isolated.source_guard import (
    verify_checkout,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py"
BASELINE = PACKAGE / "baseline/test_rule.py"
REPLACEMENT = PACKAGE / "replacement/test_rule.py"
REVIEWED_PINS = {
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py":
        "2df41f2787b76d8d35852c7de2300b90b5391cf9cadbc27b15bc62b122907a83",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/audit.py":
        "a838e53ca442a523c48a891a071b1860547d418e3c49476de545b6d84f13e0d5",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/source_guard.py":
        "60c4ab69bf70680a0585f7193962699eb28a53cc1a81949d8f9873cf289fa8d9",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/run.ps1":
        "e24f0464a285c00a24e4a510e5a59e7b1fb85f62e5ff421b23dea42631bfe397",
}
BASELINE_SHA256 = "1e7952be77c1569d211ed16f8e610c9e20183b5dc22a56d0fd4e46c2b1719f2a"
REPLACEMENT_SHA256 = "dabd332aa0cbf036e55e9aacfe992d2a87ef50db9e296780246d3c3d066d4cf8"


def normalized(data: bytes) -> bytes:
    """Ignore Windows CRLF differences, not mathematical or code changes."""
    return data.replace(b"\r\n", b"\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(normalized(data)).hexdigest()


def verified_mode() -> str:
    """Require reviewed Git/source state and the exact old or new R40 test."""
    verify_checkout()
    for name, expected in REVIEWED_PINS.items():
        file = ROOT / name
        if not file.is_file() or digest(file.read_bytes()) != expected:
            raise RuntimeError("R40R1 reviewed source differs: " + name)
    if not BASELINE.is_file() or digest(BASELINE.read_bytes()) != BASELINE_SHA256:
        raise RuntimeError("R40R1 baseline test has changed")
    if not REPLACEMENT.is_file() or digest(REPLACEMENT.read_bytes()) != REPLACEMENT_SHA256:
        raise RuntimeError("R40R1 replacement test has changed")
    if not TARGET.is_file():
        raise RuntimeError("R40 test target not present")
    current = digest(TARGET.read_bytes())
    if current == BASELINE_SHA256:
        return "BASELINE"
    if current == REPLACEMENT_SHA256:
        return "CORRECTED"
    raise RuntimeError("R40 test changed outside reviewed R40R1 scope")


def install(dry_run: bool) -> dict[str, object]:
    """On non-dry-run install a single test-file replacement atomically."""
    mode = verified_mode()
    result = {
        "source_guard": "PASS",
        "test_mode": mode,
        "production_files_changed": 0,
        "changed_test_files": 0 if dry_run or mode == "CORRECTED" else 1,
        "rule_or_api_changed": False,
        "full_pytest": False,
    }
    if dry_run:
        result["mode"] = "DRYRUN"
        return result
    if mode == "BASELINE":
        previous = TARGET.read_bytes()
        style = b"\r\n" if b"\r\n" in previous else b"\n"
        updated = normalized(REPLACEMENT.read_bytes())
        if style == b"\r\n":
            updated = updated.replace(b"\n", b"\r\n")
        temporary_name = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", prefix="r40r1_", suffix=".tmp", dir=TARGET.parent,
                delete=False,
            ) as stream:
                temporary_name = stream.name
                stream.write(updated)
            os.replace(temporary_name, TARGET)
        finally:
            if temporary_name is not None and os.path.exists(temporary_name):
                os.unlink(temporary_name)
    if verified_mode() != "CORRECTED":
        raise RuntimeError("R40R1 test replacement failed post-installation check")
    result["mode"] = "INSTALLED"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = install(dry_run=args.dry_run)
    for key, value in report.items():
        print("PHASE174_R3R7R40R1_" + key.upper() + "=" + str(value))
    print("PHASE174_R3R7R40R1_GATE=PASS_R40R1_MATCHER_ORDER_TEST_CONTRACT_FIXED")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
