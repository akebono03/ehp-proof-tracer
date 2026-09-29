from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path

EXPECTED_HEAD = "3bcb84fe687ace64f15859df1f9dcb5da7113266"
PROTECTED_PREFIXES = ("tests/", "docs/development_log/", "docs/proof_records/")
PROTECTED_EXACT = {
    "README.md",
    "docs/design.md",
    "docs/development_log.md",
    "docs/proof_records.md",
    "docs/roadmap.md",
}


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def is_backup(path: str) -> bool:
    name = Path(path).name.lower()
    parts = [part.lower() for part in Path(path).parts]
    if ".before_phase" in name or name.endswith(".bak"):
        return True
    if "_backup" in name or ".phase" in name and "_backup" in name:
        return True
    return any(part.startswith(".phase") and part.endswith("_backup") for part in parts)


def is_protected(path: str) -> bool:
    if path in PROTECTED_EXACT:
        return True
    return path.startswith(PROTECTED_PREFIXES)


def collect_candidates(root: Path) -> list[str]:
    tracked = [line for line in git(root, "ls-files").splitlines() if line]
    candidates = [path for path in tracked if is_backup(path) and not is_protected(path)]
    return sorted(candidates)


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 145-1 safe repository cleanup")
    parser.add_argument("--apply", action="store_true", help="delete verified candidates")
    parser.add_argument("--allow-head-mismatch", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    head = git(root, "rev-parse", "HEAD").strip()
    if head != EXPECTED_HEAD and not args.allow_head_mismatch:
        print(f"STOP: HEAD mismatch: {head}")
        print(f"Expected: {EXPECTED_HEAD}")
        print("Re-run on the audited develop revision, or inspect changes before using --allow-head-mismatch.")
        return 2

    status_lines = [line for line in git(root, "status", "--porcelain").splitlines() if line]
    allowed_untracked_prefix = "?? phase145_1_repository_cleanup/"
    unexpected_status = [
        line for line in status_lines if line != allowed_untracked_prefix
    ]
    if unexpected_status:
        print("STOP: working tree has changes outside the Phase 145-1 package.")
        for line in unexpected_status:
            print(line)
        return 3

    candidates = collect_candidates(root)
    print(f"Phase 145-1 candidates: {len(candidates)} files")
    for path in candidates:
        print(path)

    if not args.apply:
        print("DRY RUN ONLY: no files were deleted.")
        print("Run again with --apply after reviewing the list.")
        return 0

    for path in candidates:
        if is_protected(path):
            raise RuntimeError(f"protected path reached deletion stage: {path}")
        target = root / path
        if target.is_file() or target.is_symlink():
            target.unlink()

    print(f"Deleted {len(candidates)} tracked backup files from the working tree.")
    print("Review with: git status --short")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
