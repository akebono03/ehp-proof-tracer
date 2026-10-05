from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

import toda_group_proof_narrative_argument_multi_renderer as multi_renderer

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGET = r"\eta_{3}^{3} = \eta_{3}^{3}"


original_body_renderer = (
  multi_renderer
  .render_toda_group_proof_narrative_argument_body_markdown
)
original_numbering = (
  multi_renderer
  .number_toda_group_proof_narrative_equations
)

body_call_count = 0


def target_paragraphs(
  markdown: str,
):
  return tuple(
    (
      index,
      paragraph,
    )
    for index, paragraph in enumerate(
      markdown.split(
        "\n\n"
      )
    )
    if TARGET in paragraph
  )


def traced_body_renderer(
  presentation,
  blocks,
  local_body_blocks,
  primary_component,
  **kwargs,
):
  global body_call_count
  body_call_count += 1

  result = original_body_renderer(
    presentation,
    blocks,
    local_body_blocks,
    primary_component,
    **kwargs,
  )

  if TARGET not in result:
    return result

  print("")
  print("=" * 88)
  print(
    "ARGUMENT BODY CALL",
    body_call_count,
    "CONTAINS TARGET",
  )
  print("=" * 88)

  for index, paragraph in target_paragraphs(
    result
  ):
    print(
      f"target paragraph [{index}]:",
      paragraph,
    )

  print("")
  print("local body blocks:")

  for block_index, block in enumerate(
    local_body_blocks
  ):
    print(
      " block",
      block_index,
      "role=",
      block.role,
      "steps=",
      len(
        block.steps
      ),
    )

    for step_index, step in enumerate(
      block.steps
    ):
      rendered = (
        _render_generic_narrative_step(
          step
        )
      )
      print(
        "   step",
        step_index,
        "type=",
        type(
          step.conclusion
        ).__name__,
        "rule=",
        (
          None
          if step.inference_rule is None
          else step.inference_rule.name
        ),
      )
      print(
        "     rendered=",
        rendered,
      )
      print(
        "     conclusion=",
        repr(
          step.conclusion
        ),
      )

  return result


def traced_numbering(
  markdown,
  presentation,
  blocks,
):
  print("")
  print("=" * 88)
  print("EQUATION NUMBERING INPUT")
  print("=" * 88)
  print(
    "target present:",
    TARGET in markdown,
  )

  for index, paragraph in target_paragraphs(
    markdown
  ):
    print(
      f"[{index}] {paragraph}"
    )

  result = original_numbering(
    markdown,
    presentation,
    blocks,
  )

  print("")
  print("=" * 88)
  print("EQUATION NUMBERING OUTPUT")
  print("=" * 88)
  print(
    "target present:",
    TARGET in result,
  )

  for index, paragraph in target_paragraphs(
    result
  ):
    print(
      f"[{index}] {paragraph}"
    )

  return result


def main() -> int:
  multi_renderer.render_toda_group_proof_narrative_argument_body_markdown = (
    traced_body_renderer
  )
  multi_renderer.number_toda_group_proof_narrative_equations = (
    traced_numbering
  )

  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )

  rendered = (
    multi_renderer
    .render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  print("")
  print("=" * 88)
  print("FINAL BASE MARKDOWN")
  print("=" * 88)
  print(
    "target present:",
    TARGET in rendered,
  )

  for index, paragraph in target_paragraphs(
    rendered
  ):
    print(
      f"[{index}] {paragraph}"
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
