from pathlib import Path
import ast
import shutil
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)

PRIMARY_BACKUP = (
  REPO_ROOT
  / "phase161_r3_pi4_2_restored_reference_relink"
  / "backup_before_apply"
  / "toda_group_proof_narrative_contribution_renderer.py"
)

OUTPUT_DIR = (
  PACKAGE_DIR
  / "output"
)

REPORT = (
  OUTPUT_DIR
  / "phase161_r3_renderer_recovery.txt"
)


REQUIRED_NAMES = (
  "restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage",
  "filter_toda_group_proof_narrative_reference_entries_by_body_usage",
  "link_toda_group_proof_narrative_unmarked_reference_consumers",
)


def _validate_source(
  path: Path,
) -> tuple[
  bool,
  list[str],
]:
  problems = []

  if not path.exists():
    problems.append(
      "file does not exist"
    )
    return (
      False,
      problems,
    )

  size = path.stat().st_size

  if size <= 0:
    problems.append(
      "file is empty"
    )
    return (
      False,
      problems,
    )

  source = path.read_text(
    encoding="utf-8"
  )

  try:
    ast.parse(
      source
    )
  except SyntaxError as exc:
    problems.append(
      "syntax error: "
      + str(
        exc
      )
    )

  for required_name in REQUIRED_NAMES:
    if required_name not in source:
      problems.append(
        "missing required symbol: "
        + required_name
      )

  return (
    not problems,
    problems,
  )


def main():
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  lines = [
    "=" * 78,
    "Phase 161-R3 renderer recovery",
    "=" * 78,
    f"target: {TARGET}",
    f"primary backup: {PRIMARY_BACKUP}",
    "",
  ]

  target_size = (
    TARGET.stat().st_size
    if TARGET.exists()
    else -1
  )

  lines.append(
    f"target size before recovery: {target_size}"
  )

  backup_ok, backup_problems = (
    _validate_source(
      PRIMARY_BACKUP
    )
  )

  lines.append(
    "primary backup valid: "
    + str(
      backup_ok
    )
  )

  if backup_problems:
    for problem in backup_problems:
      lines.append(
        "  - "
        + problem
      )

  if not backup_ok:
    lines.extend(
      (
        "",
        "RECOVERY ABORTED",
        (
          "The original Phase 161-R3 backup is not usable. "
          "No production file was modified."
        ),
      )
    )

    REPORT.write_text(
      "\n".join(
        lines
      )
      + "\n",
      encoding="utf-8",
      newline="\n",
    )

    print(
      "\n".join(
        lines
      )
    )

    raise RuntimeError(
      "Usable primary backup was not found."
    )

  recovery_backup = (
    OUTPUT_DIR
    / "empty_target_before_recovery.py"
  )

  if TARGET.exists():
    shutil.copy2(
      TARGET,
      recovery_backup,
    )

  shutil.copy2(
    PRIMARY_BACKUP,
    TARGET,
  )

  restored_ok, restored_problems = (
    _validate_source(
      TARGET
    )
  )

  lines.extend(
    (
      "",
      "restored from primary backup",
      (
        "target size after recovery: "
        + str(
          TARGET.stat().st_size
        )
      ),
      (
        "restored target valid: "
        + str(
          restored_ok
        )
      ),
    )
  )

  if restored_problems:
    for problem in restored_problems:
      lines.append(
        "  - "
        + problem
      )

  if not restored_ok:
    raise RuntimeError(
      "Restored target validation failed."
    )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  lines.extend(
    (
      "",
      "required symbols:",
    )
  )

  for required_name in REQUIRED_NAMES:
    lines.append(
      "  "
      + required_name
      + ": "
      + str(
        required_name in source
      )
    )

  lines.extend(
    (
      "",
      "RECOVERY COMPLETE",
      "Phase 161-R3 feature repair has NOT been applied.",
    )
  )

  REPORT.write_text(
    "\n".join(
      lines
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    "\n".join(
      lines
    )
  )


if __name__ == "__main__":
  main()
