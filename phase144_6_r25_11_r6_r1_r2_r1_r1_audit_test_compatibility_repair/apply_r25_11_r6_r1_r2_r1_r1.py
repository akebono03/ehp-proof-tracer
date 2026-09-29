from pathlib import Path
import shutil


TARGET_DIR_NAME = (
  "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
)
REPAIR_DIR_NAME = (
  "phase144_6_r25_11_r6_r1_r2_r1_r1_audit_test_compatibility_repair"
)


def main():
  repo_root = Path.cwd()
  target_dir = repo_root / TARGET_DIR_NAME
  repair_dir = repo_root / REPAIR_DIR_NAME

  if not target_dir.is_dir():
    raise SystemExit(
      f"missing target audit directory: {target_dir}"
    )

  source = (
    repair_dir
    / "payload"
    / "test_phase144_6_r25_11_r6_r1_r1.py"
  )
  destination = (
    target_dir
    / "test_phase144_6_r25_11_r6_r1_r1.py"
  )

  shutil.copy2(
    source,
    destination,
  )

  print(
    "R25-11-R6-R1-R2-R1-R1 audit test compatibility repair applied."
  )
  print(
    "Changed only audit test: test_phase144_6_r25_11_r6_r1_r1.py"
  )
  print(
    "Production changes: none."
  )
  print(
    "Locator changes: none."
  )
  print(
    "Existing project tests changed: none."
  )
  print(
    "Expected historical population remains 190."
  )


if __name__ == "__main__":
  main()
