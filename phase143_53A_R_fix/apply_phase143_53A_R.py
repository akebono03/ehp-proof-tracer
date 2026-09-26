from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(__file__).resolve().parent


def copy_file(
  source_relative: str,
  destination_relative: str,
) -> None:
  source = SOURCE / source_relative
  destination = ROOT / destination_relative

  destination.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copyfile(
    source,
    destination,
  )
  print(
    f"updated {destination}"
  )


def main() -> None:
  copy_file(
    "toda_group_proof_narrative_transitions.py",
    "toda_group_proof_narrative_transitions.py",
  )
  copy_file(
    "tests/test_phase143_53a_r_aggregate_derivation.py",
    "tests/test_phase143_53a_r_aggregate_derivation.py",
  )


if __name__ == "__main__":
  main()
