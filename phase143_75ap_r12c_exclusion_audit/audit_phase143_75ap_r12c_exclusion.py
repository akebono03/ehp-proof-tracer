from pathlib import Path
import runpy

import toda_group_proof_narrative_argument_multi_renderer as multi

TARGET = "Toda515Sigma8TransportedDecompositionStatement"

original_body = (
  multi.render_toda_group_proof_narrative_argument_body_markdown
)

call_index = 0


def has_target(
  block,
):
  return any(
    type(
      step.conclusion
    ).__name__ == TARGET
    for step in block.steps
  )


def traced_body(
  *args,
  **kwargs,
):
  global call_index
  call_index += 1

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
  target_blocks = tuple(
    block
    for block in local_body_blocks
    if has_target(
      block
    )
  )

  if target_blocks:
    excluded = kwargs.get(
      "excluded_non_exact_block_ids",
    )
    preserved = kwargs.get(
      "preserve_provenance_block_ids",
    )

    print(
      "=" * 78
    )
    print(
      "BODY CALL",
      call_index,
      "CONTAINING TARGET"
    )
    print(
      "=" * 78
    )

    for block in target_blocks:
      block_id = id(
        block
      )
      print(
        "target block id:",
        block_id
      )
      print(
        "excluded:",
        excluded
      )
      print(
        "target in excluded:",
        (
          excluded is not None
          and block_id in excluded
        )
      )
      print(
        "preserved:",
        preserved
      )
      print(
        "target in preserved:",
        (
          preserved is not None
          and block_id in preserved
        )
      )

  return original_body(
    *args,
    **kwargs,
  )


multi.render_toda_group_proof_narrative_argument_body_markdown = (
  traced_body
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
    "Could not load _render_multi_argument"
  )

rendered = render(
  8,
  7,
)

print(
  "\nTARGET LATEX PRESENT:",
  r"$\pi_{15}^{8} \cong " in rendered,
)
