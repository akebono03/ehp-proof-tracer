"""Review-pinned Git lineage and source content checks for R15R6."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

REVIEWED_HEAD = "1f46799f0673df0de880830b37bea7071cba64b8"
REVIEWED_BLOBS = {'phase173_r4_r10_general_toda56_core/core.py': 'd35600804ecbbc5f8566d52e45a2f6ecf8816347', 'phase169_r10e4_ordered_db_prior/db_prior.py': 'ed8c6a1f0f6f130005d42a2edba4ab40991e879b', 'phase173_r4_r1_lemma54_source_bridge/source.py': 'a37bf7447194d72526522366944778c386c8966c', 'phase165_r52_r27_r5_literature.py': 'c9bfe2788f4cf043db6dada98a437afea6accf75', 'phase173_r4_r10_general_toda56_core/tests/test_core.py': '68205bf2840688a7b5d7277875c513323be7a5fc', 'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395', 'data/HyoujiGen.csv': '26f33db0c83ba7f151433583fe861598399cbe6a'}
REVIEWED_PREVIOUS_PACKAGE = {'phase173_r4_r15r5_family_source_frontier/audit.py': '46cb627981db32b930a316b329a6cf8c37b4ddba93cfde6f1d4ca6febbd9e83a', 'phase173_r4_r15r5_family_source_frontier/source_scan.py': 'df73926f4bd2b4b33d13fa582e4bb1da252b0c1373f2f8cd3062314d617e4523', 'phase173_r4_r15r5_family_source_frontier/preflight.py': '036498cae089b1f211c4e2d4981a8bdccaaff662a1ffd36c03032a2e303aa1ff'}
ALLOWED_COMMITTED_PREFIX = "phase173_r4_r15r5_family_source_frontier/"
ALLOWED_CACHE = ".pytest_cache/v/cache/nodeids"


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if completed.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + completed.stderr[:600])
    return completed.stdout.strip()


def is_allowed_committed(path: str) -> bool:
    return path == ALLOWED_CACHE or path.startswith(ALLOWED_COMMITTED_PREFIX)


def sha256_normalized(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def preflight(root: Path) -> None:
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Expected repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = git(root, "rev-parse", "HEAD")
    if git(root, "rev-parse", "origin/develop") != head:
        raise RuntimeError("GitHub develop HEAD and local HEAD differ")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode:
        raise RuntimeError("Unreviewed HEAD lineage")
    committed = tuple(filter(None, git(root, "diff", "--name-only", REVIEWED_HEAD, head).splitlines()))
    if any(not is_allowed_committed(path) for path in committed):
        raise RuntimeError("Unreviewed committed files: " + repr(committed))
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    dirty = tuple(filter(None, git(root, "diff", "--name-only").splitlines()))
    if any(path != ALLOWED_CACHE for path in dirty):
        raise RuntimeError("Unreviewed tracked changes: " + repr(dirty))
    for relative, expected in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + relative) != expected:
            raise RuntimeError("Reviewed Git blob differs: " + relative)
        if git(root, "hash-object", "--", relative) != expected:
            raise RuntimeError("Reviewed worktree differs: " + relative)
    for relative, expected in REVIEWED_PREVIOUS_PACKAGE.items():
        path = root / relative
        if not path.is_file() or sha256_normalized(path) != expected:
            raise RuntimeError("R15R5 previous source changed: " + relative)
    print("PHASE173_R4_R15R6_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R6_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R6_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R6_PRODUCTION_EDIT=NONE", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    preflight(args.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
