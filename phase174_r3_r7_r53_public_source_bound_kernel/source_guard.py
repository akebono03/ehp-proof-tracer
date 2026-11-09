"""R53 source guard: pin the R52-merged GitHub develop and reviewed code blobs."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_HEAD = "1151d6a3044fd7fae2ff1fb864a83afdaefc285d"
TARGET = "phase165_r55_nk_only_goal.py"
TARGET_BLOB = "9aa232c8f98a7a75f27266044224eddfa98c5e04"
REVIEWED_BLOBS = {
    "phase165_r52_r9_shared_math.py": "534b552856fefc8315b243fecc3170ee5792ebc7",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "phase174_r3_r7_r52_public_kernel_source_bound_probe/probe.py": "1e7d44acd7829fad858c2c88139174fe61c59fa7",
    "phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py": "fac88c852cd4c18e8d013e3dc12ab95ad57d7b03",
    "phase174_r3_r7_r37_upper_delta_surjectivity_isolated/rule.py": "e388d8d20710d1d3e7df4bee115c98a0116e32b4",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/audit.py": "033410427c965f73080d6a9c3ed42f93129b0950",
    "phase174_r3_r7_r51_public_route_gap_audit/audit.py": "9f48c852950be09f44ef2ffe653c54a5fc59a090",
    "phase174_r3_r7_r52r2_registry_assertion_id_fix/replacement/audit.py": "233f6b4a0283309cbde0a5ebee9235a2e303506b",
}


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args,
        cwd=ROOT, capture_output=True, check=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, capture_output=True, check=True,
    ).stdout


def git_blob(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\x00" + data
    ).hexdigest()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def verify_checkout() -> dict[str, object]:
    """Fail closed for unreviewed HEAD, source edits, staged paths and blobs."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R53 must be unpacked under the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R53 expects the develop branch")
    head = git("rev-parse", "HEAD")
    remote = git("ls-remote", "origin", "refs/heads/develop")
    remote_head = remote.split()[0] if remote else ""
    if head != REVIEWED_HEAD or remote_head != REVIEWED_HEAD:
        raise RuntimeError("Reviewed R52 HEAD differs: source audit required")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged modifications require review before R53")
    changed = tuple(git("diff", "--name-only").splitlines())
    if any(item != TARGET for item in changed):
        raise RuntimeError("Unreviewed tracked working change: " + repr(changed))
    reviewed = {TARGET: TARGET_BLOB, **REVIEWED_BLOBS}
    for relative, expected in reviewed.items():
        contents = git_bytes("show", "HEAD:" + relative)
        if git_blob(contents) != expected:
            raise RuntimeError("GitHub-reviewed committed blob changed: " + relative)
        if relative != TARGET and normalized((ROOT / relative).read_bytes()) != normalized(contents):
            raise RuntimeError("Pinned mathematical or public code changed locally: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": head,
        "remote_head": remote_head,
        "reviewed_blob_count": len(reviewed),
        "tracked_changes": changed,
        "full_pytest": False,
    }
