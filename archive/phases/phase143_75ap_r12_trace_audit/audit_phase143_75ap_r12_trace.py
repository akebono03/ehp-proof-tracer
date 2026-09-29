from pathlib import Path
import runpy

import toda_group_proof_narrative_argument_multi_renderer as multi
import toda_group_proof_narrative_argument_body_renderer as body

TARGET = "Toda515Sigma8TransportedDecompositionStatement"


def statement_name(
  step,
):
  return type(
    step.conclusion
  ).__name__


def describe_block(
  block,
):
  return {
    "id": id(
      block
    ),
    "role": str(
      getattr(
        block,
        "role",
        None,
      )
    ),
    "steps": [
      statement_name(
        step
      )
      for step in block.steps
    ],
    "contains_target": any(
      statement_name(
        step
      ) == TARGET
      for step in block.steps
    ),
  }


print(
  "=" * 78
)
print(
  "Phase 143-75AP R12 transported decomposition runtime trace"
)
print(
  "=" * 78
)

original_local = (
  multi.extract_toda_group_proof_narrative_argument_local_body_blocks
)
original_body_render = (
  multi.render_toda_group_proof_narrative_argument_body_markdown
)
original_generic = (
  body._render_generic_narrative_proof_block
)


def traced_local(
  *args,
  **kwargs,
):
  result = original_local(
    *args,
    **kwargs,
  )

  print(
    "\n[LOCAL BODY]"
  )
  for index, block in enumerate(
    result
  ):
    description = describe_block(
      block
    )
    if (
      description[
        "contains_target"
      ]
      or any(
        "Sigma8" in name
        or "Sigma8" in name.replace(
          "_",
          "",
        )
        or "515" in name
        for name in description[
          "steps"
        ]
      )
    ):
      print(
        index,
        description,
      )

  return result


def traced_body_render(
  *args,
  **kwargs,
):
  local_body_blocks = (
    args[
      2
    ]
    if len(
      args
    ) >= 3
    else kwargs.get(
      "local_body_blocks",
      (),
    )
  )

  print(
    "\n[BODY CALL]"
  )
  print(
    "local block ids:",
    [
      id(
        block
      )
      for block in local_body_blocks
    ],
  )
  print(
    "target local block ids:",
    [
      id(
        block
      )
      for block in local_body_blocks
      if any(
        statement_name(
          step
        ) == TARGET
        for step in block.steps
      )
    ],
  )
  print(
    "preserve_provenance_block_ids:",
    kwargs.get(
      "preserve_provenance_block_ids",
    ),
  )
  print(
    "connector_before_block_id:",
    kwargs.get(
      "connector_before_block_id",
    ),
  )

  return original_body_render(
    *args,
    **kwargs,
  )


def traced_generic(
  presentation,
  blocks,
  block_index,
  *args,
  **kwargs,
):
  block = blocks[
    block_index
  ]
  names = [
    statement_name(
      step
    )
    for step in block.steps
  ]

  if (
    TARGET in names
    or any(
      "Sigma8" in name
      or "515" in name
      for name in names
    )
  ):
    print(
      "\n[GENERIC BLOCK]"
    )
    print(
      "index:",
      block_index,
    )
    print(
      "id:",
      id(
        block
      ),
    )
    print(
      "role:",
      getattr(
        block,
        "role",
        None,
      ),
    )
    print(
      "steps:",
      names,
    )
    print(
      "suppress_provenance_only:",
      kwargs.get(
        "suppress_provenance_only",
      ),
    )
    print(
      "preserve_provenance_step_ids:",
      kwargs.get(
        "preserve_provenance_step_ids",
      ),
    )

  result = original_generic(
    presentation,
    blocks,
    block_index,
    *args,
    **kwargs,
  )

  if TARGET in names:
    print(
      "rendered target block:"
    )
    print(
      repr(
        tuple(
          result
        )
      )
    )

  return result


multi.extract_toda_group_proof_narrative_argument_local_body_blocks = (
  traced_local
)
multi.render_toda_group_proof_narrative_argument_body_markdown = (
  traced_body_render
)
body._render_generic_narrative_proof_block = (
  traced_generic
)

test_globals = runpy.run_path(
  str(
    Path(
      "tests/test_phase143_51b_aggregate_statement_prose.py"
    )
  )
)

render = test_globals.get(
  "_render_multi_argument"
)

if render is None:
  raise RuntimeError(
    "Could not load _render_multi_argument from phase143_51b test"
  )

print(
  "\n[RENDER START]"
)
rendered = render(
  8,
  7,
)
print(
  "\n[FINAL NARRATIVE]"
)
print(
  rendered
)

print(
  "\n[SOURCE OCCURRENCES]"
)
for path in sorted(
  Path(
    "."
  ).glob(
    "*.py"
  )
):
  text = path.read_text(
    encoding="utf-8-sig",
  )
  if TARGET not in text:
    continue

  print(
    path
  )
  for number, line in enumerate(
    text.splitlines(),
    start=1,
  ):
    if TARGET in line:
      print(
        f"  {number}: {line}"
      )
