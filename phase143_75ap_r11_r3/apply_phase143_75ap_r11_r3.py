from pathlib import Path
import ast

MULTI = Path(
  "toda_group_proof_narrative_argument_multi_renderer.py"
)
BODY = Path(
  "toda_group_proof_narrative_argument_body_renderer.py"
)

multi_bytes = MULTI.read_bytes()
body_bytes = BODY.read_bytes()

multi_has_bom = multi_bytes.startswith(
  b"\xef\xbb\xbf"
)
body_has_bom = body_bytes.startswith(
  b"\xef\xbb\xbf"
)

multi_text = multi_bytes.decode(
  "utf-8-sig"
)
body_text = body_bytes.decode(
  "utf-8-sig"
)


def _function_node(
  text,
  function_name,
):
  tree = ast.parse(
    text
  )
  matches = [
    node
    for node in tree.body
    if isinstance(
      node,
      (
        ast.FunctionDef,
        ast.AsyncFunctionDef,
      ),
    )
    and node.name == function_name
  ]

  if len(
    matches
  ) != 1:
    raise RuntimeError(
      "Expected exactly one function named "
      + function_name
    )

  return matches[0]


def _line_offsets(
  text,
):
  offsets = [
    0
  ]

  for index, char in enumerate(
    text
  ):
    if char == "\n":
      offsets.append(
        index + 1
      )

  return offsets


def _absolute_offset(
  text,
  lineno,
  col_offset,
):
  offsets = _line_offsets(
    text
  )

  return (
    offsets[
      lineno - 1
    ]
    + col_offset
  )


