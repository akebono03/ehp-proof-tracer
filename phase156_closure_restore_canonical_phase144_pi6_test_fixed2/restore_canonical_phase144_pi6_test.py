from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RELATIVE_PATH = (
  "tests/"
  "test_phase144_6_pi6_generic_production_route.py"
)
TARGET = ROOT / RELATIVE_PATH
BACKUP_DIR = (
  ROOT
  / "phase156_closure_test_restore_backup"
)
BACKUP = (
  BACKUP_DIR
  / "test_phase144_6_pi6_generic_production_route.py"
)


def _run_git(
  *args: str,
) -> subprocess.CompletedProcess[str]:
  return subprocess.run(
    (
      "git",
      *args,
    ),
    cwd=ROOT,
    text=True,
    encoding="utf-8",
    errors="strict",
    capture_output=True,
    check=True,
  )


def main() -> int:
  head = _run_git(
    "rev-parse",
    "HEAD",
  ).stdout.strip()

  expected_head = (
    "baab9402c9ca8c5051268d5d334591ea44b5b273"
  )

  print(
    "Current HEAD:",
    head,
  )

  if head != expected_head:
    raise RuntimeError(
      "Expected Phase156-R6 HEAD "
      + expected_head
      + " but found "
      + head
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  if TARGET.exists():
    BACKUP.write_bytes(
      TARGET.read_bytes()
    )

  _run_git(
    "restore",
    "--source=HEAD",
    "--worktree",
    "--",
    RELATIVE_PATH,
  )

  status = _run_git(
    "status",
    "--short",
    "--",
    RELATIVE_PATH,
  ).stdout.strip()

  diff = _run_git(
    "diff",
    "--",
    RELATIVE_PATH,
  ).stdout

  print()
  print(
    "Restored from HEAD:",
    RELATIVE_PATH,
  )
  print(
    "Backup:",
    BACKUP,
  )
  print()
  print(
    "git status --short -- target:"
  )
  print(
    status
    if status
    else "(clean)"
  )
  print()
  print(
    "git diff -- target:"
  )
  print(
    diff
    if diff
    else "(no diff)"
  )

  if status or diff:
    raise RuntimeError(
      "Target test file does not exactly match HEAD "
      "after restore."
    )

  print()
  print(
    "PASS: target test file exactly matches HEAD."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
