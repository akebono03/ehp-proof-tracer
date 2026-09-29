from pathlib import Path

ORDERING = Path("toda_group_proof_narrative_contribution_ordering.py")
BODY = Path("toda_group_proof_narrative_argument_body_renderer.py")

R25_15_GROUP_KEY = """def _group_key(
  occurrence: _ContributionOccurrence,
) -> tuple:
  return (
    type(
      occurrence.proof_step.conclusion
    ),
    repr(
      occurrence.proof_step.conclusion
    ),
    occurrence.provider_keys,
  )
"""

CURRENT_GROUP_KEY = """def _group_key(
  occurrence: _ContributionOccurrence,
) -> tuple:
  rendered = _render_generic_narrative_step(
    occurrence.proof_step
  )
  return (
    type(
      occurrence.proof_step.conclusion
    ),
    _normalized(
      rendered
    ),
    occurrence.provider_keys,
  )
"""

ANCHOR = """  step_derivation_sources_by_target_id = (
    _step_derivation_sources_by_target_id(
      presentation,
      blocks,
    )
  )
  derivation_source_step_ids = frozenset(
"""

REPLACEMENT = """  step_derivation_sources_by_target_id = (
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

ordering = ORDERING.read_text(encoding="utf-8-sig")
if R25_15_GROUP_KEY in ordering:
    ORDERING.write_text(
        ordering.replace(
            R25_15_GROUP_KEY,
            CURRENT_GROUP_KEY,
            1,
        ),
        encoding="utf-8",
    )
    print("Rolled back rejected R25-15 _group_key change.")
elif CURRENT_GROUP_KEY in ordering:
    print("Rejected R25-15 _group_key change is already absent.")
else:
    raise SystemExit("Unexpected contribution-ordering _group_key state.")

body = BODY.read_text(encoding="utf-8-sig")
if REPLACEMENT in body:
    print("R25-16 body repair is already present.")
elif ANCHOR in body:
    BODY.write_text(
        body.replace(
            ANCHOR,
            REPLACEMENT,
            1,
        ),
        encoding="utf-8",
    )
    print("Applied depth=2 direct-derivation support mapping repair.")
else:
    raise SystemExit("Expected body-renderer anchor not found.")

print("R25-16 production repair applied.")
