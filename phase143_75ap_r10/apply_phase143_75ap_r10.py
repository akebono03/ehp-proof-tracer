from pathlib import Path

GENERIC = Path(
  "toda_group_proof_generic_narrative_renderer.py"
)
BODY = Path(
  "toda_group_proof_narrative_argument_body_renderer.py"
)

generic_text = GENERIC.read_text(
  encoding="utf-8",
)
body_text = BODY.read_text(
  encoding="utf-8",
)

old_signature = """  suppress_provenance_only: bool = False,
) -> tuple[
"""
new_signature = """  suppress_provenance_only: bool = False,
  preserve_provenance_step_ids: (
    frozenset[int]
    | None
  ) = None,
) -> tuple[
"""

if generic_text.count(old_signature) != 1:
  raise RuntimeError(
    "Expected exactly one generic renderer signature target"
  )

generic_text = generic_text.replace(
  old_signature,
  new_signature,
  1,
)

old_validation_anchor = """  block = blocks[
    block_index
  ]

  if show_dependency_labels:
"""
new_validation_anchor = """  if (
    preserve_provenance_step_ids is not None
    and not isinstance(
      preserve_provenance_step_ids,
      frozenset,
    )
  ):
    raise TypeError(
      "preserve_provenance_step_ids must be "
      "a frozenset or None"
    )

  if preserve_provenance_step_ids is None:
    preserve_provenance_step_ids = frozenset()

  for step_id in preserve_provenance_step_ids:
    if (
      not isinstance(
        step_id,
        int,
      )
      or isinstance(
        step_id,
        bool,
      )
    ):
      raise TypeError(
        "preserve_provenance_step_ids must "
        "contain only integers"
      )

  block = blocks[
    block_index
  ]

  if show_dependency_labels:
"""

if generic_text.count(old_validation_anchor) != 1:
  raise RuntimeError(
    "Expected exactly one generic renderer validation anchor"
  )

generic_text = generic_text.replace(
  old_validation_anchor,
  new_validation_anchor,
  1,
)

old_suppression = """    if (
      suppress_provenance_only
      and _is_generic_narrative_provenance_only_statement(
        proof_step.conclusion
      )
    ):
      continue
"""
new_suppression = """    if (
      suppress_provenance_only
      and id(
        proof_step
      ) not in preserve_provenance_step_ids
      and _is_generic_narrative_provenance_only_statement(
        proof_step.conclusion
      )
    ):
      continue
"""

if generic_text.count(old_suppression) != 1:
  raise RuntimeError(
    "Expected exactly one provenance suppression target"
  )

generic_text = generic_text.replace(
  old_suppression,
  new_suppression,
  1,
)

old_sources = """  step_derivation_sources_by_target_id = (
    _step_derivation_sources_by_target_id(
      presentation,
      blocks,
    )
  )

  seen_local_block_ids = set()
"""
new_sources = """  step_derivation_sources_by_target_id = (
    _step_derivation_sources_by_target_id(
      presentation,
      blocks,
    )
  )
  derivation_source_step_ids = frozenset(
    id(
      source_step
    )
    for source_steps in (
      step_derivation_sources_by_target_id.values()
    )
    for source_step in source_steps
  )

  seen_local_block_ids = set()
"""

if body_text.count(old_sources) != 1:
  raise RuntimeError(
    "Expected exactly one derivation-source map target"
  )

body_text = body_text.replace(
  old_sources,
  new_sources,
  1,
)

old_call = """          show_dependency_labels=False,
          suppress_provenance_only=True,
        )
"""
new_call = """          show_dependency_labels=False,
          suppress_provenance_only=True,
          preserve_provenance_step_ids=(
            derivation_source_step_ids
          ),
        )
"""

if body_text.count(old_call) != 1:
  raise RuntimeError(
    "Expected exactly one argument-body generic renderer call"
  )

body_text = body_text.replace(
  old_call,
  new_call,
  1,
)

GENERIC.write_text(
  generic_text,
  encoding="utf-8",
)
BODY.write_text(
  body_text,
  encoding="utf-8",
)

print(
  "Phase 143-75AP R10 derivation-source semantic "
  "preservation patch applied."
)
