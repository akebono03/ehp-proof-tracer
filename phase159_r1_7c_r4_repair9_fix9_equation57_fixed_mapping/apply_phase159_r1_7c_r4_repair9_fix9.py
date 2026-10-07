from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = REPO_ROOT / "toda_literature_statement_boundary.py"
BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"

OLD_SINGLE = (
  "'Toda Equation 5.7 nu-prime eta_6 Hopf value': "
  "'Equation 5.7'"
)
NEW_SINGLE = (
  "'Toda Equation 5.7 nu-prime eta_6 Hopf value': "
  "'(5.7)'"
)

OLD_DOUBLE = (
  '"Toda Equation 5.7 nu-prime eta_6 Hopf value": '
  '"Equation 5.7"'
)
NEW_DOUBLE = (
  '"Toda Equation 5.7 nu-prime eta_6 Hopf value": '
  '"(5.7)"'
)


def main() -> int:
  if not TARGET.is_file():
    raise RuntimeError(
      f"Target file not found: {TARGET}"
    )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  old_count = (
    source.count(
      OLD_SINGLE
    )
    + source.count(
      OLD_DOUBLE
    )
  )

  new_count = (
    source.count(
      NEW_SINGLE
    )
    + source.count(
      NEW_DOUBLE
    )
  )

  print(
    "pre_apply_old_mapping_count=",
    old_count,
    sep="",
  )
  print(
    "pre_apply_new_mapping_count=",
    new_count,
    sep="",
  )

  if old_count == 0:
    if new_count >= 1:
      print(
        "Equation 5.7 fixed-rule mapping is already normalized."
      )
      return 0

    raise RuntimeError(
      "Equation 5.7 fixed-rule mapping was not found."
    )

  if old_count != 1:
    raise RuntimeError(
      "Expected exactly one Equation 5.7 fixed-rule mapping, "
      f"found {old_count}."
    )

  updated = source.replace(
    OLD_SINGLE,
    NEW_SINGLE,
    1,
  )
  updated = updated.replace(
    OLD_DOUBLE,
    NEW_DOUBLE,
    1,
  )

  compile(
    updated,
    str(
      TARGET
    ),
    "exec",
  )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  backup = BACKUP_DIR / TARGET.name

  if not backup.exists():
    shutil.copy2(
      TARGET,
      backup,
    )

  TARGET.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "Updated Equation 5.7 fixed-rule locator:"
  )
  print(
    '  "Equation 5.7" -> "(5.7)"'
  )
  print(
    "No import changes."
  )
  print(
    "No classification change."
  )
  print(
    "No group-specific n/k branch added."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
