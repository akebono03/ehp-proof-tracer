from pathlib import Path
import shutil

source_root = Path(__file__).resolve().parent

copies = (
  (
    source_root
    / "toda_group_proof_narrative_argument_renderer.py",
    Path(
      "toda_group_proof_narrative_argument_renderer.py"
    ),
  ),
  (
    source_root
    / "tests"
    / "test_phase143_13_purpose_sentence.py",
    Path(
      "tests"
    )
    / "test_phase143_13_purpose_sentence.py",
  ),
)

for source, destination in copies:
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
