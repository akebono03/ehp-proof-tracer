"""Guarded read-only preflight and one-test-function fix for R2J-R4-R5.

The installer refuses unrelated local edits and modifies only the two
explicitly listed, known baseline files inside the existing audit package.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET_PACKAGE = ROOT / "phase171_r2j_r4_r5_short_exact_sequence"
TARGETS = (
    (
        TARGET_PACKAGE / "tests" / "test_audit.py",
        HERE / "assets" / "test_audit.py",
        "d1d4419054ecbfa015045833c768c8ccda5fcbc7565dfc21435a58aa516a98d9",
        "56d1b18d3ceb5ba430a07fbd700a43aa09cb788ba6dbd5d5f73a7dc3a780b257",
    ),
    (
        TARGET_PACKAGE / "CODE_FULL_JA.md",
        HERE / "assets" / "CODE_FULL_JA.md",
        "9945b629e86ad0764d2598a4ff3ab3cec6e6935945b3ea629b633d91e2b50cb1",
        "f01feab468bc127a8a7275a04f025e4ac5ddba3f89330f889a28672dad4b9b87",
    ),
)


def _digest(content: bytes) -> str:
    return sha256(content).hexdigest()


def preflight() -> tuple:
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()
    if branch != "develop":
        raise RuntimeError("R4-R5-R1 requires the develop branch")
    print("PHASE171_R2J_R4_R5_R1_BRANCH=" + branch, flush=True)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()
    print("PHASE171_R2J_R4_R5_R1_HEAD=" + head, flush=True)
    planned = []
    for target, replacement, old_hash, new_hash in TARGETS:
        if not target.is_file() or not replacement.is_file():
            raise RuntimeError("required local file absent: " + str(target))
        current = target.read_bytes()
        payload = replacement.read_bytes()
        if _digest(payload) != new_hash:
            raise RuntimeError("fix asset integrity mismatch: " + str(replacement))
        current_hash = _digest(current)
        if current_hash not in (old_hash, new_hash):
            raise RuntimeError("unrecognized local modification; refusing overwrite: " + str(target))
        planned.append((target, payload, current_hash != new_hash))
    return tuple(planned)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    plan = preflight()
    print("PHASE171_R2J_R4_R5_R1_TARGETS=" + str(len(plan)), flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R5_R1_RESULT=PASS_DRY_RUN", flush=True)
        return
    for target, payload, changed in plan:
        if changed:
            target.write_bytes(payload)
            print("PHASE171_R2J_R4_R5_R1_PATCHED=" + str(target), flush=True)
    if any(target.read_bytes() != payload for target, payload, _ in plan):
        raise RuntimeError("fix file verification failed")
    print("PHASE171_R2J_R4_R5_R1_PATCH=PASS", flush=True)


if __name__ == "__main__":
    main()
