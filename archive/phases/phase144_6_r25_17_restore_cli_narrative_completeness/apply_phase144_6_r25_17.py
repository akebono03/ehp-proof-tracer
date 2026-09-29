from pathlib import Path

BODY = Path("toda_group_proof_narrative_argument_body_renderer.py")
MAIN = Path("main.py")

R25_16 = """  step_derivation_sources_by_target_id = (
    _step_derivation_sources_by_target_id(
      presentation,
      blocks,
    )
  )

  direct_derivation_support_step_ids = {
    id(
      support_step
    )
    for support_step in direct_derivation_support_steps
  }

  for premise_step in direct_derivation_premises:
    support_steps = tuple(
      support_step
      for support_step in premise_step.premises
      if id(
        support_step
      ) in direct_derivation_support_step_ids
    )

    if not support_steps:
      continue

    target_id = id(
      premise_step
    )
    existing = (
      step_derivation_sources_by_target_id.get(
        target_id,
        (),
      )
    )

    step_derivation_sources_by_target_id[
      target_id
    ] = (
      *existing,
      *tuple(
        support_step
        for support_step in support_steps
        if all(
          support_step is not existing_step
          for existing_step in existing
        )
      ),
    )

  derivation_source_step_ids = frozenset(
"""

PRE_R25_16 = """  step_derivation_sources_by_target_id = (
    _step_derivation_sources_by_target_id(
      presentation,
      blocks,
    )
  )
  derivation_source_step_ids = frozenset(
"""

PRE_R24 = """  else:
    presentation = (
      build_toda_group_proof_presentation(
        replay
      )
    )

    if mode == "outline":
"""

R24 = """  else:
    if (
      mode == "narrative"
      and max_depth is not None
    ):
      narrative_replay = (
        build_toda_group_result_proof_replay(
          group_result
        )
      )
      presentation = (
        build_toda_group_proof_presentation(
          narrative_replay
        )
      )
    else:
      presentation = (
        build_toda_group_proof_presentation(
          replay
        )
      )

    if mode == "outline":
"""

body = BODY.read_text(encoding="utf-8-sig")
if R25_16 in body:
    BODY.write_text(
        body.replace(
            R25_16,
            PRE_R25_16,
            1,
        ),
        encoding="utf-8",
    )
    print("Rolled back rejected R25-16 body-renderer change.")
elif PRE_R25_16 in body:
    print("Rejected R25-16 body-renderer change is already absent.")
else:
    raise SystemExit("Unexpected body-renderer state.")

main = MAIN.read_text(encoding="utf-8-sig")
if R24 in main:
    print("R24 CLI Narrative completeness behavior is already present.")
elif PRE_R24 in main:
    MAIN.write_text(
        main.replace(
            PRE_R24,
            R24,
            1,
        ),
        encoding="utf-8",
    )
    print("Restored R24 CLI Narrative completeness behavior.")
else:
    raise SystemExit("Unexpected main.py group-proof branch state.")

print("R25-17 production repair applied.")
