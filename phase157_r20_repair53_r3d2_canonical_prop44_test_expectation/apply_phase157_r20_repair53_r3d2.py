from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase157_r20_repair53_r3_fixed_reference_attribution.py"
)

BACKUP = (
  PACKAGE_DIR
  / "backup_before_repair53_r3d2"
  / TARGET.name
)

OLD_LINE_1 = '    r"\\left(α, \\beta\\right) \\mapsto "'
OLD_LINE_2 = '    r"Eα + \\sigma_{8}\\beta"'

NEW_LINE_1 = '    r"(α, \\beta) \\mapsto "'
NEW_LINE_2 = '    r"Eα + \\sigma_{8}\\beta"'


def main() -> int:
  if not TARGET.exists():
    raise RuntimeError(
      "missing test file: "
      + str(
        TARGET
      )
    )

  source = TARGET.read_text(
    encoding="utf-8",
  )
  lines = source.splitlines()

  old_pair_indexes = tuple(
    index
    for index in range(
      len(
        lines
      )
      - 1
    )
    if (
      lines[index] == OLD_LINE_1
      and lines[index + 1] == OLD_LINE_2
    )
  )

  new_pair_indexes = tuple(
    index
    for index in range(
      len(
        lines
      )
      - 1
    )
    if (
      lines[index] == NEW_LINE_1
      and lines[index + 1] == NEW_LINE_2
    )
  )

  if not old_pair_indexes and len(new_pair_indexes) == 1:
    print(
      "Phase157-R20 repair53-r3d2 is already applied."
    )
    return 0

  if len(
    old_pair_indexes
  ) != 1:
    print(
      "matching stale assertion line 1 count:",
      sum(
        1
        for line in lines
        if line == OLD_LINE_1
      ),
    )
    print(
      "matching stale assertion line 2 count:",
      sum(
        1
        for line in lines
        if line == OLD_LINE_2
      ),
    )
    raise RuntimeError(
      "expected exactly one stale Prop.4.4 assertion pair, found "
      + str(
        len(
          old_pair_indexes
        )
      )
    )

  BACKUP.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    TARGET,
    BACKUP,
  )

  index = old_pair_indexes[
    0
  ]
  lines[
    index
  ] = NEW_LINE_1
  lines[
    index + 1
  ] = NEW_LINE_2

  updated = "\n".join(
    lines
  )

  if source.endswith(
    "\n"
  ):
    updated += "\n"

  TARGET.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "updated test:",
    TARGET.relative_to(
      REPO_ROOT
    ),
  )
  print(
    "backup:",
    BACKUP,
  )
  print(
    "production code changes: none"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
