"""Read-only Git/working-tree verification for the reviewed R43 completion."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "f5b6899b124d435c224870476b2448454f77b1b5"
MERGED_HEAD = "02b9f8d743f57a0ad5c86ce3c63bbb8aee5e2b19"
TARGET = "phase165_r52_r9_shared_math.py"
BASE_SHA = "8bb72fe9b3fe22c1917c51971b12338d62be9e9b"
MERGED_SHA = "534b552856fefc8315b243fecc3170ee5792ebc7"
PINS = {
    "phase174_r3_r7_r43_public_ehp_map_property_wiring/audit.py": "de29f36886df76ebd234b88fa02dab8920c36e5c",
    "phase174_r3_r7_r43_public_ehp_map_property_wiring/tests/test_public.py": "fbc4dcdad82c36e21ff16f032dd1e95096949817",
    "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py": "9cf9dfa4b77a22bcbbe60b0c0b85dbf25cad50b2",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py": "dfa1519c629eef92ca1c5dae265acc050883649b",
    "phase174_r3_r7_r39_verified_zero_image_frontier/audit.py": "1e3b589bb221daa32c9ee1d21fb10a6dedcd2333",
    "phase174_r3_r7_r37_upper_delta_surjectivity_isolated/rule.py": "e388d8d20710d1d3e7df4bee115c98a0116e32b4",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(*arguments: str) -> str:
    return subprocess.run(
        ("git",) + arguments, cwd=ROOT, check=True, text=True,
        capture_output=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def matches_blob(data: bytes, expected: str) -> bool:
    normalized = normalize(data)
    return len(expected) == 40 and expected in (
        git_blob(data), git_blob(normalized),
        git_blob(normalized.replace(b"\n", b"\r\n")),
    )


def verify_checkout() -> dict[str, object]:
    """Accept only a clean R43 merge or its exactly reviewed unmerged patch."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R44 at repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R44 requires develop branch")
    remote_lines = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_lines or remote_lines[0] != MERGED_HEAD:
        raise RuntimeError("R43 remote HEAD changed: independent review required")
    head = git("rev-parse", "HEAD")
    if head not in (BASE_HEAD, MERGED_HEAD):
        raise RuntimeError("Unreviewed local HEAD")
    staged = tuple(git("diff", "--cached", "--name-only").splitlines())
    if staged:
        raise RuntimeError("Staged paths require review: " + repr(staged))
    tracked = tuple(git("diff", "--name-only").splitlines())
    if head == MERGED_HEAD:
        if tracked:
            raise RuntimeError("Tracked change outside reviewed R43 merged HEAD: " + repr(tracked))
        mode = "MERGED_R43_CLEAN"
    else:
        if tracked != (TARGET,):
            raise RuntimeError("Only the reviewed unmerged R43 code change is accepted: " + repr(tracked))
        baseline = subprocess.run(
            ("git", "show", "HEAD:" + TARGET), cwd=ROOT,
            check=True, capture_output=True,
        ).stdout
        if not matches_blob(baseline, BASE_SHA):
            raise RuntimeError("Unmerged R43 predecessor differs")
        mode = "REVIEWED_R43_UNMERGED"
    if not matches_blob((ROOT / TARGET).read_bytes(), MERGED_SHA):
        raise RuntimeError("Shared provider must equal the exact reviewed R43 merged blob")
    for path, expected_sha in PINS.items():
        source = ROOT / path
        if not source.is_file() or not matches_blob(source.read_bytes(), expected_sha):
            raise RuntimeError("Pinned source differs: " + path)
    return {
        "local_head": head,
        "remote_head": MERGED_HEAD,
        "source_guard": "PASS",
        "handoff_mode": mode,
        "reviewed_source_pins": len(PINS) + 1,
        "production_files_changed": 0,
        "full_pytest": False,
    }
