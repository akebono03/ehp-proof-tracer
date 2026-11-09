"""R46R1: guarded, idempotent repair for R46's outdated parent Source Guard."""
from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path

from phase174_r3_r7_r45_ehp_open_obligation_audit.source_guard import (
    ROOT,
    PINS as R45_PRODUCTION_PINS,
    git,
    matches_git_blob,
)

PACKAGE = Path(__file__).resolve().parent
TARGET = "phase174_r3_r7_r46_prop42_dfs_audit/source_guard.py"
PREVIOUS_REVIEWED_HEAD = "4b06ef96628b39e591cfa0b423fa0e0dec366a3b"
REVIEWED_HEAD = "4d37adab06b40330832c8ec1f08a1b7924ff95af"
REVIEWED_SEARCH_BLOB = "06009bfcf57f99cac58c229d99c53f16324692d0"
R45_LOCAL_PINS = {
    "phase174_r3_r7_r45_ehp_open_obligation_audit/audit.py": "4339a6281208edb27896cb5aa0e27315c655324de9876862c28ea27d4d1aeef5",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/source_guard.py": "726c99fae70021670eeacaa71584dec0f2c34cc1c87e7a7395c40a6dfd6426de",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1": "47e13f0876f0ac97292a0b55acb681c8763b7552cdf15211e0083bfa9fa5db89",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py": "a22bd2634bc22976793a8d4e205f3374117317e79b5323e1566670b5471b17ac",
}


def normalized_sha256(data: bytes) -> str:
    return sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def reviewed_files() -> tuple[Path, Path, Path]:
    """The only permitted patch target and its two source-verified snapshots."""
    return (
        ROOT / TARGET,
        PACKAGE / "baseline" / "source_guard.py",
        PACKAGE / "replacement" / "source_guard.py",
    )


def verify_revised_merge() -> dict[str, object]:
    """Review remote/local lineage and all mathematics before modifying anything."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R46R1 must run from reviewed repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R46R1 requires develop branch")
    remote_line = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_line or remote_line[0] != REVIEWED_HEAD:
        raise RuntimeError("GitHub develop changed since the reviewed R45 merge")
    local_head = git("rev-parse", "HEAD")
    if local_head not in (PREVIOUS_REVIEWED_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Local checkout is not a reviewed R45 merge state")
    if git("diff", "--cached", "--name-only").splitlines():
        raise RuntimeError("R46R1 refuses staged changes")
    if git("diff", "--name-only").splitlines():
        raise RuntimeError("R46R1 refuses tracked modifications")
    for relative, blob in R45_PRODUCTION_PINS.items():
        candidate = ROOT / relative
        if not candidate.is_file() or not matches_git_blob(candidate.read_bytes(), blob):
            raise RuntimeError("Unreviewed mathematical source: " + relative)
    core = ROOT / "phase165_r3_recursive_search.py"
    if not core.is_file() or not matches_git_blob(core.read_bytes(), REVIEWED_SEARCH_BLOB):
        raise RuntimeError("Unreviewed shared search engine")
    for relative, digest in R45_LOCAL_PINS.items():
        candidate = ROOT / relative
        if not candidate.is_file() or normalized_sha256(candidate.read_bytes()) != digest:
            raise RuntimeError("Unreviewed R45/R45R1 audit file: " + relative)
    return {"local_head": local_head, "remote_head": REVIEWED_HEAD}


def pending_replacement() -> tuple[Path, Path, str]:
    destination, original, replacement = reviewed_files()
    if not all(path.is_file() for path in (destination, original, replacement)):
        raise RuntimeError("R46R1 reviewed replacement or target is missing")
    before = normalized_sha256(original.read_bytes())
    after = normalized_sha256(replacement.read_bytes())
    if before == after:
        raise RuntimeError("R46R1 replacement unexpectedly equals baseline")
    current = normalized_sha256(destination.read_bytes())
    if current not in (before, after):
        raise RuntimeError("Existing R46 guard differs from both reviewed snapshots")
    return destination, replacement, "ALREADY_REPAIRED" if current == after else "REPLACE"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    checkout = verify_revised_merge()
    destination, replacement, mode = pending_replacement()
    if not args.dry_run:
        if mode == "REPLACE":
            destination.write_bytes(replacement.read_bytes())
        if pending_replacement()[2] != "ALREADY_REPAIRED":
            raise RuntimeError("R46R1 replacement verification failed")
        from phase174_r3_r7_r46_prop42_dfs_audit.source_guard import verify_checkout
        if verify_checkout()["remote_head"] != REVIEWED_HEAD:
            raise RuntimeError("R46 source guard verification failed")
    prefix = "PHASE174_R3R7R46R1_"
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "LOCAL_HEAD=" + checkout["local_head"])
    print(prefix + "REMOTE_HEAD=" + checkout["remote_head"])
    print(prefix + "TARGET=" + destination.relative_to(ROOT).as_posix() + ":" + mode)
    print(prefix + "PRODUCTION_FILES_CHANGED=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "GATE=" + (
        "PASS_R46R1_MERGE_GUARD_DRYRUN" if args.dry_run
        else "PASS_R46R1_MERGE_GUARD_REPAIRED"
    ))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
