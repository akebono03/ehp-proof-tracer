from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(__file__).resolve().parent
GENERIC = ROOT / "toda_group_proof_generic_narrative_renderer.py"


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, found {count}"
    )

  return text.replace(
    old,
    new,
    1,
  )


def install_aggregate_renderer() -> None:
  source = SOURCE / "toda_group_proof_aggregate_statement_renderer.py"
  destination = ROOT / "toda_group_proof_aggregate_statement_renderer.py"
  shutil.copyfile(source, destination)
  print(f"updated {destination}")


def patch_generic_renderer() -> None:
  text = GENERIC.read_text(encoding="utf-8")

  anchor = '''from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
'''
  replacement = '''from toda_group_proof_aggregate_statement_renderer import (
  render_toda_group_proof_aggregate_statement_prose,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
'''
  text = replace_once(
    text,
    anchor,
    replacement,
    "aggregate renderer import",
  )

  old_start = '''def _render_generic_narrative_statement_prose(
  statement,
) -> str | None:
  if isinstance(
'''
  new_start = '''def _render_generic_narrative_statement_prose(
  statement,
) -> str | None:
  aggregate_prose = (
    render_toda_group_proof_aggregate_statement_prose(
      statement
    )
  )

  if aggregate_prose is not None:
    return aggregate_prose

  if isinstance(
'''
  text = replace_once(
    text,
    old_start,
    new_start,
    "statement prose aggregate dispatch",
  )

  GENERIC.write_text(text, encoding="utf-8")
  print(f"updated {GENERIC}")


def install_test() -> None:
  source = SOURCE / "tests" / "test_phase143_51b_aggregate_statement_prose.py"
  destination = ROOT / "tests" / "test_phase143_51b_aggregate_statement_prose.py"
  shutil.copyfile(source, destination)
  print(f"updated {destination}")


def main() -> None:
  install_aggregate_renderer()
  patch_generic_renderer()
  install_test()


if __name__ == "__main__":
  main()
