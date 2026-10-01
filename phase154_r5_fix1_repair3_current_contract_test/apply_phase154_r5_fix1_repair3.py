from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase154_r2_fix3_reference_marker_completion.py"
)
SOURCE = (
  Path(__file__).resolve().parent
  / "tests"
  / "test_phase154_r2_fix3_reference_marker_completion.py"
)
BACKUP = (
  REPO_ROOT
  / "phase154_r5_fix1_repair3_current_contract_test"
  / "backup_before_repair3"
  / TARGET.name
)


def main() -> int:
  if not TARGET.exists():
    raise RuntimeError(
      "missing test file: "
      + str(
        TARGET
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
  shutil.copy2(
    SOURCE,
    TARGET,
  )

  print(
    "updated test:",
    TARGET.relative_to(
      REPO_ROOT
    ),
  )
  print(
    "production changes: none"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
