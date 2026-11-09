"""Pin reviewed R42 handoff and both existing conditional EHP rules."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "f604062833ff4dc2756daa96235814983f98fbf2"
REVIEWED_R42_HEAD = "f5b6899b124d435c224870476b2448454f77b1b5"
TARGET = "phase165_r52_r9_shared_math.py"
BASE_BLOB = "8bb72fe9b3fe22c1917c51971b12338d62be9e9b"
R42_PREFIX = "phase174_r3_r7_r42_canonical_search_frontier_audit/"
PINS = {
    "phase174_r3_r7_r42_canonical_search_frontier_audit/audit.py": "e17f15093dc434eced7755df5769424b86b0cd30",
    "phase174_r3_r7_r42_canonical_search_frontier_audit/tests/test_frontier.py": "412689d808fd5c86f864259a390df8b7d8936603",
    "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py": "9cf9dfa4b77a22bcbbe60b0c0b85dbf25cad50b2",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py": "dfa1519c629eef92ca1c5dae265acc050883649b",
    "phase174_r3_r7_r37_upper_delta_surjectivity_isolated/rule.py": "e388d8d20710d1d3e7df4bee115c98a0116e32b4",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
}
ANCHOR = "    # R4-4 stage4: exactness-map binding from cited fixed statements only.\n"
INSERT = (
    "    # R43: add only two source-dependent, conditional EHP map-property goals.\n"
    "    # No citation, verified proof, or GIVEN is registered by these providers.\n"
    "    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (\n"
    "        expand_hopf_injective_from_zero_image,\n"
    "    )\n"
    "    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (\n"
    "        expand_upper_delta_surjectivity,\n"
    "    )\n"
    "    extra_providers = (\n"
    "        expand_hopf_injective_from_zero_image,\n"
    "        expand_upper_delta_surjectivity,\n"
    "    ) + tuple(extra_providers)\n"
)


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, capture_output=True,
    ).stdout


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def blob(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data,
    ).hexdigest()


def matches_blob(data: bytes, expected: str) -> bool:
    canonical = normalize(data)
    return (len(expected) == 40 and expected in (
        blob(data), blob(canonical), blob(canonical.replace(b"\n", b"\r\n")),
    ))


def expected_replacement(original: bytes) -> bytes:
    """Insert only one guardable provider registration, preserving everything else."""
    source = normalize(original)
    anchor = ANCHOR.encode("utf-8")
    inserted = INSERT.encode("utf-8")
    if (not matches_blob(source, BASE_BLOB)
            or source.count(anchor) != 1
            or inserted in source):
        raise RuntimeError("Unexpected shared provider R41 base or insertion anchor")
    return source.replace(anchor, inserted + anchor, 1)


def verify_checkout() -> dict[str, object]:
    """Fail closed unless exactly reviewed R42 history and R43 code state exist."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R43 at the Git repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R43 requires develop branch")
    remote_rows = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_rows or remote_rows[0] != REVIEWED_R42_HEAD:
        raise RuntimeError("Unreviewed remote HEAD: R42 handoff changed")
    remote = remote_rows[0]
    local = git("rev-parse", "HEAD")
    if local not in (BASE_HEAD, REVIEWED_R42_HEAD):
        raise RuntimeError("Unreviewed local HEAD for R43")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require separate review")
    if local != remote:
        git("fetch", "-q", "origin", "develop")
        if git("rev-parse", "FETCH_HEAD") != remote:
            raise RuntimeError("Remote changed during Source Guard")
    status = subprocess.run(
        ("git", "merge-base", "--is-ancestor", BASE_HEAD, remote),
        cwd=ROOT, capture_output=True,
    ).returncode
    if status != 0:
        raise RuntimeError("Unreviewed R42 ancestry")
    changed_upstream = tuple(git(
        "diff", "--name-only", BASE_HEAD, remote,
    ).splitlines())
    if (len(changed_upstream) != 11
            or any(not path.startswith(R42_PREFIX) for path in changed_upstream)):
        raise RuntimeError("R42 remote merge changed unrelated files")
    for path, sha in PINS.items():
        p = ROOT / path
        if not p.is_file() or not matches_blob(p.read_bytes(), sha):
            raise RuntimeError("Reviewed source differs: " + path)
    reference = git_bytes("show", "HEAD:" + TARGET)
    if not matches_blob(reference, BASE_BLOB):
        raise RuntimeError("Shared provider source differs from reviewed R41 HEAD")
    expected = expected_replacement(reference)
    current = normalize((ROOT / TARGET).read_bytes())
    if current == normalize(reference):
        mode = "BASELINE"
    elif current == expected:
        mode = "INSTALLED"
    else:
        raise RuntimeError("Shared provider has unreviewed code changes")
    changed = tuple(git("diff", "--name-only").splitlines())
    required = () if mode == "BASELINE" else (TARGET,)
    if changed != required:
        raise RuntimeError("Unexpected tracked working tree edits: " + repr(changed))
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "r42_reviewed_files": len(changed_upstream),
        "reviewed_source_pins": len(PINS) + 1,
        "shared_math_mode": mode,
        "tracked_change": TARGET if mode == "INSTALLED" else "NONE",
        "full_pytest": False,
    }
