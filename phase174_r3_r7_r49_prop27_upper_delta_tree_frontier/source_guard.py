"""R49: pin current develop, R48 audited handoff and mathematical sources."""
from __future__ import annotations

from pathlib import Path

from phase174_r3_r7_r46_prop42_dfs_audit.source_guard import (
    ROOT, git, matches_git_blob, R45_PRODUCTION_PINS, REVIEWED_SEARCH_BLOB,
)
from phase174_r3_r7_r48_cited_lower_kernel_tree_frontier.source_guard import (
    REVIEWED_RULE_BLOBS, R47_HANDOFF_FILES, normalized_sha256,
)

PREVIOUS_HEAD = "398ad86615ec8484e5a9fe04143e367c059d4c85"
REVIEWED_HEAD = "1d792feec594a67b83701d337b7745270c533484"
PROP27_BLOBS = {
    "phase174_r3_r7_r25_prop27_isolated_inference/rule.py": "e5ab7aa7a88f8ce49844ced057a81bd34c9a1e3b",
    "phase174_r3_r7_r28_prop27_typed_literature_registration/registration.py": "16d7caff9303f4f1da450175fe1fea00e7821c6c",
    "phase174_r3_r7_r29_prop27_canonical_provider/provider.py": "7e0c80051a1c2438172cde75ba0dfc5323d5eaff",
    "phase174_r3_r7_r30_prop27_public_provider_wiring/provider.py": "b54a73a5cb98803c9872973cbf194b0068ba6c8c",
    "phase174_r3_r7_r37_upper_delta_surjectivity_isolated/rule.py": "e388d8d20710d1d3e7df4bee115c98a0116e32b4",
}
R48_HANDOFF_BLOBS = {
    "phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/audit.py": "f082a3f9b1f5d2a8c724f6ac05395a1f6b5a8ca4",
    "phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/source_guard.py": "5c2aa1044c5a7eae93c884c98f7fd716eff78b70",
    "phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/tests/test_frontier.py": "0a44415cb731d568e2cee7c5d6aca5538703528f",
    "phase174_r3_r7_r48r2_source_bound_kernel_dfs_fix/patch.py": "2076facc8d6129a8446624006463cfefa3ece2e2",
}


def verify_checkout() -> dict[str, object]:
    """Require exact current reviewed bytes and clean develop checkout."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R49 must be extracted into the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R49 requires develop")
    remote_parts = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_parts or remote_parts[0] != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed GitHub develop HEAD; audit new changes before R49")
    local_head = git("rev-parse", "HEAD")
    if local_head not in (PREVIOUS_HEAD, REVIEWED_HEAD):
        raise RuntimeError("R49 local HEAD differs from reviewed R48 handoff")
    staged = git("diff", "--cached", "--name-only").splitlines()
    tracked = git("diff", "--name-only").splitlines()
    if staged or tracked:
        raise RuntimeError("R49 requires clean tracked files: " + repr((staged, tracked)))
    all_blobs = {
        **R45_PRODUCTION_PINS,
        **REVIEWED_RULE_BLOBS,
        **PROP27_BLOBS,
        **R48_HANDOFF_BLOBS,
        "phase165_r3_recursive_search.py": REVIEWED_SEARCH_BLOB,
    }
    for path, blob in all_blobs.items():
        file = ROOT / path
        if not file.is_file() or not matches_git_blob(file.read_bytes(), blob):
            raise RuntimeError("Reviewed GitHub source changed: " + path)
    for path, digest in R47_HANDOFF_FILES.items():
        file = ROOT / path
        if not file.is_file() or normalized_sha256(file.read_bytes()) != digest:
            raise RuntimeError("Reviewed R47 handoff changed: " + path)
    return {
        "source_guard": "PASS",
        "local_head": local_head,
        "remote_head": REVIEWED_HEAD,
        "handoff_mode": "R48_MERGED" if local_head == REVIEWED_HEAD else "R48_PRE_MERGE",
        "reviewed_blob_count": len(all_blobs),
        "reviewed_r47_handoff_count": len(R47_HANDOFF_FILES),
        "new_givens": 0,
        "production_files_changed": 0,
        "full_pytest": False,
    }
