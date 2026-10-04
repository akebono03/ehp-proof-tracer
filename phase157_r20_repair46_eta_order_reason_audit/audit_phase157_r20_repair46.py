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

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_aggregate_semantics import (
  build_toda_group_proof_narrative_aggregate_semantic_sidecar,
)
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
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


TARGET = (
  r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$"
)


def describe_step(
  step,
) -> str:
  rule = (
    None
    if step.inference_rule is None
    else step.inference_rule.name
  )
  rendered = (
    _render_generic_narrative_step(
      step
    )
    or ""
  )

  return (
    "id="
    + str(
      id(
        step
      )
    )
    + " | type="
    + type(
      step.conclusion
    ).__name__
    + " | rule="
    + repr(
      rule
    )
    + " | rendered="
    + repr(
      rendered
    )
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
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  aggregate_sidecar = (
    build_toda_group_proof_narrative_aggregate_semantic_sidecar(
      presentation
    )
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )

  matches = tuple(
    node.proof_step
    for node in presentation.nodes
    if (
      _render_generic_narrative_step(
        node.proof_step
      )
      == TARGET
    )
  )

  print("=" * 96)
  print("ETA_3^3 ORDER STEP")
  print("=" * 96)
  print(
    "target count:",
    len(
      matches
    ),
  )

  for index, step in enumerate(
    matches,
    1,
  ):
    print("")
    print(
      "MATCH",
      index,
    )
    print(
      describe_step(
        step
      )
    )

    print("PREMISES")
    for premise_index, premise in enumerate(
      step.premises
    ):
      print(
        f"  [{premise_index}]",
        describe_step(
          premise
        ),
      )

    print("AGGREGATE SEMANTICS")
    aggregate_matches = tuple(
      semantic
      for semantic in aggregate_sidecar.step_semantics
      if semantic.proof_step is step
    )

    if not aggregate_matches:
      print("  none")
    else:
      for semantic in aggregate_matches:
        print(
          " ",
          semantic.kind,
        )

    print("REASONS")
    reasons = tuple(
      reason
      for reason in reason_sidecar.reasons
      if reason.conclusion_step is step
    )

    if not reasons:
      print("  none")
    else:
      for reason in reasons:
        print(
          "  kind=",
          reason.kind,
        )
        print(
          "  premise ids=",
          tuple(
            id(
              premise
            )
            for premise in reason.premise_steps
          ),
        )
        print(
          "  sentence=",
          repr(
            render_toda_group_proof_narrative_reason_sentence(
              reason
            )
          ),
        )

  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]

  print("")
  print("=" * 96)
  print("VISIBLE WINDOW")
  print("=" * 96)

  watch = (
    "[R1]より",
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である.",
    TARGET,
    r"$\operatorname{ord}(\eta_{3}^{3})=2$",
  )

  for index, paragraph in enumerate(
    body.split(
      "\n\n"
    )
  ):
    if any(
      token in paragraph
      for token in watch
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
