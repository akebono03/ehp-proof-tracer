"""Pinned HEAD-lineage and content checks for a read-only source frontier audit."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess


REVIEWED_BASE_HEAD = "0fc543a0d12e5fac0b2a3d842a2cf9187fd6d49c"
REVIEWED_BLOBS = {
    "phase169_r10eo_r2_definition_index/definition_index.py": "a86c1aee12a5f3bae3e24e148b86c7ae47fe2cd7",
    "phase169_r10eo_r3_reviewed_definition_bridge/reviewed_definitions.py": "d18244617e8fedb87d23c443def0c1c3147a1938",
    "phase169_r10d2_general_family_definition/family_citation.py": "b4b0c65e3eee85b557d5cfe7fa66a38a5386c3f8",
    "phase169_r10b_registered_stable_family_binding/family_registry.py": "4e461795954cc3e7a34fe9e3b47f77d00e5faeda",
    "phase173_r4_r10_general_toda56_core/core.py": "d35600804ecbbc5f8566d52e45a2f6ecf8816347",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "sources/toda/Toda_06_2.tex": "76934583cff01c8ea83f768e26947eb9b556653b",
}
PINNED_PRIOR_SOURCES = {
    "phase173_r4_r15r4_cited_composition_image/audit.py": "73f3d17e9194cd9b263857d415cd158532ca85dd7df376495df5ac7390cddee0",
    "phase173_r4_r15r4_cited_composition_image/replay.py": "c30ba826f4d24e19e7fd89153fd9da35d14f750eaea85e00e4695c827eab86f2",
    "phase173_r4_r15r4_cited_composition_image/bridge.py": "aa45bd3cd5b0bce95ebb0bf13645ec08b0e1620af5bf6130563aa50e56c78b2e",
}
ALLOWED_COMMITTED_PREFIX = "phase173_r4_r15r4_cited_composition_image/"
ALLOWED_PYTEST_CACHE = ".pytest_cache/v/cache/nodeids"


def git(root: Path, *args: str) -> str:
    """Get one local Git value; propagate command failures explicitly."""
    result = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + result.stderr[:550])
    return result.stdout.strip()


def is_allowed_committed(path: str) -> bool:
    """Only the separately verified prior read-only package may be committed."""
    return path == ALLOWED_PYTEST_CACHE or path.startswith(ALLOWED_COMMITTED_PREFIX)


def normalized_sha256(path: Path) -> str:
    """Allow CRLF/LF package extraction without relaxing source identity."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def verify_source_head(root: Path) -> None:
    """Fail closed on non-reviewed production edits, source drift or Git divergence."""
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Not the EHP Proof Tracer repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = git(root, "rev-parse", "HEAD")
    remote = git(root, "rev-parse", "origin/develop")
    if head != remote:
        raise RuntimeError("Local HEAD and origin/develop diverged")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_BASE_HEAD, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode:
        raise RuntimeError("Unreviewed HEAD lineage")
    committed = tuple(filter(None, git(
        root, "diff", "--name-only", REVIEWED_BASE_HEAD, head,
    ).splitlines()))
    if any(not is_allowed_committed(path) for path in committed):
        raise RuntimeError("Unreviewed committed source: " + repr(committed))
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    dirty = tuple(filter(None, git(root, "diff", "--name-only").splitlines()))
    if any(path != ALLOWED_PYTEST_CACHE for path in dirty):
        raise RuntimeError("Unreviewed tracked worktree changes: " + repr(dirty))
    for relative, blob in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + relative) != blob:
            raise RuntimeError("Unreviewed commit blob: " + relative)
        if git(root, "hash-object", "--", relative) != blob:
            raise RuntimeError("Unreviewed worktree blob: " + relative)
    for relative, expected in PINNED_PRIOR_SOURCES.items():
        path = root / relative
        if not path.is_file() or normalized_sha256(path) != expected:
            raise RuntimeError("Reviewed prior phase source mismatch: " + relative)
    print("PHASE173_R4_R15R5_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R5_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R5_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R5_PRODUCTION_EDIT=NONE", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    verify_source_head(args.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
