from __future__ import annotations

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
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
from repository_element_presentation import (
  render_repository_conclusion_latex,
)


def _presentation(
  depth: int,
):
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
    max_depth=depth,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  return raw, closure


def main() -> int:
  for depth in (
    2,
    3,
  ):
    raw, presentation = _presentation(
      depth
    )
    sidecar = build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
    blocks = build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )

    print(
      "=" * 90
    )
    print(
      "DEPTH",
      depth,
    )
    print(
      "=" * 90
    )

    order_steps = tuple(
      proof_step
      for block in blocks
      if block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.ORDER
      for proof_step in block.steps
    )

    print(
      "ORDER steps:",
      len(
        order_steps
      ),
    )

    for index, step in enumerate(
      order_steps,
      start=1,
    ):
      statement = step.conclusion
      print()
      print(
        "ORDER STEP",
        index,
      )
      print(
        "type:",
        type(
          statement
        ).__name__,
      )
      print(
        "has lhs:",
        hasattr(
          statement,
          "lhs",
        ),
      )
      print(
        "has rhs:",
        hasattr(
          statement,
          "rhs",
        ),
      )
      if hasattr(
        statement,
        "lhs",
      ):
        print(
          "lhs type:",
          type(
            statement.lhs
          ).__name__,
        )
        print(
          "lhs repr:",
          repr(
            statement.lhs
          ),
        )
      if hasattr(
        statement,
        "rhs",
      ):
        print(
          "rhs type:",
          type(
            statement.rhs
          ).__name__,
        )
        print(
          "rhs repr:",
          repr(
            statement.rhs
          ),
        )

      try:
        raw_latex = render_repository_conclusion_latex(
          statement
        )
      except Exception as exc:
        raw_latex = (
          "<"
          + type(
            exc
          ).__name__
          + ": "
          + str(
            exc
          )
          + ">"
        )

      print(
        "raw latex:",
        raw_latex,
      )
      print(
        "generic:",
        _render_generic_narrative_step(
          step
        ),
      )

    rendered = render_toda_group_proof_narrative_markdown(
      raw
    )

    print()
    print(
      "PUBLIC LINES CONTAINING ord"
    )
    for line in rendered.splitlines():
      if "ord" in line:
        print(
          line
        )

    print()
    print(
      "PUBLIC LINES CONTAINING eta_{3}"
    )
    for line in rendered.splitlines():
      if (
        r"\eta_{3}" in line
        and (
          "ord" in line
          or r"\tag{3}" in line
        )
      ):
        print(
          line
        )

  print()
  print(
    "PASS: diagnostic completed."
  )
  print(
    "Production changes: none."
  )
  print(
    "Repository-wide pytest is intentionally NOT run."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
