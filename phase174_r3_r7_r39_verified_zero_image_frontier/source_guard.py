"""Read-only source and Git lineage checks for Phase 174 R3-R7-R39."""
from __future__ import annotations

import hashlib
from pathlib import Path
import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "2e3fcfbea1a3816b146cf53320f9a3bbee618c52"
ALLOWED_UPSTREAM_PREFIXES = (
    "phase174_r3_r7_r38_source_bound_zero_image_public_wiring/",
    "phase174_r3_r7_r38r1_r9_sha_pin_fix/",
)
CONTEXT = "phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py"
PROVIDER = "phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py"
PINS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py": "66407339808ed4ba8a65c04fd3bfbbf05bde6745",
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": "d98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6",
    "phase174_r3_r7_r9_composition_associativity/rule.py": "2c44c68be90cb761d7bdd35e29f23977b5f93a2e",
    "phase174_r3_r7_r12_toda59_annihilator_source/rule.py": "32a5a2723cc19506695d4423e7ccb331d6f36ae2",
    "phase174_r3_r7_r13_cited_annihilator_bridge/registry.py": "489380d974d9e3a2869743325d21b15b4d64f808",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase169_r10eq_r1_universal_stable_definition/definition.py": "0c74d121419b6755e947a367d7de465d81193174",
}


def git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, check=True,
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def matches_blob(data: bytes, sha: str) -> bool:
    clean = normalized(data)
    return len(sha) == 40 and sha in (
        git_blob(data), git_blob(clean), git_blob(clean.replace(b"\n", b"\r\n")),
    )


def verify_checkout() -> dict[str, object]:
    """Allow only reviewed R38 merge or one R38 local tracked change."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R39 directly at repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R39 requires develop branch")
    local = git("rev-parse", "HEAD")
    output = git("ls-remote", "origin", "refs/heads/develop")
    remote = output.split()[0] if output else ""
    if not remote:
        raise RuntimeError("Cannot verify origin/develop")
    if remote != BASE_HEAD:
        git("fetch", "-q", "origin", "develop")
        if git("rev-parse", "FETCH_HEAD") != remote:
            raise RuntimeError("Remote changed while examining lineage")
        rc = subprocess.run(("git", "merge-base", "--is-ancestor", BASE_HEAD, remote),
                            cwd=ROOT, capture_output=True).returncode
        if rc != 0:
            raise RuntimeError("Unknown remote lineage")
        advance = tuple(git("diff", "--name-only", BASE_HEAD, remote).splitlines())
        if not advance or any(not path.startswith(ALLOWED_UPSTREAM_PREFIXES)
                              and path != CONTEXT for path in advance):
            raise RuntimeError("Remote changed outside reviewed R38 scope")
    else:
        advance = ()
    if local not in (BASE_HEAD, remote):
        raise RuntimeError("Unknown local HEAD")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require separate review")
    changed = tuple(git("diff", "--name-only").splitlines())
    if changed not in ((), (CONTEXT,)):
        raise RuntimeError("Unexpected tracked edits")
    for path, sha in PINS.items():
        item = ROOT / path
        if not item.is_file() or not matches_blob(item.read_bytes(), sha):
            raise RuntimeError("Reviewed source differs: " + path)
    r38 = ROOT / "phase174_r3_r7_r38_source_bound_zero_image_public_wiring"
    baseline = r38 / "baseline" / "context_provider_registry.py"
    replacement = r38 / "replacement" / "context_provider_registry.py"
    if not (baseline.is_file() and replacement.is_file()):
        raise RuntimeError("R38 reviewed baseline and replacement absent")
    if normalized(baseline.read_bytes()) == normalized(replacement.read_bytes()):
        raise RuntimeError("R38 replacement does not differ from baseline")
    context = ROOT / CONTEXT
    if not context.is_file() or normalized(context.read_bytes()) != normalized(replacement.read_bytes()):
        raise RuntimeError("R38 public provider not installed or modified")
    if not (ROOT / PROVIDER).is_file() or not matches_blob((ROOT / PROVIDER).read_bytes(), R38_PROVIDER_BLOB):
        raise RuntimeError("R38 provider differs from reviewed implementation")
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "reviewed_r38_upstream_files": len(advance),
        "tracked_changes": list(changed),
        "public_r38_installed": True,
        "full_pytest": False,
    }


R38_PROVIDER_BLOB = "6aa48096b41714fbdf588c3ba423d264a4a13bb9"
