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

import toda_group_proof_narrative_contribution_renderer as contribution_renderer

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _generic_short_exact_sequence_latex,
  _generic_short_exact_sequence_reason_prose,
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


REASON = (
  "この完全性と, 左の写像が単射, "
  "右の写像が全射であることより, "
  "次の短完全列を得る."
)


def describe_map_statement(
  proof_step,
) -> None:
  statement = proof_step.conclusion
  group_map = getattr(
    statement,
    "map",
    None,
  )

  print(
    "  type=",
    type(
      statement
    ).__name__,
  )
  print(
    "  rendered=",
    repr(
      _render_generic_narrative_step(
        proof_step
      )
    ),
  )
  print(
    "  has .map=",
    group_map is not None,
  )

  if group_map is not None:
    print(
      "  map type=",
      type(
        group_map
      ).__name__,
    )
    print(
      "  map name=",
      repr(
        getattr(
          group_map,
          "name",
          None,
        )
      ),
    )
    print(
      "  source=",
      repr(
        getattr(
          group_map,
          "source_group",
          None,
        )
      ),
    )
    print(
      "  target=",
      repr(
        getattr(
          group_map,
          "target_group",
          None,
        )
      ),
    )


def main() -> int:
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
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]
  paragraphs = body.split(
    "\n\n"
  )

  print("=" * 96)
  print("MAP PROPERTY CANDIDATES")
  print("=" * 96)

  for node in presentation.nodes:
    line = (
      _render_generic_narrative_step(
        node.proof_step
      )
      or ""
    )

    if (
      "は単射である."
      in line
      or "は全射である."
      in line
    ):
      describe_map_statement(
        node.proof_step
      )
      print("-" * 96)

  print("")
  print("=" * 96)
  print("SHORT EXACT CANDIDATES")
  print("=" * 96)

  for node in presentation.nodes:
    step = node.proof_step
    short_exact = (
      _generic_short_exact_sequence_latex(
        presentation,
        step,
      )
    )

    if short_exact is None:
      continue

    reason = (
      _generic_short_exact_sequence_reason_prose(
        presentation,
        step,
      )
    )

    print(
      "exactness type=",
      type(
        step.conclusion
      ).__name__,
    )
    print(
      "exactness rendered=",
      repr(
        _render_generic_narrative_step(
          step
        )
      ),
    )
    print(
      "short exact=",
      repr(
        short_exact
      ),
    )
    print(
      "reason=",
      repr(
        reason
      ),
    )

    window = getattr(
      step.conclusion,
      "window",
      None,
    )

    if window is not None:
      print(
        "window source=",
        repr(
          window.source_term
        ),
      )
      print(
        "window middle=",
        repr(
          window.middle_term
        ),
      )
      print(
        "window target=",
        repr(
          window.target_term
        ),
      )
      print(
        "first map=",
        repr(
          getattr(
            window.first_map,
            "name",
            None,
          )
        ),
      )
      print(
        "second map=",
        repr(
          getattr(
            window.second_map,
            "name",
            None,
          )
        ),
      )

    reason_indices = tuple(
      i
      for i, paragraph in enumerate(
        paragraphs
      )
      if paragraph.strip() == reason
    )
    sequence_target = (
      "$"
      + short_exact
      + "$."
    )
    sequence_indices = tuple(
      i
      for i, paragraph in enumerate(
        paragraphs
      )
      if paragraph.strip() == sequence_target
    )

    print(
      "visible reason indices=",
      reason_indices,
    )
    print(
      "visible sequence indices=",
      sequence_indices,
    )
    print("-" * 96)

  print("")
  print("=" * 96)
  print("VISIBLE SUPPORT ORDER")
  print("=" * 96)

  tokens = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である.",
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である.",
    REASON,
    r"$0\longrightarrow \pi_{5}^{2}\xrightarrow{E} \pi_{6}^{3}\xrightarrow{H} \pi_{6}^{5}\longrightarrow 0$.",
  )

  for index, paragraph in enumerate(
    paragraphs
  ):
    if any(
      token in paragraph
      for token in tokens
    ):
      print(
        f"[{index}]",
        paragraph,
      )

  print("")
  print("=" * 96)
  print("DIRECT FUNCTION RE-RUN")
  print("=" * 96)

  reordered = (
    contribution_renderer
    .order_toda_group_proof_narrative_short_exact_support(
      presentation,
      body,
    )
  )

  print(
    "changed:",
    reordered != body,
  )

  if reordered != body:
    reordered_paragraphs = reordered.split(
      "\n\n"
    )

    for index, paragraph in enumerate(
      reordered_paragraphs
    ):
      if any(
        token in paragraph
        for token in tokens
      ):
        print(
          f"[{index}]",
          paragraph,
        )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
