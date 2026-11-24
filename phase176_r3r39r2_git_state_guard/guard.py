"""Verify the exact R3R39 change independently of Git staging state."""
from __future__ import annotations

import argparse
import subprocess

from phase176_r3r39_public_equality_transport.apply import (
    ROOT, TARGET, normalized_source, patched_bytes,
)

BASE = "8033d70c5ee67626b278918be15484c688ed146e"


def classify(baseline: bytes, head: bytes, index: bytes, current: bytes) -> str:
    expected = patched_bytes(baseline, current)
    if expected == baseline or normalized_source(expected) == normalized_source(baseline):
        raise ValueError("BASELINE_ALREADY_PATCHED")
    if current != expected:
        raise ValueError("WORKTREE_BYTES_NOT_REPAIRED")
    if head == baseline and index == baseline:
        return "UNSTAGED"
    if head == baseline and index == expected:
        return "STAGED"
    if head == expected and index == expected:
        return "COMMITTED"
    raise ValueError("UNEXPECTED_HEAD_OR_INDEX_BYTES")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    relative = TARGET.relative_to(ROOT).as_posix()
    def read_git(spec: str) -> bytes:
        return subprocess.check_output(["git", "show", spec], cwd=ROOT)
    baseline = read_git(BASE + ":" + relative)
    head = read_git("HEAD:" + relative)
    index = read_git(":" + relative)
    current = TARGET.read_bytes()
    state = classify(baseline, head, index, current)
    # Check actual Git reporting as well; fail rather than hide index flags or filters.
    def stat(*options: str) -> str:
        return subprocess.check_output(["git", "diff", *options, "--numstat", "--", relative], cwd=ROOT).decode("utf-8").strip()
    expected_stat = "9\t0\t" + relative
    expected = {"UNSTAGED": (expected_stat, ""), "STAGED": ("", expected_stat), "COMMITTED": ("", "")}[state]
    actual = (stat(), stat("--cached"))
    if actual != expected:
        raise ValueError(f"GIT_DIFF_STATE_MISMATCH: state={state}, actual={actual!r}, expected={expected!r}")
    if stat(BASE) != expected_stat:
        raise ValueError("BASELINE_DIFF_NOT_NINE_INSERTIONS")
    print("PHASE176_R3R39R2_GIT_STATE=" + state)
    print("PHASE176_R3R39R2_BASELINE_DIFF=" + expected_stat)
    print("PHASE176_R3R39R2_GATE=" + ("PASS_R3R39R2_DRYRUN" if args.dry_run else "PASS_R3R39R2_EXACT_PATCH_VERIFIED"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
