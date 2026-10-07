from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = PACKAGE_DIR.parent
SOURCE_DIR = PACKAGE_DIR / "files"
BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"


def main() -> None:
  stable_rules = REPOSITORY_ROOT / "stable_rules.py"
  tests_dir = REPOSITORY_ROOT / "tests"

  if not stable_rules.is_file():
    raise SystemExit(
      "stable_rules.py was not found. Extract this package into the repository root."
    )

  if not tests_dir.is_dir():
    raise SystemExit(
      "tests directory was not found. Extract this package into the repository root."
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  backup_stable_rules = (
    BACKUP_DIR / "stable_rules.py"
  )

  if not backup_stable_rules.exists():
    shutil.copy2(
      stable_rules,
      backup_stable_rules,
    )

  shutil.copy2(
    SOURCE_DIR / "stable_rules.py",
    stable_rules,
  )

  shutil.copy2(
    SOURCE_DIR
    / "tests"
    / "test_phase160_stable_target_semantics.py",
    tests_dir
    / "test_phase160_stable_target_semantics.py",
  )

  print("Applied Phase 160-R2 files:")
  print("  stable_rules.py")
  print("  tests/test_phase160_stable_target_semantics.py")


if __name__ == "__main__":
  main()
