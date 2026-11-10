"""R52R1: guarded replacement of unstable generated-rule object comparisons.

Patches only R52's audit and focused tests. No production source, mathematical
rule, source registry, or common renderer is changed.
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
    TARGET_PREFIX + "tests/test_probe.py",
)
EXPECTED_HASHES = {'phase174_r3_r7_r52_public_kernel_source_bound_probe/audit.py': ('aee32aed10be84fc7cd8e2f3541ed986c0f05ef73c79eb684c902bceeb854b65', '5c2899abda9d4e38352d0aec7e5d91c065d8fab8fb3839e7240ad76183f6d6fe'), 'phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py': ('f39b4fff0f54a0dc8d4eeda40d7b7598a3cbaaaa7ec46ffc96c09bd7b9a26e1b', '3d5c34cfac99501b8aa1f6531866cb512cf77a30c2185047b0842b7477bbc865')}


def normalized_sha256(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def bundled_paths(relative: str) -> tuple[Path, Path]:
    if relative not in TARGETS or not relative.startswith(TARGET_PREFIX):
        raise ValueError("Unreviewed R52R1 patch target")
    suffix = relative[len(TARGET_PREFIX):]
    return PACKAGE / "baseline" / suffix, PACKAGE / "replacement" / suffix


def pending_replacements(root: Path = ROOT) -> tuple[tuple[Path, Path, str], ...]:
    decisions: list[tuple[Path, Path, str]] = []
    for relative in TARGETS:
        baseline, replacement = bundled_paths(relative)
        destination = root / relative
        if not all(path.is_file() for path in (baseline, replacement, destination)):
            raise RuntimeError("Missing reviewed R52R1 file: " + relative)
        before, after = EXPECTED_HASHES[relative]
        if normalized_sha256(baseline.read_bytes()) != before:
            raise RuntimeError("Bundled baseline changed: " + relative)
        if normalized_sha256(replacement.read_bytes()) != after:
            raise RuntimeError("Bundled replacement changed: " + relative)
        current = normalized_sha256(destination.read_bytes())
        if current not in (before, after):
            raise RuntimeError("R52 source is not reviewed baseline/replacement: " + relative)
        decisions.append((destination, replacement, "ALREADY_REPAIRED" if current == after else "REPLACE"))
    return tuple(decisions)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    from phase174_r3_r7_r52_public_kernel_source_bound_probe.source_guard import verify_checkout

    state = verify_checkout()
    pending = pending_replacements()
    if not args.dry_run:
        for destination, replacement, mode in pending:
            if mode == "REPLACE":
                destination.write_bytes(replacement.read_bytes())
        if any(mode != "ALREADY_REPAIRED" for _, _, mode in pending_replacements()):
            raise RuntimeError("R52R1 replacement verification failed")
    prefix = "PHASE174_R3R7R52R1_"
    for key in ("source_guard", "local_head", "remote_head"):
        print(prefix + key.upper() + "=" + str(state[key]))
    for destination, _, mode in pending:
        print(prefix + "TARGET=" + destination.relative_to(ROOT).as_posix() + ":" + mode)
    print(prefix + "TARGET_FILES=" + str(len(TARGETS)))
    print(prefix + "PRODUCTION_FILES_CHANGED=0")
    print(prefix + "NEW_GIVENS=0")
    print(prefix + "NEW_MATHEMATICAL_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "GATE=" + ("PASS_R52R1_PROPOSAL_CONTRACT_DRYRUN" if args.dry_run else "PASS_R52R1_PROPOSAL_CONTRACT_PATCH_APPLIED"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
