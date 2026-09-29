from pathlib import Path
import runpy
import shutil


HERE = Path(__file__).resolve().parent
TARGET_DIR_NAME = (
  "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
)


def main():
  runpy.run_path(
    str(
      HERE
      / "apply_r25_11_r6_r1_r2_r1_r2.py"
    ),
    run_name="__main__",
  )

  repo_root = Path.cwd()
  target_dir = repo_root / TARGET_DIR_NAME

  shutil.copy2(
    HERE
    / "payload"
    / "test_phase144_6_r25_11_r6_r1_r2_r1_r2.py",
    target_dir
    / "test_phase144_6_r25_11_r6_r1_r2_r1_r2.py",
  )

  print(
    "R2-R1-R2 focused audit test installed."
  )


if __name__ == "__main__":
  main()
