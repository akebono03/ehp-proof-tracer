from pathlib import Path
from datetime import datetime
import shutil


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"


def main() -> None:
  if not RENDERER.exists():
    raise FileNotFoundError(
      RENDERER
    )

  stamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase159_r1_4_repair2_backup_"
      + stamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )
  shutil.copy2(
    RENDERER,
    backup_dir / RENDERER.name,
  )

  source = RENDERER.read_text(
    encoding="utf-8-sig"
  )

  old_xrightarrow = (
    '    or r"\\\\xrightarrow{" not in stripped\n'
  )
  new_xrightarrow = (
    '    or r"\\xrightarrow{" not in stripped\n'
  )
  old_delta = (
    '    r"\\\\Delta",\n'
  )
  new_delta = (
    '    r"\\Delta",\n'
  )

  xrightarrow_count = source.count(
    old_xrightarrow
  )
  delta_count = source.count(
    old_delta
  )

  if xrightarrow_count != 1:
    raise RuntimeError(
      "expected exactly one escaped xrightarrow matcher, found "
      + str(
        xrightarrow_count
      )
    )

  if delta_count != 1:
    raise RuntimeError(
      "expected exactly one escaped Delta normalizer, found "
      + str(
        delta_count
      )
    )

  source = source.replace(
    old_xrightarrow,
    new_xrightarrow,
    1,
  )
  source = source.replace(
    old_delta,
    new_delta,
    1,
  )

  RENDERER.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-4 repair2 applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Fixed exactness matcher and Delta normalization escaping."
  )


if __name__ == "__main__":
  main()
