"""R52: pin the reviewed develop commit and all material mathematical sources.

R51 is merged, so its own old HEAD guard is intentionally not invoked.
No production files are modified or allowed to differ from their reviewed blobs.
"""
from __future__ import annotations

from phase174_r3_r7_r51_public_route_gap_audit.source_guard import (
    ROOT,
    REVIEWED_BLOBS as R51_PROTECTED_BLOBS,
    git,
    matches_blob,
)

REVIEWED_HEAD = "0d0b6b31582ff3e505d14fdde5eaf5e9a0b343d7"
R51_HANDOFF_BLOBS = {
    "phase174_r3_r7_r51_public_route_gap_audit/audit.py": "9f48c852950be09f44ef2ffe653c54a5fc59a090",
    "phase174_r3_r7_r51_public_route_gap_audit/source_guard.py": "28a3d2ff73a26a7edd29de90946d9bdcc7ffb9fd",
    "phase174_r3_r7_r51_public_route_gap_audit/tests/test_public.py": "2e7ee99bbdfe0c6e0720e615d9a932c9d9ac54c7",
}


def verify_checkout() -> dict[str, object]:
    """Reject unreviewed committed or tracked changes and all stale citations."""
    if git("rev-parse", "--show-toplevel") != str(ROOT):
        from pathlib import Path
        if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
            raise RuntimeError("R52 requires the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R52 requires branch develop")
    local = git("rev-parse", "HEAD")
    remote_line = git("ls-remote", "origin", "refs/heads/develop")
    remote = remote_line.split()[0] if remote_line else ""
    if local != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed develop HEAD: re-audit the R52 source pins")
    if git("diff", "--name-only") or git("diff", "--cached", "--name-only"):
        raise RuntimeError("R52 does not allow modified/staged tracked files")
    pins = {**R51_PROTECTED_BLOBS, **R51_HANDOFF_BLOBS}
    if len(pins) != len(R51_PROTECTED_BLOBS) + len(R51_HANDOFF_BLOBS):
        raise RuntimeError("R52 protected source paths overlap")
    for relative, sha in pins.items():
        path = ROOT / relative
        if not path.is_file() or not matches_blob(path.read_bytes(), sha):
            raise RuntimeError("Reviewed source changed: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": local,
        "remote_head": remote,
        "reviewed_files": len(pins),
        "production_files_changed": 0,
        "full_pytest": False,
    }
