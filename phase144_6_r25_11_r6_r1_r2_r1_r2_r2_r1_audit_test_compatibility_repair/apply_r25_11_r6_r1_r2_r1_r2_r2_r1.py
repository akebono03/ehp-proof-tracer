from pathlib import Path
import shutil


TARGET_DIR_NAME = (
  "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
)


def main():
  repo_root = Path.cwd()
  repair_dir = (
    repo_root
    / "phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r1_audit_test_compatibility_repair"
  )
  payload = repair_dir / "payload"
  target_dir = repo_root / TARGET_DIR_NAME

  replacements = (
    "test_phase144_6_r25_11_r6_r1_r2_r1_r2.py",
    "test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1.py",
  )

  for filename in replacements:
    source = payload / filename
    target = target_dir / filename

    if not source.is_file():
      raise SystemExit(
        f"missing repair payload: {source}"
      )

    if not target.is_file():
      raise SystemExit(
        f"missing existing audit test: {target}"
      )

    shutil.copy2(
      source,
      target,
    )

  print(
    "R25-11-R6-R1-R2-R1-R2-R2-R1 "
    "audit test compatibility repair applied."
  )
  print(
    "Changed audit-only tests: 2."
  )
  print(
    "Locator changes: none."
  )
  print(
    "Production changes: none."
  )
  print(
    "Existing project tests changed: none."
  )
  print(
    "Expected historical population remains 190."
  )
  print(
    "Existing population cache is preserved."
  )


if __name__ == "__main__":
  main()
