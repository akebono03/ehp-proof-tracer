from pathlib import Path
import shutil
from datetime import datetime


ROOT = Path.cwd()
TARGET = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)

OLD_IMPORT = 'from toda_group_proof_generic_narrative_renderer import (\n  _render_generic_narrative_step,\n)\n'
NEW_IMPORT = 'from toda_group_proof_generic_narrative_renderer import (\n  _normalize_generic_eta_family_latex,\n  _render_generic_narrative_step,\n)\n'


def main() -> int:
  if not TARGET.is_file():
    raise RuntimeError(
      "Run this script from the ehp-proof-tracer repository root."
    )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  if (
    "_normalize_generic_eta_family_latex,"
    in source
  ):
    print(
      "Phase157-R20 repair5 is already applied."
    )
    return 0

  if source.count(
    OLD_IMPORT
  ) != 1:
    raise RuntimeError(
      "Expected generic narrative renderer import block "
      "was not found exactly once."
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase157_r20_repair5_backup_"
      + timestamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TARGET,
    backup_dir / TARGET.name,
  )

  updated = source.replace(
    OLD_IMPORT,
    NEW_IMPORT,
    1,
  )

  compile(
    updated,
    str(TARGET),
    "exec",
  )

  TARGET.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R20 repair5 applied.")
  print("Backup:", backup_dir)
  print("Changed:")
  print(" ", TARGET)
  print("")
  print("Architecture preflight:")
  print(
    "  _phase157_r19_:",
    updated.count(
      "_phase157_r19_"
    ),
  )
  print(
    "  is_pi6_3:",
    updated.count(
      "is_pi6_3"
    ),
  )
  print(
    "  pi6 restore:",
    updated.count(
      "_phase157_r3_restore_pi6_3_"
    ),
  )

  if (
    "_phase157_r19_" in updated
    or "is_pi6_3" in updated
    or "_phase157_r3_restore_pi6_3_" in updated
  ):
    raise RuntimeError(
      "Target-specific Narrative code reappeared."
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
