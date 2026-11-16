"""Successor-only worktree guard for the Phase 175 R3R8R1 public installer.

The earlier Phase 175 R3 guard remains unchanged.  Its R1/R2 source pins
are rechecked by the caller after this narrowly scoped status validation.
"""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import subprocess

from phase175_r3_pi73_hopf_lift import audit as r3


PACKAGE_NAME = "phase175_r3r8r1_verified_prior_public"
PUBLIC_TARGET = "phase165_r52_r9_shared_math.py"

# No prefix or wildcard acceptance. These are precisely the inspected files
# shipped in the R3R8R1/R3R8R1R1 package lineage, plus the present guard/tests.
REVIEWED_SUCCESSOR_WORKTREE_FILES = frozenset({
    PACKAGE_NAME + "/AUDIT_PLAN_JA.md",
    PACKAGE_NAME + "/CODE_FULL_JA.md",
    PACKAGE_NAME + "/README.md",
    PACKAGE_NAME + "/TEST_RESULTS_JA.md",
    PACKAGE_NAME + "/__init__.py",
    PACKAGE_NAME + "/audit.py",
    PACKAGE_NAME + "/install.py",
    PACKAGE_NAME + "/route.py",
    PACKAGE_NAME + "/rule.py",
    PACKAGE_NAME + "/run.ps1",
    PACKAGE_NAME + "/search_shared_group_goal_FULL.py.txt",
    PACKAGE_NAME + "/worktree_guard.py",
    PACKAGE_NAME + "/tests/__init__.py",
    PACKAGE_NAME + "/tests/test_install.py",
    PACKAGE_NAME + "/tests/test_lineage.py",
    PACKAGE_NAME + "/tests/test_public_search.py",
    PACKAGE_NAME + "/tests/test_route.py",
    PACKAGE_NAME + "/tests/test_verified_prior.py",
    PACKAGE_NAME + "/tests/test_worktree_guard.py",
})


def reviewed_tracked_snapshot(
    root: Path, *, allow_public_target: bool = False,
) -> dict[str, str]:
    """Hash only explicitly reviewed, unstaged tracked edits.

    Reject staged changes, renamed/deleted files, production modifications,
    unexpected files and duplicate status records. Untracked audit files are
    left under the original R1 policy. No Git mutation or status spoofing.
    """
    root = Path(root).resolve()
    process = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=no", "-z"],
        cwd=root, capture_output=True, check=False,
    )
    if process.returncode:
        raise RuntimeError("R3R8R1R2_GIT_STATUS_READ_FAILED")
    snapshot: dict[str, str] = {}
    for raw in process.stdout.split(b"\0"):
        if not raw:
            continue
        try:
            record = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise RuntimeError("R3R8R1R2_INVALID_GIT_STATUS_ENCODING") from exc
        if len(record) < 4 or record[:2] != " M" or record[2] != " ":
            raise RuntimeError("R3R8R1R2_STAGED_OR_OTHER_TRACKED_CHANGE: " + repr(record))
        relative = record[3:]
        allowed = (r3.R3_ALLOWED_TRACKED_EDITS | REVIEWED_SUCCESSOR_WORKTREE_FILES)
        if allow_public_target:
            allowed = allowed | {PUBLIC_TARGET}
        if relative not in allowed or relative in snapshot:
            raise RuntimeError("R3R8R1R2_PROTECTED_TRACKED_CHANGE: " + relative)
        candidate = root / relative
        if not candidate.is_file() or candidate.is_symlink():
            raise RuntimeError("R3R8R1R2_AUDIT_FILE_MISSING_OR_SYMLINK: " + relative)
        snapshot[relative] = sha256(candidate.read_bytes()).hexdigest()
    return dict(sorted(snapshot.items()))
