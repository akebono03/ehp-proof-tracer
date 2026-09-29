from pathlib import Path


TARGET = Path(
  "toda_group_proof_narrative_argument_body_renderer.py"
)

OLD = """  unowned_recursive_exactness_step_ids = frozenset(
    id(
      proof_step
    )
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
      and exactness_exposure_by_block_id is not None
      and exactness_exposure_by_block_id.get(
        id(
          block
        )
      )
      is TodaGroupProofNarrativeExactnessExposureClass
      .UNOWNED_RECURSIVE
    )
    for proof_step in block.steps
  )
"""

NEW = """  suppressed_relocated_exactness_step_ids = frozenset(
    id(
      proof_step
    )
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
      and exactness_exposure_by_block_id is not None
      and exactness_exposure_by_block_id.get(
        id(
          block
        )
      )
      in (
        TodaGroupProofNarrativeExactnessExposureClass
        .OWNED_PRIMARY,
        TodaGroupProofNarrativeExactnessExposureClass
        .UNOWNED_RECURSIVE,
      )
    )
    for proof_step in block.steps
  )
"""

OLD_FILTER = """          and id(
            premise_step
          ) not in unowned_recursive_exactness_step_ids
"""

NEW_FILTER = """          and id(
            premise_step
          ) not in suppressed_relocated_exactness_step_ids
"""


def _extract_function(
  text,
  function_name,
):
  marker = (
    "def "
    + function_name
    + "("
  )
  start = text.index(
    marker
  )
  next_function = text.find(
    "\ndef ",
    start + 1,
  )
  if next_function == -1:
    return text[
      start:
    ].rstrip() + "\n"
  return text[
    start:
    next_function
  ].rstrip() + "\n"


def main():
  text = TARGET.read_text(
    encoding="utf-8"
  )

  if text.count(
    OLD
  ) != 1:
    raise SystemExit(
      "Expected exactly one R1 suppression block; "
      f"found {text.count(OLD)}."
    )

  if text.count(
    OLD_FILTER
  ) != 1:
    raise SystemExit(
      "Expected exactly one R1 relocation filter; "
      f"found {text.count(OLD_FILTER)}."
    )

  updated = text.replace(
    OLD,
    NEW,
    1,
  ).replace(
    OLD_FILTER,
    NEW_FILTER,
    1,
  )

  TARGET.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )

  snapshot = Path(
    "phase148_rc2_4_repair_r2_owned_primary_relocation_suppression"
  ) / "updated_render_toda_group_proof_narrative_argument_body_markdown.py.txt"
  snapshot.write_text(
    _extract_function(
      updated,
      "render_toda_group_proof_narrative_argument_body_markdown",
    ),
    encoding="utf-8",
    newline="\n",
  )

  print("RC2-4 Repair R2 applied.")
  print(
    "Changed only: "
    "render_toda_group_proof_narrative_argument_body_markdown"
  )
  print(
    "OWNED_PRIMARY and UNOWNED_RECURSIVE raw exactness steps "
    "cannot re-enter Narrative through premise/support relocation."
  )
  print(
    "AMBIGUOUS_RELEVANT and unclassified relocation behavior "
    "remain unchanged."
  )
  print(
    "Owned derived short exact sequence contribution remains "
    "handled by the existing exactness contribution renderer."
  )
  print(
    "Full updated function snapshot: "
    + str(
      snapshot
    )
  )


if __name__ == "__main__":
  main()
