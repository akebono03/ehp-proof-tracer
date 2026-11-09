"""Read-only R45 source guard against the reviewed R44 merge on develop."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_HEAD = "02b9f8d743f57a0ad5c86ce3c63bbb8aee5e2b19"
REVIEWED_HEAD = "4b06ef96628b39e591cfa0b423fa0e0dec366a3b"
PINS = {
    "phase165_r52_r9_shared_math.py": "534b552856fefc8315b243fecc3170ee5792ebc7",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase165_r12_r12_ehp_consequences.py": "895dc98ad4d25f14fb7aac8fa52460a77fd049bc",
    "phase174_r3_r7_r44_public_zero_image_tree_frontier/audit.py": "42767b1945bcb3e00665c00b88f2ca37c7dd6d3c",
    "phase174_r3_r7_r43_public_ehp_map_property_wiring/audit.py": "de29f36886df76ebd234b88fa02dab8920c36e5c",
    "phase174_r3_r7_r37_upper_delta_surjectivity_isolated/rule.py": "e388d8d20710d1d3e7df4bee115c98a0116e32b4",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase166_r3l_reference_order.py": "faefcf0620f92bdf7f6222814467375a075cccf6",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def matches_git_blob(data: bytes, expected: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    variants = (
        data,
        normalized,
        normalized.replace(b"\n", b"\r\n"),
    )
    return len(expected) == 40 and any(
        git_blob_sha(candidate) == expected for candidate in variants
    )


def verify_checkout() -> dict[str, object]:
    """Require exact reviewed bytes, no staged or tracked edits, and develop."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R45 ZIP must be extracted into repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R45 requires the develop branch")
    remote_line = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_line or remote_line[0] != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed GitHub develop HEAD; re-audit R45 pins")
    local_head = git("rev-parse", "HEAD")
    if local_head not in (PREVIOUS_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Local HEAD is not the reviewed R44 handoff or merge")
    staged = git("diff", "--cached", "--name-only").splitlines()
    if staged:
        raise RuntimeError("Staged changes require separate review: " + repr(staged))
    tracked = git("diff", "--name-only").splitlines()
    if tracked:
        raise RuntimeError("Tracked changes require separate review: " + repr(tracked))
    for path, expected_sha in PINS.items():
        file_path = ROOT / path
        if not file_path.is_file() or not matches_git_blob(
            file_path.read_bytes(), expected_sha
        ):
            raise RuntimeError("Reviewed source differs: " + path)
    return {
        "source_guard": "PASS",
        "local_head": local_head,
        "remote_head": REVIEWED_HEAD,
        "mode": (
            "R44_MERGED" if local_head == REVIEWED_HEAD
            else "R44_PRE_MERGE_WITH_REVIEWED_AUDIT"
        ),
        "pinned_files": len(PINS),
        "tracked_changes": 0,
        "full_pytest": False,
    }
