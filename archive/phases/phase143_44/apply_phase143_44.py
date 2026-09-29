from pathlib import Path
import shutil

source_root = Path(__file__).resolve().parent

copies = (
  (
    source_root
    / "toda_group_proof_narrative_argument_single_renderer.py",
    Path(
      "toda_group_proof_narrative_argument_single_renderer.py"
    ),
  ),
  (
    source_root
    / "tests"
    / "test_phase143_44_single_argument_narrative_renderer.py",
    Path(
      "tests"
    )
    / "test_phase143_44_single_argument_narrative_renderer.py",
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
