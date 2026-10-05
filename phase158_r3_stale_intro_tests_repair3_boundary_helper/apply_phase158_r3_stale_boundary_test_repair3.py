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
  / "phase158_r3_stale_intro_tests_repair3_backup"
)

OLD_BODY = r'''
def _body(
  rendered: str,
) -> str:
  marker = (
    "次に, $\\nu'$ の位数を決定するために"
  )
  index = rendered.find(
    marker
  )
  assert index >= 0
  return rendered[
    index:
  ]
'''

NEW_BODY = r'''
def _body(
  rendered: str,
) -> str:
  marker = "## 証明"
  index = rendered.find(
    marker
  )
  assert index >= 0

  body = rendered[
    index + len(
      marker
    ):
  ]

  return body.lstrip()
'''

OLD_START_ASSERT = r'''
  assert body.startswith(
    "次に, $\\nu'$ の位数を決定するために"
  )
'''

NEW_START_ASSERT = r'''
  assert body.startswith(
    "まず, $\\nu'$ の位数を決定するために"
  )
'''


def main() -> int:
  source = TARGET.read_text(
    encoding="utf-8",
  )

  if NEW_BODY in source:
    print(
      "Boundary helper already uses the Phase 158 public proof section."
    )
  else:
    if OLD_BODY not in source:
      raise RuntimeError(
        "Expected legacy _body helper was not found."
      )

    source = source.replace(
      OLD_BODY,
      NEW_BODY,
      1,
    )

  legacy_count = source.count(
    OLD_START_ASSERT
  )

  if legacy_count not in (
    0,
    2,
  ):
    raise RuntimeError(
      "Expected zero or two legacy body-start assertions, found "
      + str(
        legacy_count
      )
    )

  if legacy_count == 2:
    source = source.replace(
      OLD_START_ASSERT,
      NEW_START_ASSERT,
      2,
    )

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
    "Phase 158-R3 stale boundary test repair3 applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Changed test helper: _body"
  )
  print(
    "Changed tests: depth2/depth3 boundary assertions"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
