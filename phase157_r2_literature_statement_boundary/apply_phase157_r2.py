from pathlib import Path
import shutil


PACKAGE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = PACKAGE_ROOT.parent

FILES = (
  (
    PACKAGE_ROOT / "toda_literature_statement_boundary.py",
    REPOSITORY_ROOT / "toda_literature_statement_boundary.py",
  ),
  (
    PACKAGE_ROOT / "tests" / "test_phase157_r2_literature_statement_boundary.py",
    REPOSITORY_ROOT / "tests" / "test_phase157_r2_literature_statement_boundary.py",
  ),
)


def main() -> None:
  for source, destination in FILES:
    destination.parent.mkdir(
      parents=True,
      exist_ok=True,
    )
    shutil.copy2(
      source,
      destination,
    )
    print(
      f"copied: {source.name} -> {destination}"
    )


if __name__ == "__main__":
  main()
