from pathlib import Path
import shutil


DIAGNOSTIC_DIR = (
  "phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2_"
  "worktree_creation_failure_diagnostic_audit"
)
TEST_FILE = (
  "test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2.py"
)


def main():
  repo_root = Path.cwd()
  repair_dir = (
    repo_root
    / (
      "phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2_r1_"
      "diagnostic_audit_test_repair"
    )
  )
  source = repair_dir / "payload" / TEST_FILE
  target = repo_root / DIAGNOSTIC_DIR / TEST_FILE

  if not source.is_file():
    raise SystemExit(
      f"missing repair payload: {source}"
    )

  if not target.is_file():
    raise SystemExit(
      f"missing diagnostic audit test: {target}"
    )

  shutil.copy2(
    source,
    target,
  )

  print(
    "R25-11-R6-R1-R2-R1-R2-R2-R2-R1 "
    "diagnostic audit test repair applied."
  )
  print(
    "Changed audit-only test files: 1."
  )
  print(
    "Diagnostic PowerShell changes: none."
  )
  print(
    "Historical locator changes: none."
  )
  print(
    "Production changes: none."
  )
  print(
    "Existing project tests changed: none."
  )
  print(
    "Population cache changes: none."
  )


if __name__ == "__main__":
  main()
