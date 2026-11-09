"""R47: fail closed on current reviewed R46/R46R1 merge and all source bytes.

Do not reuse an older phase's remote HEAD check: the reviewed merge
has a new commit but unchanged mathematical and search code.
"""
from __future__ import annotations

from pathlib import Path

from phase174_r3_r7_r46_prop42_dfs_audit.source_guard import (
    ROOT,
    R45_LOCAL_PINS,
    R45_PRODUCTION_PINS,
    REVIEWED_SEARCH_BLOB,
    git,
    matches_git_blob,
    normalized_sha256,
)

PREVIOUS_REVIEWED_HEAD = "4d37adab06b40330832c8ec1f08a1b7924ff95af"
REVIEWED_HEAD = "fe4f07940cdb5557397dc9e610b65b7eeaff0116"
REVIEWED_R46_FILES = {
    "phase174_r3_r7_r46_prop42_dfs_audit/audit.py": "e7a29e86de8b6b38dbac04e529aa26a03c9824b437be814eb610c3f0ad568f6a",
    "phase174_r3_r7_r46_prop42_dfs_audit/source_guard.py": "470b7c68f38268f976eebc7057ec932f8670138ab35b04ce55bcc45293f2e7cb",
}


def verify_checkout() -> dict[str, object]:
    """Check the latest GitHub merge and all previously reviewed handoff bytes."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R47 ZIP must be extracted in repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R47 requires develop branch")
    remote_line = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_line or remote_line[0] != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed GitHub develop HEAD; re-audit R47 pins")
    local_head = git("rev-parse", "HEAD")
    if local_head not in (PREVIOUS_REVIEWED_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Local HEAD is not a reviewed R46 merge state")
    staged = git("diff", "--cached", "--name-only").splitlines()
    if staged:
        raise RuntimeError("Staged changes require review: " + repr(staged))
    tracked = git("diff", "--name-only").splitlines()
    if tracked:
        raise RuntimeError("Tracked changes require review: " + repr(tracked))
    for relative, blob in R45_PRODUCTION_PINS.items():
        path = ROOT / relative
        if not path.is_file() or not matches_git_blob(path.read_bytes(), blob):
            raise RuntimeError("Reviewed production source changed: " + relative)
    search_core = ROOT / "phase165_r3_recursive_search.py"
    if not search_core.is_file() or not matches_git_blob(
        search_core.read_bytes(), REVIEWED_SEARCH_BLOB,
    ):
        raise RuntimeError("Reviewed canonical search core changed")
    for relative, sha in {**R45_LOCAL_PINS, **REVIEWED_R46_FILES}.items():
        path = ROOT / relative
        if not path.is_file() or normalized_sha256(path.read_bytes()) != sha:
            raise RuntimeError("Reviewed handoff bytes are unreviewed: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": local_head,
        "remote_head": REVIEWED_HEAD,
        "mode": "R46_MERGED" if local_head == REVIEWED_HEAD else "R46_PRE_MERGE_LOCAL",
        "reviewed_r46_files": len(REVIEWED_R46_FILES),
        "r46_production_pins": len(R45_PRODUCTION_PINS),
        "r46_local_pins": len(R45_LOCAL_PINS),
        "search_core_pin": REVIEWED_SEARCH_BLOB,
        "production_files_changed": 0,
        "full_pytest": False,
    }
