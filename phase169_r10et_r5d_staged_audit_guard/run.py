"""R10ET-R5D deterministic patch, focused verification and rollback."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path

from phase169_r10et_r5d_staged_audit_guard.patch import (
    EXPECTED_BLOBS, PROVIDER, R4_TARGETS,
    apply, git_blob, git_bytes, prepare, restore,
)

BASE_HEAD = "5a8ad4a56c5407c0fbe15ba14516a1c1a99f0562"
R4_COMMITTED_HEAD = "3a8014efb91ddf76060c4d07d73153e55ea52c75"

# R5, R5B, and R5C audit packages can be staged independently while the
# production tree stays unchanged. They are not evidence for the proof and
# must never become modification targets or be added/removed from the index.
# Permit *only* added files under these previously reviewed audit namespaces.
# Exact staged entries may be a subset, so an interrupted git add or a newly
# staged audit bundle does not repeatedly prevent safe R5 implementation.
ALLOWED_STAGED_AUDIT_DIRECTORIES = frozenset((
    "phase169_r10et_r5_common_definition_provider",
    "phase169_r10et_r5b_committed_r4_guard",
    "phase169_r10et_r5c_preserve_staged_r5",
    "phase169_r10et_r5d_staged_audit_guard",
))

REVIEWED_HEADS = (BASE_HEAD, R4_COMMITTED_HEAD)
FOCUSED = (
    "phase169_r10et_r5d_staged_audit_guard/tests/test_r5d_guard.py",
    "phase169_r10et_r5d_staged_audit_guard/tests/test_r5d_git_index.py",
    "phase169_r10et_r5d_staged_audit_guard/tests/test_r5_patch.py",
    "phase169_r10et_r5d_staged_audit_guard/tests/test_r5_live.py",
    "phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py",
    "phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py",
    "phase169_r10el_shared_generator_suppression/tests/test_r10el_live.py",
    "phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py",
    "phase169_r10et_r4_cyclic_definition_projection/tests/test_r10et_r4_patch.py",
    "phase169_r10et_r4_cyclic_definition_projection/tests/test_r10et_r4_live.py",
    "phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_stable_definition.py",
    "phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_live.py",
    "phase169_r10en_shared_citation_provenance/tests/test_r10en_core.py",
    "phase169_r10es_r1_typed_partial_power_display/tests/test_r10es_display.py",
)


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout.strip()


def reviewed_index_snapshot(root: Path) -> str:
    """Check and fingerprint staged audit-only additions without altering Git.

    Only status A under the four exact reviewed audit-package directories is
    permitted. Staging partial packages is harmless and permitted. Production
    files, unknown directories, modified/deleted entries and renames fail
    closed. The raw cached diff is compared after all tests and the live audit
    to detect *any* index change during the run, including changed staged bytes.
    """
    manifest = git(root, "diff", "--cached", "--name-status")
    if manifest:
        seen = set()
        for line in manifest.splitlines():
            parts = line.split("\t")
            if len(parts) != 2 or parts[0] != "A":
                raise RuntimeError(
                    "unreviewed staged change (only added audit files allowed)"
                )
            path = parts[1].replace("\\", "/")
            segments = path.split("/")
            if (len(segments) < 2
                    or segments[0] not in ALLOWED_STAGED_AUDIT_DIRECTORIES
                    or any(segment in ("", ".", "..") for segment in segments)
                    or path in seen):
                raise RuntimeError(
                    "unreviewed staged paths; only reviewed R5 audit directories allowed"
                )
            seen.add(path)
    return git(root, "diff", "--cached", "--raw")


def verify_preconditions(root: Path) -> tuple[str, set[str]]:
    """Accept only the reviewed R4 committed or verified pre-commit state.

    R4's production changes are part of HEAD in R4_COMMITTED_HEAD, whereas
    they were uncommitted in BASE_HEAD.  Both states must resolve to the exact
    same reviewed R4 bytes before R5 touches any production source.
    """
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R10ET-R5D requires develop branch")
    head = git(root, "rev-parse", "HEAD")
    if head not in REVIEWED_HEADS:
        raise RuntimeError(f"R10ET-R5D refuses unreviewed HEAD {head}")

    tracked = set(filter(None, git(root, "diff", "--name-only").splitlines()))
    expected_tracked = set(R4_TARGETS) if head == BASE_HEAD else set()
    if tracked != expected_tracked:
        raise RuntimeError(
            "R10ET-R5D refuses unexpected tracked changes; "
            f"HEAD={head}, expected={sorted(expected_tracked)}, "
            f"actual={sorted(tracked)}"
        )

    # The only permitted cached changes are added files in reviewed audit packages.
    reviewed_index_snapshot(root)

    # Verify that both R4 files have exactly the bytes produced by the
    # already-reviewed R4 full-function patch, regardless of commit status.
    from phase169_r10et_r4_cyclic_definition_projection.patch import (
        EXPECTED_GIT_BLOBS, transformed,
    )
    for path in R4_TARGETS:
        baseline = subprocess.run(
            ["git", "-C", str(root), "show", f"{BASE_HEAD}:{path}"],
            capture_output=True, check=True,
        ).stdout
        if git_blob(baseline) != EXPECTED_GIT_BLOBS[path]:
            raise RuntimeError(f"R4 baseline source differs: {path}")
        expected_r4, _full_function = transformed(baseline, path)
        current = (root / path).read_bytes()
        if current != expected_r4:
            raise RuntimeError(f"R4 implementation differs: {path}")
        if head == R4_COMMITTED_HEAD and git_bytes(root, path) != expected_r4:
            raise RuntimeError(f"committed R4 content differs: {path}")

    # All five R5 input files must be unmodified and match their reviewed
    # Git blob IDs. The working tree cannot spoof a reviewed HEAD.
    for path, sha in EXPECTED_BLOBS.items():
        current = (root / path).read_bytes()
        if git_blob(current) != sha or git_blob(git_bytes(root, path)) != sha:
            raise RuntimeError(f"R5 source differs from reviewed production: {path}")
    return head, tracked


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--cases", default="all", choices=("all", "focus"))
    args = parser.parse_args(argv)
    root, output = args.root.resolve(), args.output.resolve()
    print("R10ET_R5D_MODE=IMPLEMENT_FOCUSED", flush=True)
    print("R10ET_R5D_REPO=" + str(root), flush=True)
    versions = None
    patched = False
    try:
        head, tracked = verify_preconditions(root)
        staged_before = reviewed_index_snapshot(root)
        print("R10ET_R5D_HEAD=" + head, flush=True)
        print("R10ET_R5D_REVIEWED_AUDIT_STAGE=" + str(bool(staged_before)), flush=True)
        versions = prepare(root, output)
        apply(root, versions)
        patched = True
        print("R10ET_R5D_PATCHED=" + ",".join(versions), flush=True)
        print("R10ET_R5D_FULL_FUNCTION=" + str(
            output / "full_sources" /
            (PROVIDER + ".shared_expansion_provider.FULL.py")), flush=True)
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        print("R10ET_R5D_FOCUSED_PYTEST_START", flush=True)
        completed = subprocess.run([sys.executable, "-m", "pytest", "-q",
                                    "-p", "no:cacheprovider", *FOCUSED],
                                   cwd=root, env=env)
        print("R10ET_R5D_FOCUSED_PYTEST_EXIT=" + str(completed.returncode), flush=True)
        if completed.returncode:
            raise RuntimeError("focused pytest failed")
        from phase169_r10et_r5d_staged_audit_guard.audit import audit
        report = audit(root, output, cases=args.cases)
        if not report.get("all_complete_trusted"):
            raise RuntimeError("production-case audit incomplete")
        expected = set(versions) | tracked
        final = set(filter(None, git(root, "diff", "--name-only").splitlines()))
        if final != expected or reviewed_index_snapshot(root) != staged_before:
            raise RuntimeError(
                f"unexpected tracked/index modifications: worktree={final}"
            )
        for path, (_before, after) in versions.items():
            if (root / path).read_bytes() != after:
                raise RuntimeError(f"changed source during audit: {path}")
        print("R10ET_R5D_AUDIT=" + str(output / "audit.md"), flush=True)
        print("R10ET_R5D_R4_CHANGES_PRESERVED=True", flush=True)
        print("R10ET_R5D_REAL_PROVIDER=True", flush=True)
        print("R10ET_R5D_INDEX_PRESERVED=True", flush=True)
        print("R10ET_R5D_COMPLETE=PASS", flush=True)
        return 0
    except BaseException:
        print("R10ET_R5D_ERROR=" + traceback.format_exc(), flush=True)
        if patched and versions is not None:
            restore(root, versions)
            print("R10ET_R5D_ROLLBACK=True", flush=True)
        if "staged_before" in locals():
            print("R10ET_R5D_INDEX_PRESERVED=" + str(
                reviewed_index_snapshot(root) == staged_before
            ), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
