"""R46 reviewed source guard after the R45/R45R1 audit-only GitHub merge.

Unlike R45's older guard, this checks the current reviewed remote commit,
then verifies all unchanged mathematical sources and both R45 handoff files.
The accepted previous local HEAD is the direct parent of the new remote HEAD.
"""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from phase174_r3_r7_r45_ehp_open_obligation_audit.source_guard import (
    ROOT,
    PINS as R45_PRODUCTION_PINS,
    git,
    matches_git_blob,
)

PREVIOUS_REVIEWED_HEAD = "4b06ef96628b39e591cfa0b423fa0e0dec366a3b"
REVIEWED_HEAD = "4d37adab06b40330832c8ec1f08a1b7924ff95af"
REVIEWED_SEARCH_BLOB = "06009bfcf57f99cac58c229d99c53f16324692d0"
R45_LOCAL_PINS = {
    "phase174_r3_r7_r45_ehp_open_obligation_audit/audit.py": "4339a6281208edb27896cb5aa0e27315c655324de9876862c28ea27d4d1aeef5",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/source_guard.py": "726c99fae70021670eeacaa71584dec0f2c34cc1c87e7a7395c40a6dfd6426de",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1": "47e13f0876f0ac97292a0b55acb681c8763b7552cdf15211e0083bfa9fa5db89",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py": "a22bd2634bc22976793a8d4e205f3374117317e79b5323e1566670b5471b17ac",
}


def normalized_sha256(data: bytes) -> str:
    """Accept CRLF/LF conversions only, not edits to statement content."""
    return sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def verify_checkout() -> dict[str, object]:
    """Accept only the two reviewed checkout states with unchanged source bytes."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R46 ZIP must be extracted into repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R46 requires the develop branch")
    remote_line = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_line or remote_line[0] != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed GitHub develop HEAD; re-audit R46 pins")
    local_head = git("rev-parse", "HEAD")
    if local_head not in (PREVIOUS_REVIEWED_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Local HEAD differs from both reviewed R45 merge states")
    staged = git("diff", "--cached", "--name-only").splitlines()
    if staged:
        raise RuntimeError("Staged changes require separate review: " + repr(staged))
    tracked = git("diff", "--name-only").splitlines()
    if tracked:
        raise RuntimeError("Tracked changes require separate review: " + repr(tracked))
    for relative, expected_blob in R45_PRODUCTION_PINS.items():
        file_path = ROOT / relative
        if not file_path.is_file() or not matches_git_blob(
            file_path.read_bytes(), expected_blob
        ):
            raise RuntimeError("Reviewed mathematical source differs: " + relative)
    core_path = ROOT / "phase165_r3_recursive_search.py"
    if not core_path.is_file() or not matches_git_blob(
        core_path.read_bytes(), REVIEWED_SEARCH_BLOB
    ):
        raise RuntimeError("Canonical depth-first search source changed")
    for relative, expected_sha in R45_LOCAL_PINS.items():
        file_path = ROOT / relative
        if not file_path.is_file() or normalized_sha256(file_path.read_bytes()) != expected_sha:
            raise RuntimeError("R45R1 reviewed handoff changed: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": local_head,
        "remote_head": REVIEWED_HEAD,
        "mode": (
            "R45_R45R1_MERGED" if local_head == REVIEWED_HEAD
            else "R45_R45R1_PRE_MERGE_LOCAL"
        ),
        "r45_production_pins": len(R45_PRODUCTION_PINS),
        "r45r1_local_pins": len(R45_LOCAL_PINS),
        "search_core_pin": REVIEWED_SEARCH_BLOB,
        "tracked_changes": 0,
        "production_files_changed": 0,
        "full_pytest": False,
    }
