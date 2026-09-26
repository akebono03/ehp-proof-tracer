from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = Path(__file__).resolve().parent


def main() -> None:
  files = (
    (
      SOURCE_ROOT
      / "toda_group_proof_narrative_argument_direct_premises.py",
      ROOT
      / "toda_group_proof_narrative_argument_direct_premises.py",
    ),
    (
      SOURCE_ROOT
      / "tests"
      / "test_phase143_61a_argument_conclusion_direct_premises.py",
      ROOT
      / "tests"
      / "test_phase143_61a_argument_conclusion_direct_premises.py",
    ),
  )

  for source, destination in files:
    shutil.copyfile(
      source,
      destination,
    )
    print(
      f"updated {destination}"
    )


if __name__ == "__main__":
  main()
