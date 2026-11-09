"""Review-bound Git and source checks for isolated R40 audit."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_R38_HEAD = "edf3672a709bde915ba28fa868a134e4a9ae18e7"
REVIEWED_R39_PREFIX = "phase174_r3_r7_r39_verified_zero_image_frontier/"
PINS = {
    "phase174_r3_r7_r39_verified_zero_image_frontier/audit.py": "1e3b589bb221daa32c9ee1d21fb10a6dedcd2333",
    "phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py": "6aa48096b41714fbdf588c3ba423d264a4a13bb9",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py": "66407339808ed4ba8a65c04fd3bfbbf05bde6745",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py": "a1afa3f733e7dd324cb827ad7a1f6cb6ee90cf40",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, check=True,
                          text=True, capture_output=True,
                          encoding="utf-8", errors="replace").stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def matches_blob(data: bytes, expected: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return len(expected) == 40 and expected in (
        git_blob(data), git_blob(normalized),
        git_blob(normalized.replace(b"\n", b"\r\n")),
    )


def verify_checkout() -> dict[str, object]:
    """Allow only the actual R39 merge, no unrelated edits or relaxed hashes."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R40 at repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD")
    remote_output = git("ls-remote", "origin", "refs/heads/develop")
    remote = remote_output.split()[0] if remote_output else ""
    if not remote:
        raise RuntimeError("Cannot verify remote develop")
    if remote != REVIEWED_R38_HEAD:
        git("fetch", "-q", "origin", "develop")
        if git("rev-parse", "FETCH_HEAD") != remote:
            raise RuntimeError("Remote changed during review")
        process = subprocess.run(("git", "merge-base", "--is-ancestor", REVIEWED_R38_HEAD, remote),
                                 cwd=ROOT, capture_output=True)
        if process.returncode != 0:
            raise RuntimeError("Unreviewed remote history")
        changed_remote = tuple(git("diff", "--name-only", REVIEWED_R38_HEAD, remote).splitlines())
        if not changed_remote or any(not p.startswith(REVIEWED_R39_PREFIX) for p in changed_remote):
            raise RuntimeError("Remote changed outside reviewed R39")
    else:
        changed_remote = ()
    if local not in (REVIEWED_R38_HEAD, remote):
        raise RuntimeError("Unreviewed local HEAD")
    if git("diff", "--cached", "--name-only") or git("diff", "--name-only"):
        raise RuntimeError("Unexpected tracked edits")
    for path, sha in PINS.items():
        item = ROOT / path
        if not item.is_file() or not matches_blob(item.read_bytes(), sha):
            raise RuntimeError("Reviewed source differs: " + path)
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "reviewed_r39_merge_files": len(changed_remote),
        "reviewed_source_pins": len(PINS),
    }
