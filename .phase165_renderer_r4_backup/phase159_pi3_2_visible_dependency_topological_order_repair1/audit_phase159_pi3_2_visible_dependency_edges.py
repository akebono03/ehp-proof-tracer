from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(
  REPO_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
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


def main() -> None:
  report = build_standard_toda_report(
    n=2,
    k=1,
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
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  interesting = (
    "単射",
    "全射",
    "同型",
    "零写像",
    r"\pi_{2}^{1} = 0",
    r"\pi_{3}^{3} = ",
    r"\eta_{2}",
  )

  visible_ids = set()

  print(
    "=== Phase 159 pi3_2 dependency-edge audit ==="
  )

  for node in presentation.nodes:
    step = node.proof_step
    rendered = (
      _render_generic_narrative_step(
        step
      )
    )

    if any(
      token in rendered
      for token in interesting
    ):
      visible_ids.add(
        id(
          step
        )
      )
      print(
        "STEP",
        id(
          step
        ),
        rendered,
      )

  print()
  print(
    "=== direct edges among audited steps ==="
  )

  for edge in presentation.edges:
    premise = edge.premise_step
    consumer = edge.parent_step

    if (
      id(
        premise
      )
      not in visible_ids
      or id(
        consumer
      )
      not in visible_ids
    ):
      continue

    print(
      _render_generic_narrative_step(
        premise
      )
    )
    print(
      "  ->"
    )
    print(
      _render_generic_narrative_step(
        consumer
      )
    )
    print()


if __name__ == "__main__":
  main()
