"""R48R2: guarded source-bound domain obligation in the R48 audit only.

The mathematical R35 rule and all production code remain unchanged.
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
EXPECTED_HASHES = {'phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/audit.py': ('4b9b8019ebe22fc8109ec793e8381c371be5ebc618ec009b9440231bb52722a2', '64acb4b8fe3c6598f766b6f98828ddd5e51bf67df9d2670a719e83621e60f0de'), 'phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/tests/test_static.py': ('43f83d892afd80aca919b7776328e76317350f88c979941108c09d1f56201a3a', 'f5ca738bacc3b151871702d8e620cca71d2bf5f8df613b28e5ccf804b4af6f83')}


def normalized_sha256(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def fragments(relative: str) -> tuple[Path, Path]:
    if relative not in TARGETS or not relative.startswith(TARGET_PREFIX):
        raise ValueError("Unreviewed R48R2 target")
    name = relative[len(TARGET_PREFIX):]
    return PACKAGE / "baseline" / name, PACKAGE / "replacement" / name


def pending_replacements(root: Path = ROOT) -> tuple[tuple[Path, Path, str], ...]:
    decisions = []
    for relative in TARGETS:
        before, after = fragments(relative)
        destination = root / relative
        if not all(path.is_file() for path in (before, after, destination)):
            raise RuntimeError("Missing R48R2 source: " + relative)
        old_expected, new_expected = EXPECTED_HASHES[relative]
        if normalized_sha256(before.read_bytes()) != old_expected:
            raise RuntimeError("R48R2 bundled baseline was changed: " + relative)
        if normalized_sha256(after.read_bytes()) != new_expected:
            raise RuntimeError("R48R2 bundled replacement was changed: " + relative)
        present = normalized_sha256(destination.read_bytes())
        if present not in (old_expected, new_expected):
            raise RuntimeError("R48 file is not the reviewed R48R1 or R48R2 version: " + relative)
        decisions.append((destination, after, "ALREADY_REPAIRED" if present == new_expected else "REPLACE"))
    return tuple(decisions)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    decisions = pending_replacements()
    if not args.dry_run:
        for destination, replacement, mode in decisions:
            if mode == "REPLACE":
                destination.write_bytes(replacement.read_bytes())
        if any(mode != "ALREADY_REPAIRED" for _, _, mode in pending_replacements()):
            raise RuntimeError("R48R2 replacement verification failed")
    prefix = "PHASE174_R3R7R48R2_"
    print(prefix + "SOURCE_GUARD=" + str(state["source_guard"]))
    print(prefix + "LOCAL_HEAD=" + str(state["local_head"]))
    print(prefix + "REMOTE_HEAD=" + str(state["remote_head"]))
    print(prefix + "TARGET_FILES=" + str(len(decisions)))
    for destination, _, mode in decisions:
        print(prefix + "TARGET=" + destination.relative_to(ROOT).as_posix() + ":" + mode)
    print(prefix + "PRODUCTION_FILES_CHANGED=0")
    print(prefix + "NEW_GIVENS=0")
    print(prefix + "NEW_MATHEMATICAL_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "GATE=" + (
        "PASS_R48R2_SOURCE_BOUND_DRYRUN" if args.dry_run else
        "PASS_R48R2_SOURCE_BOUND_PATCH_APPLIED"
    ))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
