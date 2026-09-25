from pathlib import Path
import shutil

source_root = Path(__file__).resolve().parent

copies = (
  (
    source_root
    / "toda_group_proof_narrative_method_evidence.py",
    Path(
      "toda_group_proof_narrative_method_evidence.py"
    ),
  ),
  (
    source_root
    / "tests"
    / "test_phase143_19_method_evidence.py",
    Path(
      "tests"
    )
    / "test_phase143_19_method_evidence.py",
  ),
)

for source, destination in copies:
  if not source.is_file():
    raise FileNotFoundError(
      f"ZIP payload is missing required file: {source}"
    )

  destination.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copyfile(
    source,
    destination,
  )
  print(
    "Updated:",
    destination,
  )
