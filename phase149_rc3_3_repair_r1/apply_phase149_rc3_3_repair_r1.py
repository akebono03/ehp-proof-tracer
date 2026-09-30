from pathlib import Path

TARGET = Path("toda_group_proof_narrative_argument_body_renderer.py")

OLD_INIT = """  lines = []
  connector_inserted = False
  deferred_owned_primary_exactness_lines = []

  for block in local_body_blocks:
"""

NEW_INIT = """  owned_primary_exactness_lines = []

  for block in local_body_blocks:
    if (
      block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    ):
      continue

    exposure_class = (
      None
      if exactness_exposure_by_block_id is None
      else exactness_exposure_by_block_id.get(
        id(
          block
        )
      )
    )

    if (
      exposure_class
      is not TodaGroupProofNarrativeExactnessExposureClass
      .OWNED_PRIMARY
    ):
      continue

    block_index = block_index_by_identity[
      id(
        block
      )
    ]
    owned_primary_exactness_lines.extend(
      _render_toda_group_proof_narrative_argument_exactness_body_block(
        presentation,
        blocks,
        block_index,
        primary_component,
        exposure_class,
        excluded_exactness_contribution_keys,
      )
    )

  lines = []
  connector_inserted = False
  owned_primary_exactness_inserted = False

  for block in local_body_blocks:
"""

OLD_EXACTNESS = """      if (
        block_lines
        and exposure_class
        is TodaGroupProofNarrativeExactnessExposureClass
        .OWNED_PRIMARY
      ):
        deferred_owned_primary_exactness_lines.extend(
          block_lines
        )
        continue
    else:
"""

NEW_EXACTNESS = """      if (
        exposure_class
        is TodaGroupProofNarrativeExactnessExposureClass
        .OWNED_PRIMARY
      ):
        continue
    else:
"""

OLD_INSERT = """    if (
      deferred_owned_primary_exactness_lines
      and conclusion_step is not None
      and conclusion_step in block.steps
      and block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    ):
      block_lines = (
        tuple(
          deferred_owned_primary_exactness_lines
        )
        + block_lines
      )
      deferred_owned_primary_exactness_lines.clear()

    if (
      not connector_inserted
"""

NEW_INSERT = """    if (
      not owned_primary_exactness_inserted
      and owned_primary_exactness_lines
      and conclusion_step is not None
      and conclusion_step in block.steps
      and block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    ):
      block_lines = (
        tuple(
          owned_primary_exactness_lines
        )
        + block_lines
      )
      owned_primary_exactness_inserted = True

    if (
      not connector_inserted
"""

OLD_RETURN = """  if deferred_owned_primary_exactness_lines:
    lines.extend(
      deferred_owned_primary_exactness_lines
    )

  return "\\n".join(
    lines
  ).rstrip()
"""

NEW_RETURN = """  if (
    owned_primary_exactness_lines
    and not owned_primary_exactness_inserted
  ):
    lines.extend(
      owned_primary_exactness_lines
    )

  return "\\n".join(
    lines
  ).rstrip()
"""

def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"{label}: expected exactly one match, found {count}. "
            "Apply this repair after phase149_rc3_3_minimal_implementation."
        )
    return text.replace(old, new, 1)

def main():
    text = TARGET.read_text(encoding="utf-8")
    text = replace_once(text, OLD_INIT, NEW_INIT, "precollect initialization")
    text = replace_once(text, OLD_EXACTNESS, NEW_EXACTNESS, "exactness skip")
    text = replace_once(text, OLD_INSERT, NEW_INSERT, "conclusion insertion")
    text = replace_once(text, OLD_RETURN, NEW_RETURN, "fallback")
    TARGET.write_text(text, encoding="utf-8")
    print("Phase 149 RC3-3 Repair R1 applied.")
    print("Changed only:")
    print("  toda_group_proof_narrative_argument_body_renderer.py")
    print("Reason:")
    print("  Precollect OWNED_PRIMARY exactness before iterating global-order body blocks.")

if __name__ == "__main__":
    main()
