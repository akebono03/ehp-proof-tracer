from pathlib import Path
import shutil


TARGET_DIR_NAME = (
  "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
)
REPAIR_DIR_NAME = (
  "phase144_6_r25_11_r6_r1_r2_windows_worktree_cache_robustness_repair"
)


def main():
  repo_root = Path.cwd()
  target_dir = (
    repo_root
    / TARGET_DIR_NAME
  )
  repair_dir = (
    repo_root
    / REPAIR_DIR_NAME
  )

  if not target_dir.is_dir():
    raise SystemExit(
      f"missing target audit directory: {target_dir}"
    )

  shutil.copy2(
    repair_dir
    / "payload"
    / "locate_historical_190.ps1",
    target_dir
    / "locate_historical_190.ps1",
  )

  shutil.copy2(
    repair_dir
    / "payload"
    / "test_phase144_6_r25_11_r6_r1_r2.py",
    target_dir
    / "test_phase144_6_r25_11_r6_r1_r2.py",
  )

  print(
    "R25-11-R6-R1-R2 Windows worktree/cache robustness repair applied."
  )
  print(
    "Production changes: none."
  )
  print(
    "Existing project tests changed: none."
  )
  print(
    "Historical expected population remains 190."
  )
  print(
    "Existing population cache is preserved."
  )


if __name__ == "__main__":
  main()
