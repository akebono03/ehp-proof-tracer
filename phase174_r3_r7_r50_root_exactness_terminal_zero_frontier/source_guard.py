"""R50 source guard: pin the reviewed R48 handoff and only allow R49-only merges."""
from __future__ import annotations

from pathlib import Path

from phase174_r3_r7_r46_prop42_dfs_audit.source_guard import (
    ROOT, git, matches_git_blob, R45_PRODUCTION_PINS, REVIEWED_SEARCH_BLOB,
)
from phase174_r3_r7_r48_cited_lower_kernel_tree_frontier.source_guard import (
    REVIEWED_RULE_BLOBS, R47_HANDOFF_FILES, normalized_sha256,
)
from phase174_r3_r7_r49_prop27_upper_delta_tree_frontier.source_guard import (
    PROP27_BLOBS, R48_HANDOFF_BLOBS,
)

REVIEWED_BASE_HEAD = "1d792feec594a67b83701d337b7745270c533484"
PERMITTED_MERGE_PREFIX = "phase174_r3_r7_r49_prop27_upper_delta_tree_frontier/"
ROOT_PROOF_SOURCE_BLOBS = {'phase165_r12_r15_toda51.py': '6a7120ba9955749a74ee90fe1d85e003f80873a0', 'phase165_r14_r39_toda51.tex': 'f582d1094e2e813f428a03b02426e407c58d610e', 'phase174_r3_r7_r3_ehp_zero_rule/rule.py': '8834cbefbfca5bcca18dc01f072c9738a05f7bdc', 'phase165_r12_r11_prop42_unified.py': '79752ec035244677ff6a54debff312e87a76fbf2', 'phase165_r52_r9_shared_math.py': '534b552856fefc8315b243fecc3170ee5792ebc7', 'phase169_r10e2_unpositioned_citation/source_first.py': 'b91b97a74d65b843fa8f9c19ffd082f684e461a7'}
R49_HANDOFF_SHA256 = {'phase174_r3_r7_r49_prop27_upper_delta_tree_frontier/audit.py': '40c73e1a1b70747a6e148c061012fdafef7ec1842efc80d411a16c879ab5c9d9', 'phase174_r3_r7_r49_prop27_upper_delta_tree_frontier/source_guard.py': '27847ae0b2871bb91aef56ac9dc3eba662d23238ed45190521f56d9bf47eb184', 'phase174_r3_r7_r49_prop27_upper_delta_tree_frontier/run.ps1': '7cb6988e40f6c1a986c8f69a899614f7f7af98733904844fb1cda90d580018dd', 'phase174_r3_r7_r49_prop27_upper_delta_tree_frontier/tests/test_frontier.py': '872d7249318017b269738e79f2353dfc7fc5caea547d664fad874004083688c8', 'phase174_r3_r7_r49_prop27_upper_delta_tree_frontier/tests/test_static.py': '63d7029ce715c1029bf79a105c72121bea41d1ebb0fc01ebc276643a539359f4', 'phase174_r3_r7_r49_prop27_upper_delta_tree_frontier/tests/test_guard.py': '22a5715e5ca39ed869d60f43d37eda2de7a50353b97092747ab4c25f098b17de'}


def verify_checkout() -> dict[str, object]:
    """Reject changed math, unreviewed merges, dirty tracked files or altered R49 handoff."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R50 must be extracted directly into the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R50 requires the develop branch")
    local_head = git("rev-parse", "HEAD")
    remote_parts = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_parts or remote_parts[0] != local_head:
        raise RuntimeError("Unreviewed or out-of-sync develop HEAD")
    if git("merge-base", REVIEWED_BASE_HEAD, local_head) != REVIEWED_BASE_HEAD:
        raise RuntimeError("R50 reviewed R48 commit is not a HEAD ancestor")
    changed = tuple(git("diff", "--name-only", REVIEWED_BASE_HEAD, local_head).splitlines())
    if any(not name.startswith(PERMITTED_MERGE_PREFIX) for name in changed):
        raise RuntimeError("Other committed changes require a new R50 source audit: " + repr(changed))
    staged = tuple(git("diff", "--cached", "--name-only").splitlines())
    modified = tuple(git("diff", "--name-only").splitlines())
    if staged or modified:
        raise RuntimeError("R50 requires no staged or modified tracked files: " + repr((staged, modified)))
    pinned = {
        **R45_PRODUCTION_PINS,
        **REVIEWED_RULE_BLOBS,
        **PROP27_BLOBS,
        **R48_HANDOFF_BLOBS,
        **ROOT_PROOF_SOURCE_BLOBS,
        "phase165_r3_recursive_search.py": REVIEWED_SEARCH_BLOB,
    }
    for relative, blob in pinned.items():
        path = ROOT / relative
        if not path.is_file() or not matches_git_blob(path.read_bytes(), blob):
            raise RuntimeError("R50 reviewed mathematical source differs: " + relative)
    for relative, digest in R47_HANDOFF_FILES.items():
        path = ROOT / relative
        if not path.is_file() or normalized_sha256(path.read_bytes()) != digest:
            raise RuntimeError("R47 handoff differs: " + relative)
    for relative, digest in R49_HANDOFF_SHA256.items():
        path = ROOT / relative
        if not path.is_file() or normalized_sha256(path.read_bytes()) != digest:
            raise RuntimeError("R49 handoff differs: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": local_head,
        "remote_head": remote_parts[0],
        "handoff_mode": "R49_MERGED" if changed else "R49_UNTRACKED_REVIEWED",
        "committed_audit_only_changes": len(changed),
        "pinned_mathematical_sources": len(pinned),
        "pinned_r49_handoff_files": len(R49_HANDOFF_SHA256),
        "tracked_changes": 0,
        "new_givens": 0,
        "production_files_changed": 0,
        "full_pytest": False,
    }
