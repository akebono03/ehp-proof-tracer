from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(__file__).resolve().parent / "tests"


def copy_test(
  name: str,
) -> None:
  source = SOURCE / name
  destination = ROOT / "tests" / name
  shutil.copyfile(
    source,
    destination,
  )
  print(
    f"updated {destination}"
  )


def main() -> None:
  copy_test(
    "test_phase143_47_multi_argument_shared_contribution_dedup.py"
  )
  copy_test(
    "test_phase143_42_argument_body_contribution_renderer.py"
  )


if __name__ == "__main__":
  main()
