"""Strict read-only preflight for R15R1, committed or still locally installed."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from phase173_r4_r15r1_unbounded_abstract_frontier.patch_source import (
    ORIGINAL_BLOB,
    TARGET,
    transform,
)

REVIEWED_HEAD = "7104222524b63c9c517eaf8e09b8f0825842b316"
REVIEWED_R15R1_COMMITTED_HEAD = "c44519a123fdbf2c5ec57fe9c89e2fb1027f41a5"
REVIEWED_COMMITTED_CORE_BLOB = "d35600804ecbbc5f8566d52e45a2f6ecf8816347"
REVIEWED_COMMITTED_PATCH_BLOB = "06fcdb3c36362225332a1f49cda788b23f9cfc37"
PATCH_SOURCE = "phase173_r4_r15r1_unbounded_abstract_frontier/patch_source.py"
DEPENDENCIES = {
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase173_r4_r4_typed_generator_audit/audit.py": "82f9f734104ddb70df42090ee9a6413b06f1e98b",
    "phase173_r4_r6_alias_source_audit/audit.py": "9670dbd8c721e15e0c76b3e043accab6cb01daf3",
    "phase169_r10eq_r1_universal_stable_definition/definition.py": "0c74d121419b6755e947a367d7de465d81193174",
}
ALLOWED_TRACKED = {
    ".pytest_cache/v/cache/nodeids",
    "phase173_r4_r10_general_toda56_core/core.py",
    "phase168_r3_5_model_renderer.py",
    "phase165_r52_r3_web_adapter.py",
    "phase173_r4_r13_narrative_audit/audit.py",
    "phase173_r4_r13_narrative_audit/tests/test_audit.py",
}


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=root, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if completed.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + completed.stderr[:700])
    return completed.stdout.strip()


def git_content(root: Path, revision: str) -> bytes:
    completed = subprocess.run(
        ("git", "show", revision), cwd=root, capture_output=True, check=False,
    )
    if completed.returncode:
        raise RuntimeError("Cannot read reviewed git content: " + revision)
    return completed.stdout


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def reviewed_installed_core(root: Path, head: str) -> str:
    """Accept only the two reviewed commit states and the exact R15R1 core.

    Old HEAD: R15R1 is a local tracked change. New HEAD: the same R15R1
    core is committed. Neither case accepts an unrelated successor commit.
    """
    if head not in (REVIEWED_HEAD, REVIEWED_R15R1_COMMITTED_HEAD):
        raise RuntimeError("Unreviewed R15R1 commit lineage: " + head)
    if git(root, "rev-parse", REVIEWED_HEAD + ":" + TARGET) != ORIGINAL_BLOB:
        raise RuntimeError("Reviewed pre-R15R1 source blob changed")
    baseline = git_content(root, REVIEWED_HEAD + ":" + TARGET)
    transformed = normalized(transform(baseline))
    actual = normalized((root / TARGET).read_bytes())
    if actual != transformed:
        raise RuntimeError("R15R1 core does not equal reviewed transformation")

    if head == REVIEWED_HEAD:
        if git(root, "rev-parse", "HEAD:" + TARGET) != ORIGINAL_BLOB:
            raise RuntimeError("Pre-R15R1 committed core blob changed")
        return "LOCAL_PATCH"

    if git(root, "rev-parse", "HEAD:" + TARGET) != REVIEWED_COMMITTED_CORE_BLOB:
        raise RuntimeError("Committed R15R1 core blob changed")
    if normalized(git_content(root, "HEAD:" + TARGET)) != transformed:
        raise RuntimeError("Committed R15R1 core differs from the reviewed patch")
    if git(root, "rev-parse", "HEAD:" + PATCH_SOURCE) != REVIEWED_COMMITTED_PATCH_BLOB:
        raise RuntimeError("R15R1 patch implementation changed in committed state")
    if (normalized((root / PATCH_SOURCE).read_bytes())
            != normalized(git_content(root, "HEAD:" + PATCH_SOURCE))):
        raise RuntimeError("Unreviewed local R15R1 patch implementation")
    return "COMMITTED_PATCH"


def preflight(root: Path) -> bool:
    """Verify fixed reviewed commits and pristine mathematical dependencies."""
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Expected repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop")
    head = git(root, "rev-parse", "HEAD")
    remote = git(root, "rev-parse", "origin/develop")
    if head != remote:
        raise RuntimeError("Local and remote HEAD differ: " + head + "/" + remote)
    if head not in (REVIEWED_HEAD, REVIEWED_R15R1_COMMITTED_HEAD):
        raise RuntimeError("Unreviewed local or remote HEAD: " + head + "/" + remote)
    staged = git(root, "diff", "--cached", "--name-only")
    if staged:
        raise RuntimeError("Staged changes require review")
    modified = set(filter(None, git(root, "diff", "--name-only").splitlines()))
    if modified - ALLOWED_TRACKED:
        raise RuntimeError("Unexpected tracked modifications: " + str(modified - ALLOWED_TRACKED))
    for name, blob in DEPENDENCIES.items():
        if git(root, "rev-parse", "HEAD:" + name) != blob:
            raise RuntimeError("Committed dependency mismatch: " + name)
        if normalized((root / name).read_bytes()) != normalized(git_content(root, "HEAD:" + name)):
            raise RuntimeError("Unreviewed local dependency change: " + name)
    state = reviewed_installed_core(root, head)
    print("PHASE173_R4_R15R2_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R2_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R2_CORE_STATE=" + state, flush=True)
    print("PHASE173_R4_R15R2_PREVIOUS_R15R1_INSTALLED=True", flush=True)
    print("PHASE173_R4_R15R2_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R2_PRODUCTION_EDIT=NONE", flush=True)
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    preflight(args.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
