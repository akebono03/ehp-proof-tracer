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

import toda_group_proof_narrative_argument_body_renderer as body_renderer
import toda_group_proof_narrative_argument_multi_renderer as multi_renderer

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGET = r"\eta_{3}^{3} = \eta_{3}^{3}"

original_helper = (
  body_renderer
  ._is_toda_group_proof_narrative_rendered_reflexive_equality_step
)
original_body = (
  body_renderer
  .render_toda_group_proof_narrative_argument_body_markdown
)
original_relocatable = (
  body_renderer
  ._relocatable_toda_group_proof_narrative_direct_derivation_premises
)
original_insert = (
  body_renderer
  ._insert_toda_group_proof_narrative_relocated_direct_premises
)


def rendered_step(
  step,
) -> str:
  return (
    body_renderer
    ._render_generic_narrative_step(
      step
    )
  )


def traced_helper(
  proof_step,
):
  result = original_helper(
    proof_step
  )
  rendered = rendered_step(
    proof_step
  )

  if TARGET in rendered:
    statement = proof_step.conclusion

    print("")
    print("=" * 88)
    print("TARGET HELPER CHECK")
    print("=" * 88)
    print(
      "result:",
      result,
    )
    print(
      "rendered:",
      rendered,
    )
    print(
      "lhs type:",
      type(
        statement.lhs
      ).__name__,
    )
    print(
      "rhs type:",
      type(
        statement.rhs
      ).__name__,
    )

    try:
      lhs = (
        body_renderer
        ._render_generic_narrative_expression_latex(
          statement.lhs
        )
      )
      print(
        "lhs normalized:",
        lhs,
      )
    except Exception as exc:
      print(
        "lhs normalize error:",
        type(
          exc
        ).__name__,
        str(
          exc
        ),
      )

    try:
      rhs = (
        body_renderer
        ._render_generic_narrative_expression_latex(
          statement.rhs
        )
      )
      print(
        "rhs normalized:",
        rhs,
      )
    except Exception as exc:
      print(
        "rhs normalize error:",
        type(
          exc
        ).__name__,
        str(
          exc
        ),
      )

  return result


def traced_relocatable(
  direct_derivation_premises,
  sources_by_target_id,
  conclusion_block,
):
  result = original_relocatable(
    direct_derivation_premises,
    sources_by_target_id,
    conclusion_block,
  )

  matching = tuple(
    step
    for step in result
    if TARGET in rendered_step(
      step
    )
  )

  if matching:
    print("")
    print("=" * 88)
    print("RAW RELOCATABLE RESULT CONTAINS TARGET")
    print("=" * 88)

    for step in matching:
      print(
        "helper:",
        original_helper(
          step
        ),
      )
      print(
        "rendered:",
        rendered_step(
          step
        ),
      )

  return result


def traced_insert(
  block_lines,
  block,
  conclusion_step,
  direct_derivation_premises,
  relocated_direct_premises,
):
  matching = tuple(
    step
    for step in relocated_direct_premises
    if TARGET in rendered_step(
      step
    )
  )

  if matching:
    print("")
    print("=" * 88)
    print("FILTERED RELOCATED INPUT STILL CONTAINS TARGET")
    print("=" * 88)

    for step in matching:
      print(
        "helper:",
        original_helper(
          step
        ),
      )

  result = original_insert(
    block_lines,
    block,
    conclusion_step,
    direct_derivation_premises,
    relocated_direct_premises,
  )

  if any(
    TARGET in line
    for line in result
  ):
    print("")
    print("=" * 88)
    print("RELOCATED INSERT OUTPUT CONTAINS TARGET")
    print("=" * 88)

    for index, line in enumerate(
      result
    ):
      if TARGET in line:
        print(
          f"[{index}]",
          line,
        )

  return result


def traced_body(
  *args,
  **kwargs,
):
  result = original_body(
    *args,
    **kwargs,
  )

  if TARGET in result:
    print("")
    print("=" * 88)
    print("ARGUMENT BODY OUTPUT CONTAINS TARGET")
    print("=" * 88)

    for index, paragraph in enumerate(
      result.split(
        "\n\n"
      )
    ):
      if TARGET in paragraph:
        print(
          f"[{index}]",
          paragraph,
        )

  return result


def main() -> int:
  body_renderer._is_toda_group_proof_narrative_rendered_reflexive_equality_step = (
    traced_helper
  )
  body_renderer._relocatable_toda_group_proof_narrative_direct_derivation_premises = (
    traced_relocatable
  )
  body_renderer._insert_toda_group_proof_narrative_relocated_direct_premises = (
    traced_insert
  )

  multi_renderer.render_toda_group_proof_narrative_argument_body_markdown = (
    traced_body
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
  presentation = build_toda_group_proof_presentation(
    replay
  )

  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  print("")
  print("=" * 88)
  print("FINAL")
  print("=" * 88)
  print(
    "target present:",
    TARGET in rendered,
  )

  for index, paragraph in enumerate(
    rendered.split(
      "\n\n"
    )
  ):
    if TARGET in paragraph:
      print(
        f"[{index}]",
        paragraph,
      )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
