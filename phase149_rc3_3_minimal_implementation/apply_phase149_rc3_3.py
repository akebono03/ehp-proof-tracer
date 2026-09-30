from pathlib import Path

TARGET = Path("toda_group_proof_narrative_argument_body_renderer.py")

OLD_INIT = """  lines = []
  connector_inserted = False

  for block in local_body_blocks:
"""

NEW_INIT = """  lines = []
  connector_inserted = False
  deferred_owned_primary_exactness_lines = []

  for block in local_body_blocks:
"""

OLD_EXACTNESS = """    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    ):
      block_lines = (
        _render_toda_group_proof_narrative_argument_exactness_body_block(
          presentation,
          blocks,
          block_index,
          primary_component,
          (
            None
            if exactness_exposure_by_block_id is None
            else exactness_exposure_by_block_id.get(id(block))
          ),
          excluded_exactness_contribution_keys,
        )
      )
    else:
"""

NEW_EXACTNESS = """    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    ):
      exposure_class = (
        None
        if exactness_exposure_by_block_id is None
        else exactness_exposure_by_block_id.get(id(block))
      )
      block_lines = (
        _render_toda_group_proof_narrative_argument_exactness_body_block(
          presentation,
          blocks,
          block_index,
          primary_component,
          exposure_class,
          excluded_exactness_contribution_keys,
        )
      )

      if (
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

OLD_BEFORE_CONNECTOR = """    if not block_lines:
      continue

    if (
      not connector_inserted
"""

NEW_BEFORE_CONNECTOR = """    if not block_lines:
      continue

    if (
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

OLD_RETURN = """    lines.extend(
      block_lines
    )

  return "\\n".join(
    lines
  ).rstrip()
"""

NEW_RETURN = """    lines.extend(
      block_lines
    )

  if deferred_owned_primary_exactness_lines:
    lines.extend(
      deferred_owned_primary_exactness_lines
    )

  return "\\n".join(
    lines
  ).rstrip()
"""

def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"{label}: expected exactly one match, found {count}"
        )
    return text.replace(old, new, 1)

def main():
    text = TARGET.read_text(encoding="utf-8")
    text = replace_once(text, OLD_INIT, NEW_INIT, "init")
    text = replace_once(text, OLD_EXACTNESS, NEW_EXACTNESS, "exactness")
    text = replace_once(
        text,
        OLD_BEFORE_CONNECTOR,
        NEW_BEFORE_CONNECTOR,
        "before connector",
    )
    text = replace_once(text, OLD_RETURN, NEW_RETURN, "return")
    TARGET.write_text(text, encoding="utf-8")
    print("Phase 149 RC3-3 minimal implementation applied.")
    print("Changed:")
    print("  toda_group_proof_narrative_argument_body_renderer.py")
    print("Added:")
    print("  tests/test_phase149_rc3_3_minimal_ordering.py")

if __name__ == "__main__":
    main()
