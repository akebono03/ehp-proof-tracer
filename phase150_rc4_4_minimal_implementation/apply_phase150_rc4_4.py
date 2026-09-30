from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
PAYLOAD = Path(__file__).resolve().parent / "payload"


def copy_file(relative_path):
  source = PAYLOAD / relative_path
  destination = ROOT / relative_path
  destination.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copyfile(
    source,
    destination,
  )
  print(
    "Wrote:",
    relative_path,
  )


def main():
  copy_file(
    Path(
      "toda_group_proof_narrative_reasons.py"
    )
  )
  copy_file(
    Path(
      "tests"
    )
    / "test_phase150_rc4_4_reasons.py"
  )
  print(
    "RC4-4 minimal reason infrastructure applied."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
