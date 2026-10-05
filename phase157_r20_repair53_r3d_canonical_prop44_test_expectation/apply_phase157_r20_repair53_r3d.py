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
  / "backup_before_repair53_r3d"
  / TARGET.name
)

OLD = (
  '    r"\\\\left(α, \\\\beta\\\\right) \\\\mapsto "\n'
  '    r"Eα + \\\\sigma_{8}\\\\beta"\n'
)

NEW = (
  '    r"(α, \\\\beta) \\\\mapsto "\n'
  '    r"Eα + \\\\sigma_{8}\\\\beta"\n'
)


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

  old_count = source.count(
    OLD
  )
  new_count = source.count(
    NEW
  )

  if old_count == 0 and new_count == 1:
    print(
      "Phase157-R20 repair53-r3d is already applied."
    )
    return 0

  if old_count != 1:
    raise RuntimeError(
      "expected exactly one stale Prop.4.4 assertion, found "
      + str(
        old_count
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

  updated = source.replace(
    OLD,
    NEW,
    1,
  )

  if updated.count(
    NEW
  ) != new_count + 1:
    raise RuntimeError(
      "canonical Prop.4.4 assertion replacement failed"
    )

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
