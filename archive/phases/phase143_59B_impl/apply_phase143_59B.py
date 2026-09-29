from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = Path(__file__).resolve().parent


def _replace_once(
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


def _update_body_renderer() -> None:
  path = (
    ROOT
    / "toda_group_proof_narrative_argument_body_renderer.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  old_import = '''from toda_group_proof_narrative_exactness_display_contributions import (
  TodaGroupProofNarrativeExactnessDisplayContributionKind,
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_group_proof_narrative_step_transitions import (
'''
  new_import = '''from toda_group_proof_narrative_exactness_display_contributions import (
  TodaGroupProofNarrativeExactnessDisplayContributionKind,
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_group_proof_narrative_group_structure_semantics import (
  extract_toda_group_structure_narrative_redundant_direct_premise_step_ids,
)
from toda_group_proof_narrative_step_transitions import (
'''
  text = _replace_once(
    text,
    old_import,
    new_import,
    "body renderer import",
  )

  marker = '''  lines = []
  connector_inserted = False

  for block in local_body_blocks:
'''
  replacement = '''  redundant_direct_premise_step_ids = (
    frozenset()
    if conclusion_step is None
    else (
      extract_toda_group_structure_narrative_redundant_direct_premise_step_ids(
        conclusion_step
      )
    )
  )

  lines = []
  connector_inserted = False

  for block in local_body_blocks:
'''
  text = _replace_once(
    text,
    marker,
    replacement,
    "redundant premise derivation",
  )

  old_reordered = '''      reordered_block = (
        _reorder_toda_group_proof_narrative_calculation_derivations(
          block,
          step_derivation_sources_by_target_id,
        )
      )

      if (
'''
  new_reordered = '''      display_steps = tuple(
        proof_step
        for proof_step in block.steps
        if id(
          proof_step
        ) not in redundant_direct_premise_step_ids
      )

      if not display_steps:
        continue

      display_block = block

      if display_steps != block.steps:
        display_block = (
          TodaGroupProofNarrativeBlock(
            role=block.role,
            steps=display_steps,
          )
        )

      reordered_block = (
        _reorder_toda_group_proof_narrative_calculation_derivations(
          display_block,
          step_derivation_sources_by_target_id,
        )
      )

      if (
'''
  text = _replace_once(
    text,
    old_reordered,
    new_reordered,
    "step suppression",
  )

  path.write_text(
    text,
    encoding="utf-8",
  )
  print(
    f"updated {path}"
  )


def main() -> None:
  destination = (
    ROOT
    / "toda_group_proof_narrative_group_structure_semantics.py"
  )
  shutil.copyfile(
    SOURCE_ROOT
    / "toda_group_proof_narrative_group_structure_semantics.py",
    destination,
  )
  print(
    f"updated {destination}"
  )

  _update_body_renderer()

  destination = (
    ROOT
    / "tests"
    / "test_phase143_59b_group_structure_duplicate_suppression.py"
  )
  shutil.copyfile(
    SOURCE_ROOT
    / "tests"
    / "test_phase143_59b_group_structure_duplicate_suppression.py",
    destination,
  )
  print(
    f"updated {destination}"
  )


if __name__ == "__main__":
  main()
