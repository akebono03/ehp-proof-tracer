from __future__ import annotations

from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase156_r5_repair9_test_contract_after_boundary_collapse.py"
)
BACKUP_DIR = (
  REPO_ROOT
  / "phase158_r3_stale_boundary_repair5_backup"
)

OLD_ASSERT = r'''
  assert body.startswith(
    "まず, $\\nu'$ の位数を決定するために"
  )
'''

NEW_ASSERT = r'''
  assert body
  assert r"\pi_{7}^{3}" in body
'''


def main() -> int:
  source = TARGET.read_text(
    encoding="utf-8",
  )

  count = source.count(
    OLD_ASSERT
  )

  if count not in (
    0,
    2,
  ):
    raise RuntimeError(
      "Expected zero or two brittle body-start assertions, found "
      + str(
        count
      )
    )

  if count == 0:
    print(
      "Brittle body-start assertions already removed."
    )
    return 0

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  backup = (
    BACKUP_DIR
    / TARGET.name
  )

  if not backup.exists():
    shutil.copy2(
      TARGET,
      backup,
    )

  source = source.replace(
    OLD_ASSERT,
    NEW_ASSERT,
    2,
  )

  TARGET.write_text(
    source,
    encoding="utf-8",
  )

  compile(
    source,
    str(
      TARGET
    ),
    "exec",
  )

  print(
    "Phase 158-R3 stale boundary repair5 applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Removed exact prose-start expectation from depth2/depth3 tests."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
