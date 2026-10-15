from __future__ import annotations

import sys
from collections import deque
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
from toda_group_proof_narrative_references import (
  extract_toda_group_proof_step_literature_reference,
)


NEEDLES = (
  r"H\left(\nu'\eta_{6}\right) = H\left(\nu'\right)\eta_{6}",
  r"\Delta: \pi_{7}^{5} \to \pi_{5}^{2}",
)


def describe_step(
  step,
) -> str:
  rendered = (
    _render_generic_narrative_step(
      step
    )
    or ""
  )
  rule = (
    None
    if step.inference_rule is None
    else step.inference_rule.name
  )
  reference = (
    extract_toda_group_proof_step_literature_reference(
      step
    )
  )
  locator = (
    None
    if reference is None
    else reference.locator
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
    + " | ref="
    + repr(
      locator
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

  consumers = {}

  for edge in presentation.edges:
    consumers.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  print("=" * 96)
  print("MATCHING STEPS")
  print("=" * 96)

  for needle in NEEDLES:
    print("")
    print("NEEDLE:", needle)
    print("-" * 96)

    matches = tuple(
      node.proof_step
      for node in presentation.nodes
      if needle
      in (
        _render_generic_narrative_step(
          node.proof_step
        )
        or ""
      )
    )

    print(
      "count:",
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

      print("CONSUMERS")
      for consumer_index, consumer in enumerate(
        consumers.get(
          id(
            step
          ),
          (),
        )
      ):
        print(
          f"  [{consumer_index}]",
          describe_step(
            consumer
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
  print("VISIBLE ORDER")
  print("=" * 96)

  watch = (
    r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}",
    r"$H\left(\nu'\eta_{6}\right) = H\left(\nu'\right)\eta_{6}",
    r"$\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である.",
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である.",
    r"$0\longrightarrow \pi_{5}^{2}",
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
