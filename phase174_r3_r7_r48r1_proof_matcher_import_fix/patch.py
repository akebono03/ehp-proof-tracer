"""R48R1: a guarded, idempotent fix for a missing audit function import.

Only R48 audit.py and its static tests may be replaced.  The R48 checkout
and all source pins are independently verified before a non-dry-run write.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from phase174_r3_r7_r48_cited_lower_kernel_tree_frontier.source_guard import verify_checkout

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET_PREFIX = "phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/"
TARGETS = (
    TARGET_PREFIX + "audit.py",
    TARGET_PREFIX + "tests/test_static.py",
)


def normalized_sha256(data: bytes) -> str:
    """Allow CRLF/LF conversion, not arbitrary source changes."""
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def target_fragments(relative_path: str) -> tuple[Path, Path]:
    """Return the reviewed baseline and replacement for an allowed file."""
    if relative_path not in TARGETS or not relative_path.startswith(TARGET_PREFIX):
        raise ValueError("Unreviewed R48R1 patch destination")
    leaf = relative_path[len(TARGET_PREFIX):]
    return PACKAGE / "baseline" / leaf, PACKAGE / "replacement" / leaf


def pending_replacements(root: Path = ROOT) -> tuple[tuple[Path, Path, str], ...]:
    """Refuse changed R48 files and accept either exact vetted revision."""
    result = []
    for relative in TARGETS:
        before_path, after_path = target_fragments(relative)
        destination = root / relative
        if not all(path.is_file() for path in (before_path, after_path, destination)):
            raise RuntimeError("Missing reviewed R48 file: " + relative)
        before = normalized_sha256(before_path.read_bytes())
        after = normalized_sha256(after_path.read_bytes())
        current = normalized_sha256(destination.read_bytes())
        if before == after:
            raise RuntimeError("R48R1 replacement has no change: " + relative)
        if current not in (before, after):
            raise RuntimeError("Unreviewed existing R48 file: " + relative)
        result.append((destination, after_path, "ALREADY_REPAIRED" if current == after else "REPLACE"))
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
            raise RuntimeError("R48R1 patch verification failed")
    prefix = "PHASE174_R3R7R48R1_"
    print(prefix + "SOURCE_GUARD=" + str(state["source_guard"]))
    print(prefix + "LOCAL_HEAD=" + str(state["local_head"]))
    print(prefix + "REMOTE_HEAD=" + str(state["remote_head"]))
    print(prefix + "TARGET_FILES=" + str(len(changes)))
    for destination, _, mode in changes:
        print(prefix + "TARGET=" + destination.relative_to(ROOT).as_posix() + ":" + mode)
    print(prefix + "PRODUCTION_FILES_CHANGED=0")
    print(prefix + "NEW_GIVENS=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "GATE=" + (
        "PASS_R48R1_MATCHER_IMPORT_DRYRUN" if args.dry_run else
        "PASS_R48R1_MATCHER_IMPORT_REPAIR_APPLIED"
    ))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
