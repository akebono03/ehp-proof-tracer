"""Content-pinned Git/source preflight for the non-invasive R15R7 package."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

REVIEWED_HEAD = "3e3dfecec3c6972a1a2bb19f00372b66314492e2"
REVIEWED_BLOBS = {
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase173_r4_r11_zero_public_connection/source.py": "d18a52b87ca258fdabea46f3523cbd09ace65833",
    "phase165_r52_r9_shared_math.py": "f49b0b7699e29ec1b78d73578dc66a0e33d6e336",
    "phase164_r8_proofstep_factory.py": "d314def19ab4e3e77f57af0ca9da18d7837efdda",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r27_r5_literature.py": "c9bfe2788f4cf043db6dada98a437afea6accf75",
    "phase173_r4_r1_lemma54_source_bridge/source.py": "a37bf7447194d72526522366944778c386c8966c",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase173_r4_r10_general_toda56_core/core.py": "d35600804ecbbc5f8566d52e45a2f6ecf8816347",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase173_r4_r10_general_toda56_core/tests/test_core.py": "68205bf2840688a7b5d7277875c513323be7a5fc",
}
PREVIOUS_R6_HASHES = {
    "phase173_r4_r15r6_abstract_toda44_rule/abstract_rule.py": "fceab3505977b741e0756221b8c7c7abb70339ca75527e55f1924f23f7b54444",
    "phase173_r4_r15r6_abstract_toda44_rule/audit.py": "490044d7d5e5513b3fb46b4c876a36b4ffd36aa7fb6b6f63926641c00d48decd",
    "phase173_r4_r15r6_abstract_toda44_rule/preflight.py": "6d50cc42879bf2178b6ed554aa7207df7f28280e50efbe0f7f361ff796c71041",
}
ALLOWED_PREVIOUS_PREFIX = "phase173_r4_r15r6_abstract_toda44_rule/"
ALLOWED_CACHE = ".pytest_cache/v/cache/nodeids"


def git(root: Path, *args: str) -> str:
    """Run one read-only Git query, refusing failure."""
    result = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + result.stderr[:600])
    return result.stdout.strip()


def allowed_committed(path: str) -> bool:
    """Permit only the immediate previous phase package's commit."""
    return path == ALLOWED_CACHE or path.startswith(ALLOWED_PREVIOUS_PREFIX)


def normalized_sha256(path: Path) -> str:
    """Recognize identical text under either Windows or Unix line endings."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def preflight(root: Path) -> None:
    """Require a pristine reviewed math core and same upstream/local HEAD."""
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Expected repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = git(root, "rev-parse", "HEAD")
    if git(root, "rev-parse", "origin/develop") != head:
        raise RuntimeError("Local HEAD and GitHub develop differ")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode:
        raise RuntimeError("Unreviewed HEAD lineage")
    committed = tuple(filter(None, git(
        root, "diff", "--name-only", REVIEWED_HEAD, head,
    ).splitlines()))
    if any(not allowed_committed(path) for path in committed):
        raise RuntimeError("Unreviewed committed source: " + repr(committed))
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    dirty = tuple(filter(None, git(root, "diff", "--name-only").splitlines()))
    if any(path != ALLOWED_CACHE for path in dirty):
        raise RuntimeError("Unreviewed tracked modifications: " + repr(dirty))
    for relative, expected_blob in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + relative) != expected_blob:
            raise RuntimeError("Reviewed Git blob changed: " + relative)
        if git(root, "hash-object", "--", relative) != expected_blob:
            raise RuntimeError("Reviewed worktree content changed: " + relative)
    for relative, expected_hash in PREVIOUS_R6_HASHES.items():
        source = root / relative
        if not source.is_file() or normalized_sha256(source) != expected_hash:
            raise RuntimeError("R15R6 source not reviewed: " + relative)
    print("PHASE173_R4_R15R7_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R7_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R7_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R7_PRODUCTION_EDIT=NONE", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    preflight(args.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
