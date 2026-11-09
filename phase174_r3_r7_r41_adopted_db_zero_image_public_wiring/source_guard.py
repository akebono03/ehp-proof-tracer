"""Source-first pinned Git and R40/R40R1 preconditions for R41 public wiring."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TARGET = "phase165_r52_r9_shared_math.py"
BASE_HEAD = "df93c0516dff64cddfebdac69d9755058322cdec"
BASE_BLOB = "6b965aa49db2ad8707c75dcc953d3c78cdd3e458"
UPSTREAM_PREFIXES = (
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/",
    "phase174_r3_r7_r40r1_matcher_order_test_fix/",
)
GIT_BLOB_PINS = {
    "phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py": "a1afa3f733e7dd324cb827ad7a1f6cb6ee90cf40",
    "phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py": "6aa48096b41714fbdf588c3ba423d264a4a13bb9",
    "phase174_r3_r7_r39_verified_zero_image_frontier/audit.py": "1e3b589bb221daa32c9ee1d21fb10a6dedcd2333",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}
SHA256_PINS = {
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py": "2df41f2787b76d8d35852c7de2300b90b5391cf9cadbc27b15bc62b122907a83",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/audit.py": "a838e53ca442a523c48a891a071b1860547d418e3c49476de545b6d84f13e0d5",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py": "dabd332aa0cbf036e55e9aacfe992d2a87ef50db9e296780246d3c3d066d4cf8",
}
ANCHOR = "    # R4-4 stage4: exactness-map binding from cited fixed statements only.\n"
INSERT = (
    "    # R41: retain DB-prior provenance and the actual cited source boundary.\n"
    "    # This only proposes an inference; it never registers a proof or GIVEN.\n"
    "    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (\n"
    "        build_public_adopted_zero_image_provider,\n"
    "    )\n"
    "    extra_providers = (\n"
    "        build_public_adopted_zero_image_provider(\n"
    "            bridge=bridge, proof_target=proof_target,\n"
    "        ),\n"
    "    ) + tuple(extra_providers)\n"
)


def git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, check=True,
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(("git",) + args, cwd=ROOT, check=True,
                          capture_output=True).stdout


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def matches_blob(data: bytes, expected: str) -> bool:
    data_lf = normalized(data)
    return len(expected) == 40 and expected in (
        blob(data), blob(data_lf), blob(data_lf.replace(b"\n", b"\r\n")),
    )


def expected_replacement(baseline: bytes) -> bytes:
    """Patch exactly one inspected anchor, without touching surrounding code."""
    original = normalized(baseline)
    anchor = ANCHOR.encode("utf-8")
    if (not matches_blob(original, BASE_BLOB)
            or original.count(anchor) != 1
            or INSERT.encode("utf-8") in original):
        raise RuntimeError("Unreviewed or ambiguous shared provider anchor")
    return original.replace(anchor, INSERT.encode("utf-8") + anchor, 1)


def verified_state() -> dict[str, object]:
    """Refuse unrelated changes or source edits; allow only R40 merge lineage."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R41 in the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R41 requires develop branch")
    local = git("rev-parse", "HEAD")
    remote_rows = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_rows:
        raise RuntimeError("Cannot verify origin/develop")
    remote = remote_rows[0]
    if remote != BASE_HEAD:
        git("fetch", "-q", "origin", "develop")
        if git("rev-parse", "FETCH_HEAD") != remote:
            raise RuntimeError("Remote lineage changed during check")
        if subprocess.run(("git", "merge-base", "--is-ancestor", BASE_HEAD, remote),
                          cwd=ROOT, capture_output=True).returncode != 0:
            raise RuntimeError("Unreviewed remote ancestry")
        changed = tuple(git("diff", "--name-only", BASE_HEAD, remote).splitlines())
        if not changed or any(not name.startswith(UPSTREAM_PREFIXES) for name in changed):
            raise RuntimeError("Remote advanced outside reviewed R40/R40R1 package")
    if local not in (BASE_HEAD, remote):
        raise RuntimeError("Unreviewed local HEAD")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require separate review")
    modified = tuple(git("diff", "--name-only").splitlines())
    if modified not in ((), (TARGET,)):
        raise RuntimeError("Unexpected tracked working-tree changes: " + repr(modified))
    for path, expected in GIT_BLOB_PINS.items():
        file = ROOT / path
        if not file.is_file() or not matches_blob(file.read_bytes(), expected):
            raise RuntimeError("Pinned source differs: " + path)
    for path, expected in SHA256_PINS.items():
        file = ROOT / path
        if (not file.is_file()
                or hashlib.sha256(normalized(file.read_bytes())).hexdigest() != expected):
            raise RuntimeError("R40/R40R1 reviewed file differs: " + path)
    baseline = git_bytes("show", "HEAD:" + TARGET)
    if not matches_blob(baseline, BASE_BLOB):
        raise RuntimeError("Shared math baseline differs from GitHub reviewed blob")
    expected = expected_replacement(baseline)
    current = normalized((ROOT / TARGET).read_bytes())
    base_lf = normalized(baseline)
    if current == base_lf:
        mode = "BASELINE"
    elif current == expected:
        mode = "INSTALLED"
    else:
        raise RuntimeError("Shared math differs from approved original or R41 replacement")
    if (mode == "BASELINE" and modified
            or mode == "INSTALLED" and modified != (TARGET,)):
        raise RuntimeError("Unexpected index/working-tree change state")
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "shared_math_mode": mode,
        "expected_change": TARGET,
        "reviewed_git_blobs": len(GIT_BLOB_PINS) + 1,
        "reviewed_r40_sha256_files": len(SHA256_PINS),
        "full_pytest": False,
    }
