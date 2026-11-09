"""Guarded, idempotent installation of one reviewed shared provider function."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = "phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py"
REVIEWED_HEAD = "4200211563834028ed6c4e2eeb01004646b92ba9"
REVIEWED_SUCCESSOR_PREFIX = "phase174_r3_r7_r35_isolated_cyclic_delta_kernel/"
GIT_PINS = {
    TARGET: "34b9cd021f768b404bbcbc8fe9d3cc7fe91b287f",
    "phase165_r52_r9_shared_math.py": "6b965aa49db2ad8707c75dcc953d3c78cdd3e458",
    "phase174_r3_r7_r34_prior_lower_delta_source_wiring/source.py":
        "b90fe1fee5db04228ed986083b5214709045a7ea",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r12_r2_quotient_rules.py": "2b3e8e0449382e9245ee22f08501e9cede0a5b59",
}
R35_PATH = "phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py"
R35_SHA256 = "f8eb16242ea91c6c8c1c3a991650e2708add16c06b9d4ac0741cae148b4e2847"


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, text=True,
        capture_output=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def canonical(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def reviewed_blob_matches(data: bytes, expected: str) -> bool:
    normalized = canonical(data)
    return any(
        git_blob_sha(candidate) == expected
        for candidate in (data, normalized, normalized.replace(b"\n", b"\r\n"))
    )


def baseline_source() -> str:
    return (PACKAGE / "baseline" / "context_provider_registry.py").read_text(
        encoding="utf-8-sig"
    ).replace("\r\n", "\n")


def replacement_source() -> str:
    return (PACKAGE / "replacement" / "context_provider_registry.py").read_text(
        encoding="utf-8-sig"
    ).replace("\r\n", "\n")


def patch_source(source: str) -> str:
    """Replace exactly the reviewed whole function; reject unreviewed changes."""
    if not isinstance(source, str):
        raise TypeError("source must be text")
    original = baseline_source()
    replacement = replacement_source()
    if source.replace("\r\n", "\n") == replacement:
        return replacement
    if source.replace("\r\n", "\n") != original:
        raise ValueError("Context provider code changed outside reviewed R36 scope")
    if not reviewed_blob_matches(original.encode("utf-8"), GIT_PINS[TARGET]):
        raise ValueError("R36 baseline does not match the reviewed GitHub code")
    compile(replacement, TARGET, "exec")
    return replacement


def verify_checkout() -> dict[str, object]:
    """Allow only the reviewed R34 HEAD and a R35-only merge successor."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R36 directly into repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R36 requires develop")
    local = git("rev-parse", "HEAD")
    raw_remote = git("ls-remote", "origin", "refs/heads/develop")
    remote = raw_remote.split()[0] if raw_remote else ""
    if not remote:
        raise RuntimeError("Cannot verify current GitHub develop")
    reviewed_additions: tuple[str, ...] = ()
    if remote != REVIEWED_HEAD:
        git("fetch", "-q", "origin", "develop")
        if git("rev-parse", "FETCH_HEAD") != remote:
            raise RuntimeError("Remote HEAD changed during source review")
        descendant = subprocess.run(
            ("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, remote),
            cwd=ROOT, capture_output=True,
        )
        if descendant.returncode != 0:
            raise RuntimeError("Remote HEAD has unreviewed lineage")
        reviewed_additions = tuple(
            git("diff", "--name-only", REVIEWED_HEAD, remote).splitlines()
        )
        if not reviewed_additions or any(
            not path.startswith(REVIEWED_SUCCESSOR_PREFIX)
            for path in reviewed_additions
        ):
            raise RuntimeError("Remote changed files beyond the reviewed R35 handoff")
    if local not in (REVIEWED_HEAD, remote):
        raise RuntimeError("Local HEAD requires review before R36 installation")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    changed = git("diff", "--name-only").splitlines()
    if changed not in ([], [TARGET]):
        raise RuntimeError("Unexpected tracked edits; no reset performed: " + repr(changed))
    for path, expected in GIT_PINS.items():
        if path == TARGET:
            data = baseline_source().encode("utf-8")
        else:
            file = ROOT / path
            if not file.is_file():
                raise RuntimeError("Reviewed file missing: " + path)
            data = file.read_bytes()
        if not reviewed_blob_matches(data, expected):
            raise RuntimeError("Reviewed GitHub blob mismatch: " + path)
    r35 = ROOT / R35_PATH
    if not r35.is_file() or hashlib.sha256(canonical(r35.read_bytes())).hexdigest() != R35_SHA256:
        raise RuntimeError("R35 isolated general rule missing or unreviewed")
    if not (PACKAGE / "baseline/context_provider_registry.py").is_file():
        raise RuntimeError("R36 replacement baseline missing")
    actual = (ROOT / TARGET).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    if actual not in (baseline_source(), replacement_source()):
        raise RuntimeError("Tracked context provider differs from both reviewed states")
    if (actual == baseline_source() and changed) or (actual == replacement_source() and changed != [TARGET]):
        raise RuntimeError("Tracked file state disagrees with reviewed R36 installation")
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "r35_rule_preserved": True,
        "r34_sources_preserved": True,
        "tracked_mode": "INSTALLED" if actual == replacement_source() else "BASELINE",
        "reviewed_successor_files": len(reviewed_additions),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    prefix = "PHASE174_R3R7R36_"
    for key, value in state.items():
        print(prefix + key.upper() + "=" + str(value))
    if args.dry_run:
        print(prefix + "GATE=PASS_R36_REVIEWED_SOURCE_PREFLIGHT")
        print("(END)")
        return 0
    file = ROOT / TARGET
    updated = patch_source(file.read_text(encoding="utf-8-sig"))
    if state["tracked_mode"] == "BASELINE":
        original_bytes = file.read_bytes()
        separator = "\r\n" if b"\r\n" in original_bytes else "\n"
        bom = b"\xef\xbb\xbf" if original_bytes.startswith(b"\xef\xbb\xbf") else b""
        file.write_bytes(bom + updated.replace("\n", separator).encode("utf-8"))
    verify_checkout()
    print(prefix + "MODE=INSTALLED")
    print(prefix + "GATE=PASS_R36_MINIMAL_CONTEXT_PROVIDER_INSTALLED")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
