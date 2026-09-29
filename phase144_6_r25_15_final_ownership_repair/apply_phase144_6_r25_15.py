from pathlib import Path

MULTI = Path("toda_group_proof_narrative_argument_multi_renderer.py")
ORDERING = Path("toda_group_proof_narrative_contribution_ordering.py")

R25_13 = """    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    ):
      local_body_block_ids = {
        id(
          block
        )
        for block in local_body_blocks
      }
      evidence_block_ids = {
        id(
          block
        )
        for block in evidence
      }
      local_body_blocks = tuple(
        block
        for block in blocks
        if (
          id(
            block
          ) in local_body_block_ids
          or id(
            block
          ) in evidence_block_ids
        )
      )
"""

PRE_R25_13 = """    local_body_block_ids = {
      id(
        block
      )
      for block in local_body_blocks
    }
    evidence_block_ids = {
      id(
        block
      )
      for block in evidence
    }
    local_body_blocks = tuple(
      block
      for block in blocks
      if (
        id(
          block
        ) in local_body_block_ids
        or id(
          block
        ) in evidence_block_ids
      )
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

SEMANTIC_GROUP_KEY = """def _group_key(
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

multi = MULTI.read_text(encoding="utf-8-sig")
if R25_13 in multi:
    multi = multi.replace(R25_13, PRE_R25_13, 1)
    MULTI.write_text(multi, encoding="utf-8")
    print("Rolled back rejected R25-13.")
elif PRE_R25_13 in multi:
    print("R25-13 already absent.")
else:
    raise SystemExit("Unexpected multi-renderer state; no further changes applied.")

ordering = ORDERING.read_text(encoding="utf-8-sig")
if CURRENT_GROUP_KEY not in ordering:
    if SEMANTIC_GROUP_KEY in ordering:
        print("_group_key already uses semantic statement identity.")
    else:
        raise SystemExit("Unexpected _group_key state; no ordering change applied.")
else:
    ORDERING.write_text(
        ordering.replace(
            CURRENT_GROUP_KEY,
            SEMANTIC_GROUP_KEY,
            1,
        ),
        encoding="utf-8",
    )
    print("Restored semantic statement identity in _group_key.")

print("R25-15 production repair applied.")
