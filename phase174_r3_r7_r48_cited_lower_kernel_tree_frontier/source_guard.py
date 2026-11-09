"""R48: independently verify reviewed GitHub HEAD and the R47 handoff bytes."""
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

PREVIOUS_HEAD = "fe4f07940cdb5557397dc9e610b65b7eeaff0116"
REVIEWED_HEAD = "398ad86615ec8484e5a9fe04143e367c059d4c85"
REVIEWED_RULE_BLOBS = {
    "phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py": "fac88c852cd4c18e8d013e3dc12ab95ad57d7b03",
    "phase174_r3_r7_r34_prior_lower_delta_source_wiring/source.py": "b90fe1fee5db04228ed986083b5214709045a7ea",
    "phase174_r3_r7_r36_cited_kernel_provider_wiring/audit.py": "b3d74e831edb49a60a54c5b609394fd815870068",
    "phase174_r3_r7_r32_lower_delta_kernel_audit/kernel_contract.py": "c2357859b00ed0b446bac7a060a6d0c134fc7de5",
    "phase165_r12_r29_kernel_connection.py": "170fc085a6d7a7aa9a9760647e35196f32f9f5ac",
}
R47_HANDOFF_FILES = {
    "phase174_r3_r7_r47_zero_image_prop42_hopf_bridge/audit.py": "da67d06bd4c558e9bd220cf3b1ea20d0bda7780965d9267b4248394592cb321c",
    "phase174_r3_r7_r47_zero_image_prop42_hopf_bridge/source_guard.py": "3acdc2aa7035fc2ee62190818d3ef2d7f78dcbf87b172feb29a9a733511d1161",
}


def verify_checkout() -> dict[str, object]:
    """Reject changed code, unknown local/remote HEAD, staged/dirty tracked files."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R48 ZIP must be extracted in the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R48 requires branch develop")
    remote_parts = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_parts or remote_parts[0] != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed GitHub develop HEAD; review new commits before R48")
    local_head = git("rev-parse", "HEAD")
    if local_head not in (PREVIOUS_HEAD, REVIEWED_HEAD):
        raise RuntimeError("R48 local HEAD differs from both reviewed R47 handoff states")
    staged = git("diff", "--cached", "--name-only").splitlines()
    tracked = git("diff", "--name-only").splitlines()
    if staged or tracked:
        raise RuntimeError("R48 requires no staged/tracked modifications: " + repr((staged, tracked)))
    for relative, blob in {**R45_PRODUCTION_PINS, **REVIEWED_RULE_BLOBS}.items():
        p = ROOT / relative
        if not p.is_file() or not matches_git_blob(p.read_bytes(), blob):
            raise RuntimeError("R48 reviewed mathematical source changed: " + relative)
    search = ROOT / "phase165_r3_recursive_search.py"
    if not search.is_file() or not matches_git_blob(search.read_bytes(), REVIEWED_SEARCH_BLOB):
        raise RuntimeError("R48 reviewed canonical search changed")
    for relative, digest in {**R45_LOCAL_PINS, **R47_HANDOFF_FILES}.items():
        p = ROOT / relative
        if not p.is_file() or normalized_sha256(p.read_bytes()) != digest:
            raise RuntimeError("R48 reviewed handoff file differs: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": local_head,
        "remote_head": REVIEWED_HEAD,
        "mode": "R47_MERGED" if local_head == REVIEWED_HEAD else "R47_REVIEWED_PRE_MERGE",
        "reviewed_mathematical_blobs": len(R45_PRODUCTION_PINS) + len(REVIEWED_RULE_BLOBS) + 1,
        "reviewed_r47_handoff_files": len(R47_HANDOFF_FILES),
        "new_given": 0,
        "production_files_changed": 0,
        "full_pytest": False,
    }
