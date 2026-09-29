from pathlib import Path

ROOT = Path.cwd()
multi_path = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
multi = multi_path.read_text(encoding="utf-8-sig")

old_protection = """  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
  ):
    for proof_step in direct_premise_steps:
      protected_step_ids.update(
        id(
          premise_step
        )
        for premise_step in proof_step.premises
      )
"""

new_protection = """  for proof_step in direct_premise_steps:
    protected_step_ids.update(
      id(
        premise_step
      )
      for premise_step in proof_step.premises
    )
"""

if old_protection not in multi:
    raise RuntimeError(
        "frontier prerequisite-protection anchor not found; "
        "local production file is not the expected R12 state"
    )
multi = multi.replace(old_protection, new_protection, 1)

old_seen = """    for block in local_body_blocks:
      if (
        block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        visible_step_ids = {
          id(
            proof_step
          )
          for proof_step in block.steps
          if id(
            proof_step
          ) not in context_hidden_step_ids
        }
        seen_non_exact_step_ids.update(
          visible_step_ids
        )

        if (
          len(
            visible_step_ids
          )
          == len(
            block.steps
          )
        ):
          seen_non_exact_block_ids.add(
            id(
              block
            )
          )
        continue
"""

new_seen = """    for block in local_body_blocks:
      if (
        block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        if (
          block.role
          is TodaGroupProofNarrativeMathematicalBlockRole
          .CALCULATION
        ):
          continue

        visible_step_ids = {
          id(
            proof_step
          )
          for proof_step in block.steps
          if id(
            proof_step
          ) not in context_hidden_step_ids
        }
        seen_non_exact_step_ids.update(
          visible_step_ids
        )

        if (
          len(
            visible_step_ids
          )
          == len(
            block.steps
          )
        ):
          seen_non_exact_block_ids.add(
            id(
              block
            )
          )
        continue
"""

if old_seen not in multi:
    raise RuntimeError(
        "R12 non-exact ownership anchor not found; "
        "apply R12 before R15"
    )
multi = multi.replace(old_seen, new_seen, 1)

multi_path.write_text(multi, encoding="utf-8")
print("Updated:", multi_path)
print("Phase 144-6 R15 production repair applied.")
