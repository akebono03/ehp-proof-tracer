from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
TEST = (
  ROOT
  / "tests"
  / "test_phase159_r1_6c_source_faithful_reference_linkage.py"
)


def main() -> None:
  if not TEST.exists():
    raise FileNotFoundError(
      TEST
    )

  stamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase159_r1_6d_repair1_backup_"
      + stamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TEST,
    backup_dir / TEST.name,
  )

  source = TEST.read_text(
    encoding="utf-8-sig"
  )

  normalized = (
    source.rstrip()
    + "\n"
  )

  TEST.write_text(
    normalized,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-6d repair1 applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Production code changes: none"
  )
  print(
    "Removed extra blank line(s) at EOF from "
    "test_phase159_r1_6c_source_faithful_reference_linkage.py."
  )


if __name__ == "__main__":
  main()
