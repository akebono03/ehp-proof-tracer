"""Guarded, idempotent replacement of R45 runner and its static contract.

The production math modules, source references and R45 audit itself are not
modified. A dry run checks the reviewed checkout without writing any files.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from phase174_r3_r7_r45_ehp_open_obligation_audit.source_guard import verify_checkout

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGETS = (
    "phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py",
)


def normalized_sha256(data: bytes) -> str:
    """Compare exact reviewed content modulo whole-file Windows EOL conversion."""
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def target_fragments(relative_path: str) -> tuple[Path, Path]:
    prefix = "phase174_r3_r7_r45_ehp_open_obligation_audit/"
    if relative_path not in TARGETS or not relative_path.startswith(prefix):
        raise ValueError("Unreviewed patch destination")
    child = relative_path[len(prefix):]
    return PACKAGE / "baseline" / child, PACKAGE / "replacement" / child


def pending_replacements(root: Path = ROOT) -> tuple[tuple[Path, Path, str], ...]:
    """Refuse arbitrary edits; accept only baseline or the exact repaired file."""
    result = []
    for relative in TARGETS:
        original, replacement = target_fragments(relative)
        destination = root / relative
        if not all(x.is_file() for x in (original, replacement, destination)):
            raise RuntimeError("Missing reviewed file: " + relative)
        current = normalized_sha256(destination.read_bytes())
        before = normalized_sha256(original.read_bytes())
        after = normalized_sha256(replacement.read_bytes())
        if before == after:
            raise RuntimeError("Repair replacement unexpectedly unchanged: " + relative)
        if current not in (before, after):
            raise RuntimeError("Unreviewed existing R45 file: " + relative)
        result.append((destination, replacement, "ALREADY_REPAIRED" if current == after else "REPLACE"))
    return tuple(result)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    changes = pending_replacements()
    if not args.dry_run:
        for destination, replacement, mode in changes:
            if mode == "REPLACE":
                destination.write_bytes(replacement.read_bytes())
        if any(mode != "ALREADY_REPAIRED" for _, _, mode in pending_replacements()):
            raise RuntimeError("Patch verification failed")
    print("PHASE174_R3R7R45R1_SOURCE_GUARD=" + state["source_guard"])
    print("PHASE174_R3R7R45R1_REVIEWED_HEAD=" + state["local_head"])
    print("PHASE174_R3R7R45R1_TARGET_FILES=" + str(len(changes)))
    for destination, _, mode in changes:
        print("PHASE174_R3R7R45R1_TARGET=" + destination.relative_to(ROOT).as_posix() + ":" + mode)
    print("PHASE174_R3R7R45R1_PRODUCTION_FILES_CHANGED=0")
    print("PHASE174_R3R7R45R1_FULL_PYTEST=False")
    print("PHASE174_R3R7R45R1_GATE=" + (
        "PASS_R45R1_IMPORTMODE_DRYRUN" if args.dry_run else
        "PASS_R45R1_IMPORTMODE_REPAIR_APPLIED"
    ))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
