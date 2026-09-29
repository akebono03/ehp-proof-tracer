from pathlib import Path
import ast

MULTI = Path(
  "toda_group_proof_narrative_argument_multi_renderer.py"
)
BODY = Path(
  "toda_group_proof_narrative_argument_body_renderer.py"
)


def read_python(
  path,
):
  raw = path.read_bytes()
  return (
    raw.decode(
      "utf-8-sig"
    ),
    raw.startswith(
      b"\xef\xbb\xbf"
    ),
  )


def write_python(
  path,
  text,
  had_bom,
):
  ast.parse(
    text
  )
  path.write_text(
    text,
    encoding=(
      "utf-8-sig"
      if had_bom
      else "utf-8"
    ),
  )


multi_text, multi_bom = read_python(
  MULTI
)
body_text, body_bom = read_python(
  BODY
)


# ------------------------------------------------------------
# 1. Current audited import block.
# ------------------------------------------------------------

old_import = """from toda_group_proof_narrative_transitions import (
  extract_toda_group_proof_narrative_transitions,
)
"""
new_import = """from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)
"""

if "TodaGroupProofNarrativeTransitionRole" not in multi_text:
  if multi_text.count(
    old_import
  ) != 1:
    raise RuntimeError(
      "Current audited narrative transitions import "
      "block was not found exactly once"
    )
  multi_text = multi_text.replace(
    old_import,
    new_import,
    1,
  )


# ------------------------------------------------------------
# 2. Current audited body signature tail.
# ------------------------------------------------------------

old_signature_tail = """  context_hidden_step_ids: (
    frozenset[
      int
    ]
    | None
  ) = None,
) -> str:
"""
new_signature_tail = """  context_hidden_step_ids: (
    frozenset[
      int
    ]
    | None
  ) = None,
  preserve_provenance_block_ids: (
    frozenset[
      int
    ]
    | None
  ) = None,
) -> str:
"""

if "preserve_provenance_block_ids" not in body_text:
  if body_text.count(
    old_signature_tail
  ) != 1:
    raise RuntimeError(
      "Current audited body signature tail "
      "was not found exactly once"
    )
  body_text = body_text.replace(
    old_signature_tail,
    new_signature_tail,
    1,
  )


# ------------------------------------------------------------
# 3. Validate/default block IDs immediately after the existing
#    context_hidden_step_ids validation.
# ------------------------------------------------------------

validation_marker = (
  "preserve_provenance_block_ids must be "
  "a frozenset or None"
)

if validation_marker not in body_text:
  anchor = """  block_index_by_identity = {
"""
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

  if body_text.count(
    anchor
  ) != 1:
    raise RuntimeError(
      "Current audited block-index anchor "
      "was not found exactly once"
    )

  body_text = body_text.replace(
    anchor,
    validation + anchor,
    1,
  )


# ------------------------------------------------------------
# 4. Keep R10 step-level preservation, but disable
#    provenance-only suppression for an explicitly preserved
#    argument-level DERIVATION source block.
# ------------------------------------------------------------

old_suppression = """          suppress_provenance_only=True,
          preserve_provenance_step_ids=(
            derivation_source_step_ids
          ),
"""
new_suppression = """          suppress_provenance_only=(
            id(
              block
            ) not in preserve_provenance_block_ids
          ),
          preserve_provenance_step_ids=(
            derivation_source_step_ids
          ),
"""

if new_suppression not in body_text:
  if body_text.count(
    old_suppression
  ) != 1:
    raise RuntimeError(
      "R10 generic-renderer suppression call "
      "was not found exactly once"
    )

  body_text = body_text.replace(
    old_suppression,
    new_suppression,
    1,
  )


# ------------------------------------------------------------
# 5. Current audited multi-renderer transition block.
# ------------------------------------------------------------

derivation_marker = (
  "    derivation_source_block_ids = (\n"
)

if derivation_marker not in multi_text:
  connector_block = """    connector = (
      None
      if transition is None
      else render_toda_group_proof_narrative_transition_connector(
        transition
      )
    )
"""
  replacement = connector_block + """    derivation_source_block_ids = (
      frozenset()
      if (
        transition is None
        or transition.role
        is not TodaGroupProofNarrativeTransitionRole
        .DERIVATION
      )
      else frozenset(
        id(
          source_block
        )
        for source_block in transition.source_blocks
      )
    )
"""

  if multi_text.count(
    connector_block
  ) != 1:
    raise RuntimeError(
      "Current audited transition connector block "
      "was not found exactly once"
    )

  multi_text = multi_text.replace(
    connector_block,
    replacement,
    1,
  )


# ------------------------------------------------------------
# 6. Current audited body call tail.
# ------------------------------------------------------------

call_marker = (
  "        preserve_provenance_block_ids=(\n"
)

if call_marker not in multi_text:
  old_call_tail = """        direct_derivation_premises=direct_derivation_premises,
        context_hidden_step_ids=context_hidden_step_ids,
      )
"""
  new_call_tail = """        direct_derivation_premises=direct_derivation_premises,
        context_hidden_step_ids=context_hidden_step_ids,
        preserve_provenance_block_ids=(
          derivation_source_block_ids
        ),
      )
"""

  if multi_text.count(
    old_call_tail
  ) != 1:
    raise RuntimeError(
      "Current audited body-renderer call tail "
      "was not found exactly once"
    )

  multi_text = multi_text.replace(
    old_call_tail,
    new_call_tail,
    1,
  )


# Syntax-check both complete files before either is written.
ast.parse(
  multi_text
)
ast.parse(
  body_text
)

write_python(
  MULTI,
  multi_text,
  multi_bom,
)
write_python(
  BODY,
  body_text,
  body_bom,
)

print(
  "Phase 143-75AP R11-R4 audited "
  "argument-level DERIVATION source patch applied."
)
