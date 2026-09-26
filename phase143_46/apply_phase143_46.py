from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
PHASE_DIR = Path(__file__).resolve().parent


def copy_file(
  source_name: str,
  destination_name: str,
) -> None:
  source = PHASE_DIR / source_name
  destination = ROOT / destination_name

  destination.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    source,
    destination,
  )
  print(
    f"copied {source} -> {destination}"
  )


def main() -> None:
  copy_file(
    "toda_group_proof_narrative_argument_multi_renderer.py",
    "toda_group_proof_narrative_argument_multi_renderer.py",
  )
  copy_file(
    "tests/test_phase143_46_multi_argument_narrative_assembler.py",
    "tests/test_phase143_46_multi_argument_narrative_assembler.py",
  )


if __name__ == "__main__":
  main()
