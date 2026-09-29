from pathlib import Path

MULTI = Path(
  "toda_group_proof_narrative_argument_multi_renderer.py"
)
BODY = Path(
  "toda_group_proof_narrative_argument_body_renderer.py"
)

multi_text = MULTI.read_text(
  encoding="utf-8",
)
body_text = BODY.read_text(
  encoding="utf-8",
)

# ------------------------------------------------------------
# 1. Import TodaGroupProofNarrativeTransitionRole.
# ------------------------------------------------------------

if "TodaGroupProofNarrativeTransitionRole" not in multi_text:
  old_import = """from toda_group_proof_narrative_transitions import (
  extract_toda_group_proof_narrative_transitions,
)
"""
  new_import = """from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)
"""

  if multi_text.count(old_import) != 1:
    raise RuntimeError(
      "Expected exactly one narrative transitions import block"
    )

  multi_text = multi_text.replace(
    old_import,
    new_import,
    1,
  )

# ------------------------------------------------------------
# 2. Add preserve_provenance_block_ids to the body renderer.
# ------------------------------------------------------------

old_body_signature = """  connector_before_block_id: int | None = None,
  connector_text: str | None = None,
  conclusion_step: ProofStep | None = None,
) -> str:
"""
new_body_signature = """  connector_before_block_id: int | None = None,
  connector_text: str | None = None,
  conclusion_step: ProofStep | None = None,
  preserve_provenance_block_ids: (
    frozenset[int]
    | None
  ) = None,
) -> str:
"""

if body_text.count(old_body_signature) != 1:
  raise RuntimeError(
    "Expected exactly one current body renderer signature"
  )

body_text = body_text.replace(
  old_body_signature,
  new_body_signature,
  1,
)

# Validate/default the new optional argument immediately before
# the existing conclusion_step validation/handling when possible.
anchor_candidates = (
  """  if (
    conclusion_step is not None
""",
  """  if conclusion_step is not None:
""",
)

anchor = next(
  (
    candidate
    for candidate in anchor_candidates
    if candidate in body_text
  ),
  None,
)

validation = """  if (
    preserve_provenance_block_ids is not None
    and not isinstance(
      preserve_provenance_block_ids,
      frozenset,
    )
  ):
    raise TypeError(
      "preserve_provenance_block_ids must be "
      "a frozenset or None"
    )

  if preserve_provenance_block_ids is None:
    preserve_provenance_block_ids = frozenset()

  for block_id in preserve_provenance_block_ids:
    if (
      not isinstance(
        block_id,
        int,
      )
      or isinstance(
        block_id,
        bool,
      )
    ):
      raise TypeError(
        "preserve_provenance_block_ids must "
        "contain only integers"
      )

"""

if anchor is not None:
  body_text = body_text.replace(
    anchor,
    validation + anchor,
    1,
  )
else:
  loop_anchor = """  lines = []

  connector_inserted = False
"""
  if body_text.count(loop_anchor) != 1:
    raise RuntimeError(
      "Could not find body renderer validation insertion anchor"
    )
  body_text = body_text.replace(
    loop_anchor,
    validation + loop_anchor,
    1,
  )

old_generic_call = """          show_dependency_labels=False,
          suppress_provenance_only=True,
          preserve_provenance_step_ids=(
            derivation_source_step_ids
          ),
"""
new_generic_call = """          show_dependency_labels=False,
          suppress_provenance_only=(
            id(
              block
            ) not in preserve_provenance_block_ids
          ),
          preserve_provenance_step_ids=(
            derivation_source_step_ids
          ),
"""

if body_text.count(old_generic_call) != 1:
  raise RuntimeError(
    "Expected exactly one R10 generic renderer call"
  )

body_text = body_text.replace(
  old_generic_call,
  new_generic_call,
  1,
)

# ------------------------------------------------------------
# 3. Multi-argument renderer: derive block IDs only from an
#    argument-level DERIVATION transition and pass them to body.
# ------------------------------------------------------------

old_connector = """    connector = (
      None
      if transition is None
      else render_toda_group_proof_narrative_transition_connector(
        transition
      )
    )

    body = (
"""
new_connector = """    connector = (
      None
      if transition is None
      else render_toda_group_proof_narrative_transition_connector(
        transition
      )
    )
    derivation_source_block_ids = (
      frozenset()
      if (
        transition is None
        or transition.role
        is not TodaGroupProofNarrativeTransitionRole.DERIVATION
      )
      else frozenset(
        id(
          source_block
        )
        for source_block in transition.source_blocks
      )
    )

    body = (
"""

if multi_text.count(old_connector) != 1:
  raise RuntimeError(
    "Expected exactly one transition connector/body anchor"
  )

multi_text = multi_text.replace(
  old_connector,
  new_connector,
  1,
)

old_body_call_tail = """        connector_text=connector,
      )
"""
new_body_call_tail = """        connector_text=connector,
        preserve_provenance_block_ids=(
          derivation_source_block_ids
        ),
      )
"""

if multi_text.count(old_body_call_tail) != 1:
  raise RuntimeError(
    "Expected exactly one body renderer call tail"
  )

multi_text = multi_text.replace(
  old_body_call_tail,
  new_body_call_tail,
  1,
)

MULTI.write_text(
  multi_text,
  encoding="utf-8",
)
BODY.write_text(
  body_text,
  encoding="utf-8",
)

print(
  "Phase 143-75AP R11 argument-level DERIVATION "
  "source preservation patch applied."
)
