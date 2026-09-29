from pathlib import Path
import shutil


PHASE_DIR_NAME = (
  "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
)
REPAIR_DIR_NAME = (
  "phase144_6_r25_11_r6_r1_r1_runner_repair"
)


def main():
  repo_root = Path.cwd()
  repair_dir = (
    repo_root
    / REPAIR_DIR_NAME
  )
  target_dir = (
    repo_root
    / PHASE_DIR_NAME
  )

  if not target_dir.is_dir():
    raise SystemExit(
      f"missing target audit directory: {target_dir}"
    )

  replacements = (
    "locate_historical_190.ps1",
    "run_phase144_6_r25_11_r6_r1.ps1",
  )

  for name in replacements:
    shutil.copy2(
      repair_dir
      / "payload"
      / name,
      target_dir
      / name,
    )

  shutil.copy2(
    repair_dir
    / "payload"
    / "test_phase144_6_r25_11_r6_r1_r1.py",
    target_dir
    / "test_phase144_6_r25_11_r6_r1_r1.py",
  )

  print(
    "R25-11-R6-R1-R1 runner repair applied."
  )
  print(
    "Production changes: none."
  )
  print(
    "Existing project tests changed: none."
  )
  print(
    "Repaired audit runner only."
  )


if __name__ == "__main__":
  main()
