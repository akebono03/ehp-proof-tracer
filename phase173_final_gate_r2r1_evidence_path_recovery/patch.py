"""Guarded two-file repair of the R2 preflight; does not touch production code."""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
from pathlib import Path


ORIGINAL_SHA256 = {
    "gate.py": "f282ff57ca4db29a4c8d0630f168084cafa205d30c7569e8e57c37a984d9a83c",
    "run.ps1": "0892e7245ef11e3225aa7202ef738488da824372009514f1fc3d5094b633a93c",
}
REPLACEMENT_SHA256 = {
    "gate.py": "71a2cea4ef928d7d2bc82e6ac90cf1233a1460ba1cecdf03d32627f9b8f19db2",
    "run.ps1": "d67c0b3ffdce14654fa62585e2205af9ad13d6eaa514437c8c65face251987ab",
}
TARGET_DIR = "phase173_final_gate_r2_recovery"


def digest(data: bytes) -> str:
    """Hash complete bytes; do not normalize source code or mathematical data."""
    return hashlib.sha256(data).hexdigest()


def reviewed_files(repo: Path, package: Path) -> tuple[tuple[Path, Path, str], ...]:
    """Fail on altered R2 input or on missing release replacements."""
    result: list[tuple[Path, Path, str]] = []
    for name, old_sha in ORIGINAL_SHA256.items():
        target = repo / TARGET_DIR / name
        replacement = package / "replacement" / name
        if not target.is_file() or not replacement.is_file():
            raise RuntimeError("R2 source or reviewed replacement is missing: " + name)
        present = digest(target.read_bytes())
        desired = digest(replacement.read_bytes())
        if desired != REPLACEMENT_SHA256[name]:
            raise RuntimeError("Reviewed R2R1 replacement has changed: " + name)
        if present not in (old_sha, desired):
            raise RuntimeError("R2 source has unreviewed local edits: " + name)
        state = "ALREADY_PATCHED" if present == desired else "REVIEWED_OLD"
        result.append((target, replacement, state))
    return tuple(result)


def _atomic_write(path: Path, content: bytes) -> None:
    """Replace one reviewed file without leaving truncated output."""
    temporary = path.with_name(path.name + ".phase173_r2r1_tmp")
    if temporary.exists():
        raise RuntimeError("Stale temporary file needs manual review: " + str(temporary))
    try:
        with temporary.open("xb") as stream:
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def apply_reviewed_patch(repo: Path, package: Path) -> tuple[str, ...]:
    """Back up original bytes before applying only the two reviewed files."""
    files = reviewed_files(repo, package)
    backup_dir = package / "original_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    for target, replacement, state in files:
        backup = backup_dir / target.name
        if backup.exists():
            if digest(backup.read_bytes()) != ORIGINAL_SHA256[target.name]:
                raise RuntimeError("An existing original backup differs: " + str(backup))
        elif state == "REVIEWED_OLD":
            with backup.open("xb") as output:
                output.write(target.read_bytes())
        elif state == "ALREADY_PATCHED":
            # Do not invent an original backup after the original has vanished.
            continue
    before = {target: target.read_bytes() for target, _, _ in files}
    changed: list[Path] = []
    try:
        for target, replacement, state in files:
            if state == "REVIEWED_OLD":
                _atomic_write(target, replacement.read_bytes())
                changed.append(target)
        if any(state != "ALREADY_PATCHED" for _, _, state in reviewed_files(repo, package)):
            raise RuntimeError("R2 patch did not reach the reviewed state")
    except Exception:
        for target in reversed(changed):
            _atomic_write(target, before[target])
        raise
    return tuple("R2R1_PATCHED_FILE=" + str(target.relative_to(repo))
                 for target in changed)


def rollback_reviewed_patch(repo: Path, package: Path) -> tuple[str, ...]:
    """Restore backed-up originals only if targets still equal our replacements."""
    files = reviewed_files(repo, package)
    backup_dir = package / "original_backups"
    changed: list[str] = []
    for target, _, state in files:
        if state == "ALREADY_PATCHED":
            backup = backup_dir / target.name
            if not backup.is_file() or digest(backup.read_bytes()) != ORIGINAL_SHA256[target.name]:
                raise RuntimeError("R2 original backup missing; refusing rollback: " + target.name)
            _atomic_write(target, backup.read_bytes())
            changed.append(str(target.relative_to(repo)))
    return tuple(changed)


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 173 R2R1 evidence-location patch")
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve(strict=True)
    package = args.package.resolve(strict=True)
    if args.apply and args.rollback:
        parser.error("--apply and --rollback are mutually exclusive")
    git_root = subprocess.run(
        ("git", "rev-parse", "--show-toplevel"), cwd=repo, capture_output=True,
        encoding="utf-8", errors="replace", check=True,
    ).stdout.strip()
    if Path(git_root).resolve() != repo:
        raise RuntimeError("Extract at EHP repository root")
    for target, replacement, state in reviewed_files(repo, package):
        print(f"PHASE173_FINAL_R2R1_SOURCE={target.name}:{state}")
        print(f"PHASE173_FINAL_R2R1_REPLACEMENT_SHA256={target.name}:{digest(replacement.read_bytes())}")
    if args.rollback:
        for name in rollback_reviewed_patch(repo, package):
            print("PHASE173_FINAL_R2R1_ROLLED_BACK=" + name)
    elif args.apply:
        for marker in apply_reviewed_patch(repo, package):
            print(marker)
        print("PHASE173_FINAL_R2R1_INSTALL=PASS")
    else:
        print("PHASE173_FINAL_R2R1_DRY_RUN=PASS")
        print("PHASE173_FINAL_R2R1_PRODUCTION_WRITES=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