def _replace_span(
  text,
  start,
  end,
  replacement,
):
  return (
    text[
      :start
    ]
    + replacement
    + text[
      end:
    ]
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

  if multi_text.count(
    old_import
  ) != 1:
    raise RuntimeError(
      "Expected exactly one narrative transitions import block"
    )

  multi_text = multi_text.replace(
    old_import,
    new_import,
    1,
  )


# ------------------------------------------------------------
# 2. Add preserve_provenance_block_ids to the body renderer
#    using the AST function signature rather than an exact
#    whole-signature string.
# ------------------------------------------------------------

body_function_name = (
  "render_toda_group_proof_narrative_argument_body_markdown"
)

body_node = _function_node(
  body_text,
  body_function_name,
)

body_function_text = ast.get_source_segment(
  body_text,
  body_node,
)

if body_function_text is None:
  raise RuntimeError(
    "Could not read body renderer source"
  )

if "preserve_provenance_block_ids" not in body_function_text:
  close_marker = ") -> str:\n"

  marker_index = body_function_text.find(
    close_marker
  )

  if marker_index < 0:
    raise RuntimeError(
      "Could not locate body renderer signature terminator"
    )

  parameter = """  preserve_provenance_block_ids: (
    frozenset[int]
    | None
  ) = None,
"""

  body_function_text = (
    body_function_text[
      :marker_index
    ]
    + parameter
    + body_function_text[
      marker_index:
    ]
  )

  function_start = _absolute_offset(
    body_text,
    body_node.lineno,
    body_node.col_offset,
  )
  function_end = _absolute_offset(
    body_text,
    body_node.end_lineno,
    body_node.end_col_offset,
  )

  body_text = _replace_span(
    body_text,
    function_start,
    function_end,
    body_function_text,
  )


# ------------------------------------------------------------
# 3. Add validation/defaulting inside the body renderer.
# ------------------------------------------------------------

body_node = _function_node(
  body_text,
  body_function_name,
)
body_function_text = ast.get_source_segment(
  body_text,
  body_node,
)

if body_function_text is None:
  raise RuntimeError(
    "Could not re-read body renderer source"
  )

validation_marker = (
  "preserve_provenance_block_ids must be "
  "a frozenset or None"
)

if validation_marker not in body_function_text:
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

  anchors = (
    "  lines = []\n",
    "  render_blocks = tuple(\n",
    "  step_derivation_sources_by_target_id = (\n",
  )

  anchor = next(
    (
      candidate
      for candidate in anchors
      if candidate in body_function_text
    ),
    None,
  )

  if anchor is None:
    raise RuntimeError(
      "Could not locate body renderer validation anchor"
    )

  body_function_text = body_function_text.replace(
    anchor,
    validation + anchor,
    1,
  )

  function_start = _absolute_offset(
    body_text,
    body_node.lineno,
    body_node.col_offset,
  )
  function_end = _absolute_offset(
    body_text,
    body_node.end_lineno,
    body_node.end_col_offset,
  )

  body_text = _replace_span(
    body_text,
    function_start,
    function_end,
    body_function_text,
  )


# ------------------------------------------------------------
# 4. Change only the generic block suppression expression.
# ------------------------------------------------------------

body_node = _function_node(
  body_text,
  body_function_name,
)
body_function_text = ast.get_source_segment(
  body_text,
  body_node,
)

if body_function_text is None:
  raise RuntimeError(
    "Could not read body renderer for call repair"
  )

old_suppression = (
  "          suppress_provenance_only=True,\n"
)
new_suppression = """          suppress_provenance_only=(
            id(
              block
            ) not in preserve_provenance_block_ids
          ),
"""

if old_suppression in body_function_text:
  body_function_text = body_function_text.replace(
    old_suppression,
    new_suppression,
    1,
  )
elif new_suppression not in body_function_text:
  raise RuntimeError(
    "Could not locate generic provenance suppression argument"
  )

function_start = _absolute_offset(
  body_text,
  body_node.lineno,
  body_node.col_offset,
)
function_end = _absolute_offset(
  body_text,
  body_node.end_lineno,
  body_node.end_col_offset,
)

body_text = _replace_span(
  body_text,
  function_start,
  function_end,
  body_function_text,
)


# ------------------------------------------------------------
# 5. Multi-argument renderer:
#    derive argument-level DERIVATION source block IDs.
# ------------------------------------------------------------

multi_function_name = (
  "render_toda_group_proof_narrative_multi_argument_markdown"
)

multi_node = _function_node(
  multi_text,
  multi_function_name,
)
multi_function_text = ast.get_source_segment(
  multi_text,
  multi_node,
)

if multi_function_text is None:
  raise RuntimeError(
    "Could not read multi-argument renderer source"
  )

derivation_marker = (
  "derivation_source_block_ids = ("
)

if derivation_marker not in multi_function_text:
  connector_block = """    connector = (
      None
      if transition is None
      else render_toda_group_proof_narrative_transition_connector(
        transition
      )
    )
"""

  derivation_block = connector_block + """    derivation_source_block_ids = (
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
"""

  if multi_function_text.count(
    connector_block
  ) != 1:
    raise RuntimeError(
      "Expected exactly one transition connector block"
    )

  multi_function_text = multi_function_text.replace(
    connector_block,
    derivation_block,
    1,
  )


# ------------------------------------------------------------
# 6. Pass source block IDs to the body renderer.
# ------------------------------------------------------------

body_call_marker = (
  "preserve_provenance_block_ids=("
)

if body_call_marker not in multi_function_text:
  call_tail = """        connector_text=connector,
      )
"""

  replacement_tail = """        connector_text=connector,
        preserve_provenance_block_ids=(
          derivation_source_block_ids
        ),
      )
"""

  if multi_function_text.count(
    call_tail
  ) != 1:
    raise RuntimeError(
      "Expected exactly one body renderer call tail"
    )

  multi_function_text = multi_function_text.replace(
    call_tail,
    replacement_tail,
    1,
  )

function_start = _absolute_offset(
  multi_text,
  multi_node.lineno,
  multi_node.col_offset,
)
function_end = _absolute_offset(
  multi_text,
  multi_node.end_lineno,
  multi_node.end_col_offset,
)

multi_text = _replace_span(
  multi_text,
  function_start,
  function_end,
  multi_function_text,
)


# ------------------------------------------------------------
# 7. Syntax validation before writing.
# ------------------------------------------------------------

ast.parse(
  multi_text
)
ast.parse(
  body_text
)

MULTI.write_text(
  multi_text,
  encoding=(
    "utf-8-sig"
    if multi_has_bom
    else "utf-8"
  ),
)
BODY.write_text(
  body_text,
  encoding=(
    "utf-8-sig"
    if body_has_bom
    else "utf-8"
  ),
)

print(
  "Phase 143-75AP R11-R3 argument-level DERIVATION "
  "source preservation patch applied."
)
