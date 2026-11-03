"""Guarded, reversible one-module change for unbounded abstract prior matching."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

from phase173_r4_r15r1_unbounded_abstract_frontier.patch_source import (
    ORIGINAL_BLOB,
    TARGET,
    transform,
)

REVIEWED_ANCESTOR = "382cef8b866351b14fe1e717a283e50dc6f24555"
DEPENDENCIES = {
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase173_r4_r4_typed_generator_audit/audit.py": "82f9f734104ddb70df42090ee9a6413b06f1e98b",
    "phase173_r4_r6_alias_source_audit/audit.py": "9670dbd8c721e15e0c76b3e043accab6cb01daf3",
}
ALLOWED_TRACKED = {
    ".pytest_cache/v/cache/nodeids",
    "phase165_r52_r3_web_adapter.py",
    "phase173_r4_r13_narrative_audit/audit.py",
    "phase173_r4_r13_narrative_audit/tests/test_audit.py",
    "phase168_r3_5_model_renderer.py",
    TARGET,
}


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if completed.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + completed.stderr[:600])
    return completed.stdout.strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def package_path(root: Path) -> Path:
    return root / "phase173_r4_r15r1_unbounded_abstract_frontier"


def preflight(root: Path) -> tuple[bytes, bytes, bool]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("Run from the repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Only develop is supported")
    local = git(root, "rev-parse", "HEAD")
    remote = git(root, "rev-parse", "origin/develop")
    if local != remote:
        raise RuntimeError(f"GitHub/local HEAD mismatch: local={local} remote={remote}")
    git(root, "merge-base", "--is-ancestor", REVIEWED_ANCESTOR, local)
    if git(root, "rev-parse", "HEAD:" + TARGET) != ORIGINAL_BLOB:
        raise RuntimeError("Production base core differs from the reviewed Git blob")
    for path, expected in DEPENDENCIES.items():
        if git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("Committed dependency changed: " + path)
        committed = subprocess.run(
            ("git", "show", "HEAD:" + path), cwd=root,
            capture_output=True, check=True,
        ).stdout
        working = (root / path).read_bytes()
        if working.replace(b"\r\n", b"\n") != committed.replace(b"\r\n", b"\n"):
            raise RuntimeError("Local dependency changed: " + path)
    changed = set(filter(None, git(root, "diff", "--name-only").splitlines()))
    staged = git(root, "diff", "--cached", "--name-only")
    if staged:
        raise RuntimeError("Review staged changes before running")
    unexpected = changed - ALLOWED_TRACKED
    if unexpected:
        raise RuntimeError("Unexpected tracked changes: " + ", ".join(sorted(unexpected)))
    actual = (root / TARGET).read_bytes()
    baseline = subprocess.run(
        ("git", "show", "HEAD:" + TARGET), cwd=root, check=True,
        capture_output=True,
    ).stdout
    expected = transform(baseline)
    normalized = lambda value: value.replace(b"\r\n", b"\n")
    if normalized(actual) == normalized(baseline):
        candidate = transform(actual)
        installed = False
    elif normalized(actual) == normalized(expected):
        candidate = actual
        installed = True
    else:
        raise RuntimeError("Target has unexpected local edits")
    print("PHASE173_R4_R15R1_LOCAL_HEAD=" + local, flush=True)
    print("PHASE173_R4_R15R1_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R1_PREFLIGHT=PASS", flush=True)
    print("PHASE173_R4_R15R1_PREVIOUS_WORKTREE_PRESERVED=True", flush=True)
    return baseline, candidate, installed


def write_preview(root: Path, candidate: bytes) -> None:
    folder = package_path(root) / "reviewed_full_source"
    folder.mkdir(exist_ok=True)
    (folder / "phase173_r4_r10_core_FULL.py.txt").write_bytes(candidate)
    print("PHASE173_R4_R15R1_FULL_SOURCE=" + str(folder / "phase173_r4_r10_core_FULL.py.txt"), flush=True)


def apply(root: Path, *, dry_run: bool) -> None:
    baseline, candidate, installed = preflight(root)
    write_preview(root, candidate)
    if dry_run:
        print("PHASE173_R4_R15R1_DRY_RUN=PASS", flush=True)
        print("PHASE173_R4_R15R1_PRODUCTION_EDIT=NONE", flush=True)
        return
    if installed:
        print("PHASE173_R4_R15R1_ALREADY_INSTALLED=True", flush=True)
        return
    package = package_path(root)
    backup = package / "reviewed_full_source" / "original_core.py.bak"
    state = package / "reviewed_full_source" / "installed_state.json"
    if backup.exists() or state.exists():
        raise RuntimeError("Unreviewed existing backup/state requires inspection")
    backup.write_bytes(baseline)
    state.write_text(json.dumps({
        "original_sha256": sha256(baseline),
        "candidate_sha256": sha256(candidate),
        "target": TARGET,
    }, indent=2) + "\n", encoding="utf-8")
    temp = (root / TARGET).with_suffix(".phase173.tmp")
    try:
        temp.write_bytes(candidate)
        os.replace(temp, root / TARGET)
    finally:
        if temp.exists():
            temp.unlink()
    print("PHASE173_R4_R15R1_PATCHED=" + TARGET, flush=True)


def rollback(root: Path) -> None:
    package = package_path(root)
    state_path = package / "reviewed_full_source" / "installed_state.json"
    backup_path = package / "reviewed_full_source" / "original_core.py.bak"
    if not state_path.is_file() or not backup_path.is_file():
        raise RuntimeError("No reviewed backup available for rollback")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    target_path = root / TARGET
    actual = target_path.read_bytes()
    baseline = backup_path.read_bytes()
    if (sha256(baseline) != state["original_sha256"]
            or sha256(actual) != state["candidate_sha256"]):
        raise RuntimeError("Refusing rollback: source changed after installation")
    temp = target_path.with_suffix(".phase173.tmp")
    try:
        temp.write_bytes(baseline)
        os.replace(temp, target_path)
    finally:
        if temp.exists():
            temp.unlink()
    state_path.unlink()
    backup_path.unlink()
    print("PHASE173_R4_R15R1_ROLLBACK=PASS", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.rollback:
        rollback(root)
    else:
        apply(root, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
