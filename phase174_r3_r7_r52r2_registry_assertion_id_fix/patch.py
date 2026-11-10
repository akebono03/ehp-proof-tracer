"""R52R2: repair only the registry assertion-id lookup in the R52 audit.

Read-only production: no mathematical rule, provider, Web route or other
application module is changed. Only the R52 audit and static test are replaced.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET_PREFIX = "phase174_r3_r7_r52_public_kernel_source_bound_probe/"
TARGETS = (
    TARGET_PREFIX + "audit.py",
    TARGET_PREFIX + "tests/test_static.py",
)
EXPECTED_HASHES = {'phase174_r3_r7_r52_public_kernel_source_bound_probe/audit.py': ('5c2899abda9d4e38352d0aec7e5d91c065d8fab8fb3839e7240ad76183f6d6fe', '40ebfdd1452655f17613bf1927d21151966a0f098287846d1587e952c62442e8'), 'phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_static.py': ('1547a6ab7bf78475d0bd9756bdb6d3b146a8e03324fdb5bc3fea94260c094559', '13976270d406920c26e8fe7dfc27ba2d29144d0c2f5d16dcbd19d8bf9d655b86')}


def normalized_sha256(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def reviewed_paths(relative: str) -> tuple[Path, Path]:
    if relative not in TARGETS or not relative.startswith(TARGET_PREFIX):
        raise ValueError("Unreviewed R52R2 replacement target")
    suffix = relative[len(TARGET_PREFIX):]
    return PACKAGE / "baseline" / suffix, PACKAGE / "replacement" / suffix


def pending_replacements(root: Path = ROOT) -> tuple[tuple[Path, Path, str], ...]:
    decisions: list[tuple[Path, Path, str]] = []
    for relative in TARGETS:
        before, after = reviewed_paths(relative)
        destination = root / relative
        if not all(path.is_file() for path in (before, after, destination)):
            raise RuntimeError("R52R2 target or bundled source missing: " + relative)
        old_hash, new_hash = EXPECTED_HASHES[relative]
        if normalized_sha256(before.read_bytes()) != old_hash:
            raise RuntimeError("R52R2 bundled baseline tampered: " + relative)
        if normalized_sha256(after.read_bytes()) != new_hash:
            raise RuntimeError("R52R2 bundled replacement tampered: " + relative)
        present = normalized_sha256(destination.read_bytes())
        if present not in (old_hash, new_hash):
            raise RuntimeError("Unreviewed R52 working file: " + relative)
        decisions.append((
            destination, after, "ALREADY_REPAIRED" if present == new_hash else "REPLACE",
        ))
    return tuple(decisions)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    from phase174_r3_r7_r52_public_kernel_source_bound_probe.source_guard import verify_checkout
    state = verify_checkout()
    decisions = pending_replacements()
    if not args.dry_run:
        for target, replacement, mode in decisions:
            if mode == "REPLACE":
                target.write_bytes(replacement.read_bytes())
        if any(mode != "ALREADY_REPAIRED" for _, _, mode in pending_replacements()):
            raise RuntimeError("R52R2 replacement verification failed")
    p = "PHASE174_R3R7R52R2_"
    for key in ("source_guard", "local_head", "remote_head"):
        print(p + key.upper() + "=" + str(state[key]))
    for target, _, mode in decisions:
        print(p + "TARGET=" + target.relative_to(ROOT).as_posix() + ":" + mode)
    print(p + "TARGET_FILES=" + str(len(decisions)))
    print(p + "PRODUCTION_FILES_CHANGED=0")
    print(p + "NEW_GIVENS=0")
    print(p + "NEW_MATHEMATICAL_RULES=0")
    print(p + "FULL_PYTEST=False")
    print(p + "GATE=" + (
        "PASS_R52R2_ASSERTION_ID_DRYRUN" if args.dry_run else
        "PASS_R52R2_ASSERTION_ID_PATCH_APPLIED"
    ))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
