"""Pin the actual current develop commit and its reviewed source files.

This guard does not use the stale R50 source guard, whose HEAD limit predates
its merger. No tracked production edits are allowed in this audit.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_HEAD = "a77592da1c8ae5aa1d33969ef9674ce914bce341"
REVIEWED_BLOBS = {
    "phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/audit.py": "033410427c965f73080d6a9c3ed42f93129b0950",
    "phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/source_guard.py": "ceb31b6f567858aca861235df68304cafd53a3c2",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "phase165_r52_r9_shared_math.py": "534b552856fefc8315b243fecc3170ee5792ebc7",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "phase165_r52_r3_web_adapter.py": "dda215780c0468cf421592aff86c79b1f5482eed",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py": "fac88c852cd4c18e8d013e3dc12ab95ad57d7b03",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r30_prop27_public_provider_wiring/provider.py": "b54a73a5cb98803c9872973cbf194b0068ba6c8c",
    "phase173_r4_r11_zero_public_connection/route.py": "e3230eed2dfa8dd3efc60cc0a03f787fa92bbeaa",
}


def git(*arguments: str) -> str:
    result = subprocess.run(("git",) + arguments, cwd=ROOT, check=True,
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace")
    return result.stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def matches_blob(data: bytes, expected: str) -> bool:
    canonical = data.replace(b"\r\n", b"\n")
    return any(git_blob(candidate) == expected for candidate in (
        data, canonical, canonical.replace(b"\n", b"\r\n"),
    ))


def verify_checkout() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R51 must be extracted into the checkout root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R51 requires develop")
    local = git("rev-parse", "HEAD")
    text = git("ls-remote", "origin", "refs/heads/develop")
    remote = text.split()[0] if text else ""
    if local != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed GitHub develop HEAD; re-audit required")
    if git("diff", "--cached", "--name-only") or git("diff", "--name-only"):
        raise RuntimeError("R51 requires no staged/modified tracked files")
    for relative, sha in REVIEWED_BLOBS.items():
        path = ROOT / relative
        if not path.is_file() or not matches_blob(path.read_bytes(), sha):
            raise RuntimeError("Reviewed file differs: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": local,
        "remote_head": remote,
        "reviewed_files": len(REVIEWED_BLOBS),
        "production_files_changed": 0,
        "full_pytest": False,
    }
