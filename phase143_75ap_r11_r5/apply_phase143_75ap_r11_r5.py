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
  newline = (
    "\r\n"
    if b"\r\n" in raw
    else "\n"
  )
  return (
    raw.decode(
      "utf-8-sig"
    ).replace(
      "\r\n",
      "\n",
    ),
    raw.startswith(
      b"\xef\xbb\xbf"
    ),
    newline,
  )


def write_python(
  path,
  text,
  had_bom,
  newline,
):
  ast.parse(
    text
  )
  normalized = text.replace(
    "\r\n",
    "\n",
  )
  if newline == "\r\n":
    normalized = normalized.replace(
      "\n",
      "\r\n",
    )
  path.write_text(
    normalized,
    encoding=(
      "utf-8-sig"
      if had_bom
      else "utf-8"
    ),
    newline="",
  )


def offsets(
  text,
):
  result = [
    0
  ]
  for index, char in enumerate(
    text
  ):
    if char == "\n":
      result.append(
        index + 1
      )
  return result


def span(
  text,
  node,
):
  line_offsets = offsets(
    text
  )
  return (
    line_offsets[
      node.lineno - 1
    ] + node.col_offset,
    line_offsets[
      node.end_lineno - 1
    ] + node.end_col_offset,
  )


def top_function(
  text,
  name,
):
  tree = ast.parse(
    text
  )
  matches = [
    node
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
    and node.name == name
  ]
  if len(
    matches
  ) != 1:
    raise RuntimeError(
      "Expected exactly one top-level function: "
      + name
    )
  return matches[
    0
  ]


multi_text, multi_bom, multi_newline = read_python(
  MULTI
)
body_text, body_bom, body_newline = read_python(
  BODY
)


# ------------------------------------------------------------
# 1. AST-based import replacement.
# ------------------------------------------------------------

multi_tree = ast.parse(
  multi_text
)
transition_imports = [
  node
  for node in multi_tree.body
  if isinstance(
    node,
    ast.ImportFrom,
  )
  and node.module
  == "toda_group_proof_narrative_transitions"
]

if len(
  transition_imports
) != 1:
  raise RuntimeError(
    "Expected exactly one transitions ImportFrom node"
  )

transition_import = transition_imports[
  0
]
import_names = {
  alias.name
  for alias in transition_import.names
}

if (
  "extract_toda_group_proof_narrative_transitions"
  not in import_names
):
  raise RuntimeError(
    "Transitions import does not contain extractor"
  )

if (
  "TodaGroupProofNarrativeTransitionRole"
  not in import_names
):
  start, end = span(
    multi_text,
    transition_import,
  )
  replacement = """from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)"""
  multi_text = (
    multi_text[
      :start
    ]
    + replacement
    + multi_text[
      end:
    ]
  )


# ------------------------------------------------------------
# 2. Add body parameter using the audited current tail.
#    Text is normalized to LF first, so this is CRLF-safe.
# ------------------------------------------------------------

body_function_name = (
  "render_toda_group_proof_narrative_argument_body_markdown"
)
body_node = top_function(
  body_text,
  body_function_name,
)
start, end = span(
  body_text,
  body_node,
)
body_function = body_text[
  start:end
]

if (
  "preserve_provenance_block_ids"
  not in body_function
):
  tail = """  context_hidden_step_ids: (
    frozenset[
      int
    ]
    | None
  ) = None,
) -> str:
"""
  replacement = """  context_hidden_step_ids: (
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

  if body_function.count(
    tail
  ) != 1:
    raise RuntimeError(
      "Audited body signature tail not found once"
    )

  body_function = body_function.replace(
    tail,
    replacement,
    1,
  )


# ------------------------------------------------------------
# 3. Add validation before block_index_by_identity.
# ------------------------------------------------------------

validation_marker = (
  "preserve_provenance_block_ids must be "
  "a frozenset or None"
)

if validation_marker not in body_function:
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

  if body_function.count(
    anchor
  ) != 1:
    raise RuntimeError(
      "Body block-index anchor not found once"
    )

  body_function = body_function.replace(
    anchor,
    validation + anchor,
    1,
  )


# ------------------------------------------------------------
# 4. Change the generic block suppression expression.
# ------------------------------------------------------------

new_suppression = """          suppress_provenance_only=(
            id(
              block
            ) not in preserve_provenance_block_ids
          ),
"""

if new_suppression not in body_function:
  old_suppression = (
    "          suppress_provenance_only=True,\n"
  )

  if body_function.count(
    old_suppression
  ) != 1:
    raise RuntimeError(
      "Generic provenance suppression argument "
      "not found exactly once"
    )

  body_function = body_function.replace(
    old_suppression,
    new_suppression,
    1,
  )

body_text = (
  body_text[
    :start
  ]
  + body_function
  + body_text[
    end:
  ]
)


# ------------------------------------------------------------
# 5. Add argument-level DERIVATION source block IDs.
# ------------------------------------------------------------

multi_function_name = (
  "render_toda_group_proof_narrative_multi_argument_markdown"
)
multi_node = top_function(
  multi_text,
  multi_function_name,
)
start, end = span(
  multi_text,
  multi_node,
)
multi_function = multi_text[
  start:end
]

if (
  "derivation_source_block_ids = ("
  not in multi_function
):
  connector = """    connector = (
      None
      if transition is None
      else render_toda_group_proof_narrative_transition_connector(
        transition
      )
    )
"""
  replacement = connector + """    derivation_source_block_ids = (
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

  if multi_function.count(
    connector
  ) != 1:
    raise RuntimeError(
      "Transition connector block not found once"
    )

  multi_function = multi_function.replace(
    connector,
    replacement,
    1,
  )


# ------------------------------------------------------------
# 6. Pass IDs through the audited current body-call tail.
# ------------------------------------------------------------

if (
  "preserve_provenance_block_ids=("
  not in multi_function
):
  tail = """        direct_derivation_premises=direct_derivation_premises,
        context_hidden_step_ids=context_hidden_step_ids,
      )
"""
  replacement = """        direct_derivation_premises=direct_derivation_premises,
        context_hidden_step_ids=context_hidden_step_ids,
        preserve_provenance_block_ids=(
          derivation_source_block_ids
        ),
      )
"""

  if multi_function.count(
    tail
  ) != 1:
    raise RuntimeError(
      "Audited body-call tail not found once"
    )

  multi_function = multi_function.replace(
    tail,
    replacement,
    1,
  )

multi_text = (
  multi_text[
    :start
  ]
  + multi_function
  + multi_text[
    end:
  ]
)


# ------------------------------------------------------------
# 7. Validate both complete modules before writing either.
# ------------------------------------------------------------

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
  multi_newline,
)
write_python(
  BODY,
  body_text,
  body_bom,
  body_newline,
)

print(
  "Phase 143-75AP R11-R5 newline-independent "
  "DERIVATION source patch applied."
)
