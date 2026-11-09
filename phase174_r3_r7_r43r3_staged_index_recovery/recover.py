"""Unstage only the twelve reviewed R43 package additions; preserve worktree bytes."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HEAD = "f5b6899b124d435c224870476b2448454f77b1b5"
FOLDER = "phase174_r3_r7_r43_public_ehp_map_property_wiring"
STAGED_ADDITIONS = (
    "AUDIT_PLAN_JA.md",
    "CODE_FULL_JA.md",
    "README.md",
    "TEST_RESULTS_JA.md",
    "__init__.py",
    "audit.py",
    "install.py",
    "run.ps1",
    "source_guard.py",
    "tests/test_guard.py",
    "tests/test_public.py",
    "tests/test_static.py",
)
PATHS = tuple(FOLDER + "/" + name for name in STAGED_ADDITIONS)


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def validate_index(
    staged_entries: tuple[tuple[str, str], ...],
    unstaged_tracked_paths: tuple[str, ...],
    untracked_paths: tuple[str, ...],
) -> str:
    """Permit only exactly twelve staged additions or all twelve untracked files."""
    if unstaged_tracked_paths:
        raise RuntimeError("Tracked worktree edits need separate review: "
                           + repr(unstaged_tracked_paths))
    actual = tuple(path for _status, path in staged_entries)
    if len(actual) != len(set(actual)):
        raise RuntimeError("Duplicate staged paths")
    if staged_entries:
        if (set(actual) != set(PATHS) or len(actual) != len(PATHS)
                or any(status != "A" for status, _path in staged_entries)):
            raise RuntimeError("Unexpected staged changes; nothing was unstaged: "
                               + repr(staged_entries))
        return "EXACT_R43_NEW_FILES_STAGED"
    if not set(PATHS).issubset(set(untracked_paths)):
        raise RuntimeError("R43 package is not an intact untracked worktree: "
                           + repr(tuple(sorted(set(PATHS) - set(untracked_paths)))))
    return "ALREADY_UNSTAGED"


def verify_checkout() -> dict[str, object]:
    """Inspect the actual Git index, never infer safety from a directory name."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R43R3 at the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R43R3 requires develop")
    local_head = git("rev-parse", "HEAD")
    remote_lines = git("ls-remote", "origin", "refs/heads/develop").split()
    remote_head = remote_lines[0] if remote_lines else ""
    if local_head != EXPECTED_HEAD or remote_head != EXPECTED_HEAD:
        raise RuntimeError("Unreviewed HEAD: local=" + local_head + "; remote=" + remote_head)
    raw_status = git("diff", "--cached", "--name-status")
    staged: list[tuple[str, str]] = []
    for line in raw_status.splitlines():
        fields = line.split("\t", 1)
        if len(fields) != 2:
            raise RuntimeError("Unexpected staged Git status: " + repr(line))
        staged.append((fields[0], fields[1]))
    modified = tuple(git("diff", "--name-only").splitlines())
    untracked = tuple(git("ls-files", "--others", "--exclude-standard").splitlines())
    status = validate_index(tuple(staged), modified, untracked)
    if not all((ROOT / path).is_file() for path in PATHS):
        raise RuntimeError("One of the reviewed R43 worktree files is absent")
    for path in (
        "phase174_r3_r7_r43r2_reviewed_tracked_change_guard/run.ps1",
        "phase174_r3_r7_r43r1_r3_sha_pin_fix/run.ps1",
    ):
        if not (ROOT / path).is_file():
            raise RuntimeError("Required existing recovery script is absent: " + path)
    return {
        "local_head": local_head,
        "remote_head": remote_head,
        "source_guard": "PASS",
        "staged_r43_paths": len(staged),
        "staged_other_paths": 0,
        "unstaged_tracked_paths": len(modified),
        "index_state": status,
        "production_files_modified_by_r43r3": 0,
        "full_pytest": False,
    }


def recover(*, dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    if not dry_run and state["index_state"] == "EXACT_R43_NEW_FILES_STAGED":
        subprocess.run(
            ("git", "restore", "--staged", "--", *PATHS),
            cwd=ROOT, check=True, capture_output=True,
        )
        checked = verify_checkout()
        if checked["index_state"] != "ALREADY_UNSTAGED":
            raise RuntimeError("R43 staged additions were not safely unstaged")
        state = checked
    state["mode"] = "DRYRUN" if dry_run else "RECOVERED"
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = recover(dry_run=args.dry_run)
    prefix = "PHASE174_R3R7R43R3_"
    for name, value in state.items():
        print(prefix + name.upper() + "=" + str(value))
    print(prefix + "GATE=PASS_R43R3_EXACT_INDEX_ONLY_RECOVERY")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
