"""R54: review both pre-merge and R53-merged public HTTP code strictly."""
from __future__ import annotations

from pathlib import Path

from phase174_r3_r7_r53_public_source_bound_kernel.install import patched_source
from phase174_r3_r7_r53_public_source_bound_kernel.source_guard import (
    ROOT, REVIEWED_HEAD as R52_MERGED_HEAD, git, git_blob, git_bytes, normalized,
    verify_checkout as verify_r53_unmerged,
)

R53_MERGED_HEAD = "e2598a3b4c865afea15b06b097c809333fabcc85"
TARGET = "phase165_r55_nk_only_goal.py"
ORIGINAL_TARGET_BLOB = "9aa232c8f98a7a75f27266044224eddfa98c5e04"
INSTALLED_TARGET_BLOB = "e436879f578148fe5c30f5a34974bea3425108b2"
PINNED_WEB_BLOBS = {
    "web_app.py": "6f95663df5cbf028bb16d1f05dca62db2e3fc00e",
    "templates/index.html": "7af2afa40b92b8c1ec3916cf9759516c158b989f",
    "phase165_r52_r4_flask_bridge.py": "aec7615671ea0b472d4f6093c06fc0f857632db7",
    "phase165_r52_r3_web_adapter.py": "dda215780c0468cf421592aff86c79b1f5482eed",
    "phase168_r3_5_model_renderer.py": "64e0570e8462ee0361ed07afab836c66ce8e7895",
    "phase168_r3_41p13_trust_boundary/verification.py": "547464846ce574d227092a4aacb895d2e2dfefca",
    "tests/test_phase145_group_proof_defaults.py": "914d045cfd9615afa90cd0e877c298b7fd994426",
    "test_phase165_r52_r4_flask_connection.py": "45e42093449f9b09dfbba5e86bcbd56d86bf3d80",
}


def verify_checkout() -> dict[str, object]:
    """Accept only two reviewed source states, with identical installed R53 bytes."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R54 must be unpacked under the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R54 expects the develop branch")
    head = git("rev-parse", "HEAD")
    remote = git("ls-remote", "origin", "refs/heads/develop")
    remote_head = remote.split()[0] if remote else ""
    if head != remote_head or head not in (R52_MERGED_HEAD, R53_MERGED_HEAD):
        raise RuntimeError("R54 GitHub HEAD must be the reviewed R52 or R53 commit")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("R54 requires an unstaged and unmodified Git index")
    working_changes = tuple(git("diff", "--name-only").splitlines())
    mode = "R53_UNCOMMITTED" if head == R52_MERGED_HEAD else "R53_MERGED"
    allowed = (TARGET,) if mode == "R53_UNCOMMITTED" else ()
    if working_changes != allowed:
        raise RuntimeError("R54 found unreviewed tracked working changes: " + repr(working_changes))
    baseline = git_bytes("show", R52_MERGED_HEAD + ":" + TARGET)
    if git_blob(baseline) != ORIGINAL_TARGET_BLOB:
        raise RuntimeError("R52 reviewed public search target changed")
    updated = patched_source(normalized(baseline).decode("utf-8-sig"))
    current = normalized((ROOT / TARGET).read_bytes()).decode("utf-8-sig")
    if current != updated:
        raise RuntimeError("R53 public Source-bound implementation is not installed")
    head_target = git_bytes("show", "HEAD:" + TARGET)
    expected_head_blob = (
        ORIGINAL_TARGET_BLOB if mode == "R53_UNCOMMITTED" else INSTALLED_TARGET_BLOB
    )
    if git_blob(head_target) != expected_head_blob:
        raise RuntimeError("Unexpected committed public search function blob")
    if mode == "R53_UNCOMMITTED":
        verify_r53_unmerged()
    for relative, expected in PINNED_WEB_BLOBS.items():
        source = git_bytes("show", "HEAD:" + relative)
        if git_blob(source) != expected:
            raise RuntimeError("Unreviewed R54 HTTP source blob: " + relative)
        installed = (ROOT / relative).read_bytes()
        if normalized(installed) != normalized(source):
            raise RuntimeError("HTTP or narrative source changed: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": head,
        "remote_head": remote_head,
        "handoff_mode": mode,
        "r53_public_wiring_installed": True,
        "reviewed_http_and_renderer_blobs": len(PINNED_WEB_BLOBS),
        "tracked_changes": working_changes,
        "production_files_changed_by_r54": 0,
        "new_given": 0,
        "new_math_rules": 0,
        "full_pytest": False,
    }
