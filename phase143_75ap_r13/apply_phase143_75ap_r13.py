from pathlib import Path
import ast

PATH = Path(
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


text, had_bom, newline = read_python(
  PATH
)

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
  and node.name
  == "render_toda_group_proof_narrative_argument_body_markdown"
]

if len(
  matches
) != 1:
  raise RuntimeError(
    "Expected exactly one body renderer function"
  )

node = matches[
  0
]
lines = text.splitlines(
  keepends=True
)
start = sum(
  len(
    line
  )
  for line in lines[
    :node.lineno - 1
  ]
)
end = sum(
  len(
    line
  )
  for line in lines[
    :node.end_lineno
  ]
)
function = text[
  start:end
]

old = """      display_steps = tuple(
        proof_step
        for proof_step in block.steps
        if (
          (
            context_hidden_step_ids is None
            or id(
              proof_step
            ) not in context_hidden_step_ids
          )
          and id(
            proof_step
          ) not in redundant_direct_premise_step_ids
          and (
            id(
              proof_step
            ) not in relocated_direct_premise_ids
            or (
              conclusion_step is not None
              and conclusion_step in block.steps
            )
          )
        )
      )
"""

new = """      preserve_direct_derivation_premises = (
        id(
          block
        ) in preserve_provenance_block_ids
      )

      display_steps = tuple(
        proof_step
        for proof_step in block.steps
        if (
          (
            context_hidden_step_ids is None
            or id(
              proof_step
            ) not in context_hidden_step_ids
          )
          and (
            preserve_direct_derivation_premises
            or id(
              proof_step
            ) not in redundant_direct_premise_step_ids
          )
          and (
            preserve_direct_derivation_premises
            or id(
              proof_step
            ) not in relocated_direct_premise_ids
            or (
              conclusion_step is not None
              and conclusion_step in block.steps
            )
          )
        )
      )
"""

if new not in function:
  if function.count(
    old
  ) != 1:
    raise RuntimeError(
      "Current audited display_steps block was not found exactly once"
    )
  function = function.replace(
    old,
    new,
    1,
  )

updated = (
  text[
    :start
  ]
  + function
  + text[
    end:
  ]
)

ast.parse(
  updated
)

write_python(
  PATH,
  updated,
  had_bom,
  newline,
)

print(
  "Phase 143-75AP R13 preserved semantic direct-premise patch applied."
)
