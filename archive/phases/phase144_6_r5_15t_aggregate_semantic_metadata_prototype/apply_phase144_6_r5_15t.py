from pathlib import Path
import shutil

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path.cwd()

FILES = (
  "toda_group_proof_narrative_aggregate_semantics.py",
  "tests/test_phase144_6_r5_15t_aggregate_semantics.py",
)

for relative_path in FILES:
  source = PACKAGE_DIR / relative_path
  destination = REPO_ROOT / relative_path

  if destination.exists():
    raise RuntimeError(
      f"refusing to overwrite existing file: {relative_path}"
    )

  destination.parent.mkdir(parents=True, exist_ok=True)
  shutil.copy2(source, destination)

print("Applied Phase 144-6-R5-15T prototype files.")
