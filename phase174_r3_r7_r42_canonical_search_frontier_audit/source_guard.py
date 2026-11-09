"""Read-only GitHub R41 handoff and source integrity gate for R42."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PRE_R41_HEAD = "92edf5d5c5025243e70e06e57baa9220668cc7b6"
REVIEWED_R41_HEAD = "f604062833ff4dc2756daa96235814983f98fbf2"
SHARED = "phase165_r52_r9_shared_math.py"
R41_PREFIX = "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/"
PINS = {
    SHARED: "8bb72fe9b3fe22c1917c51971b12338d62be9e9b",
    "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py": "9cf9dfa4b77a22bcbbe60b0c0b85dbf25cad50b2",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py": "dfa1519c629eef92ca1c5dae265acc050883649b",
    "phase174_r3_r7_r37_upper_delta_surjectivity_isolated/rule.py": "e388d8d20710d1d3e7df4bee115c98a0116e32b4",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def matches_blob(data: bytes, sha: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return len(sha) == 40 and sha in (
        git_blob(data), git_blob(normalized),
        git_blob(normalized.replace(b"\n", b"\r\n")),
    )


def verify_checkout() -> dict[str, object]:
    """Accept only the reviewed R41 merge or its exact uncommitted patch."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Unpack R42 directly into the Git repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R42 requires the develop branch")
    remote_line = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_line or remote_line[0] != REVIEWED_R41_HEAD:
        raise RuntimeError("Unreviewed remote HEAD; R42 refuses an unknown source")
    local = git("rev-parse", "HEAD")
    if local not in (PRE_R41_HEAD, REVIEWED_R41_HEAD):
        raise RuntimeError("Unreviewed local HEAD")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require separate review")
    changed = tuple(git("diff", "--name-only").splitlines())
    expected = (SHARED,) if local == PRE_R41_HEAD else ()
    if changed != expected:
        raise RuntimeError("Unexpected tracked edits: " + repr(changed))
    if local == PRE_R41_HEAD:
        git("fetch", "-q", "origin", "develop")
    if git("rev-parse", REVIEWED_R41_HEAD) != REVIEWED_R41_HEAD:
        raise RuntimeError("Reviewed R41 merge is not locally available")
    if subprocess.run(
        ("git", "merge-base", "--is-ancestor", PRE_R41_HEAD, REVIEWED_R41_HEAD),
        cwd=ROOT, capture_output=True,
    ).returncode != 0:
        raise RuntimeError("Unreviewed R41 history")
    upstream = tuple(git("diff", "--name-only", PRE_R41_HEAD, REVIEWED_R41_HEAD).splitlines())
    if (len(upstream) != 16
            or SHARED not in upstream
            or any(p != SHARED and not p.startswith(R41_PREFIX) for p in upstream)):
        raise RuntimeError("R41 merge includes unexpected paths")
    for path, sha in PINS.items():
        file = ROOT / path
        if not file.is_file() or not matches_blob(file.read_bytes(), sha):
            raise RuntimeError("Reviewed source differs: " + path)
    return {
        "local_head": local,
        "remote_head": REVIEWED_R41_HEAD,
        "source_guard": "PASS",
        "handoff_mode": "UNMERGED_R41_PATCH" if local == PRE_R41_HEAD else "MERGED_R41_CLEAN",
        "reviewed_merge_paths": len(upstream),
        "reviewed_source_pins": len(PINS),
        "production_files_changed": 0,
        "full_pytest": False,
    }
