from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(__file__).resolve().parent


def update_arguments_file() -> None:
  path = ROOT / "toda_group_proof_narrative_arguments.py"
  text = path.read_text(
    encoding="utf-8",
  )

  old_import = """from proof import (
  Relation,
  RelationType,
)
"""
  new_import = """from proof import (
  ProofStep,
  Relation,
  RelationType,
)
"""

  if old_import in text:
    text = text.replace(
      old_import,
      new_import,
      1,
    )
  elif new_import not in text:
    raise RuntimeError(
      "expected proof import block was not found"
    )

  marker = """def build_toda_group_proof_narrative_arguments(
"""
  extractor = SOURCE.joinpath(
    "argument_conclusion_step_extractor.txt"
  ).read_text(
    encoding="utf-8",
  )

  if extractor in text:
    pass
  elif marker in text:
    text = text.replace(
      marker,
      extractor + marker,
      1,
    )
  else:
    raise RuntimeError(
      "build_toda_group_proof_narrative_arguments "
      "marker was not found"
    )

  path.write_text(
    text,
    encoding="utf-8",
  )
  print(
    f"updated {path}"
  )


def copy_file(
  source_relative: str,
  destination_relative: str,
) -> None:
  source = SOURCE / source_relative
  destination = ROOT / destination_relative
  destination.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copyfile(
    source,
    destination,
  )
  print(
    f"updated {destination}"
  )


def main() -> None:
  update_arguments_file()
  copy_file(
    "tests/test_phase143_55a_argument_conclusion_step.py",
    "tests/test_phase143_55a_argument_conclusion_step.py",
  )


if __name__ == "__main__":
  main()
