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


TARGET = r"H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}"


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
  conclusion_type = type(
    step.conclusion
  ).__name__

  return (
    "type="
    + conclusion_type
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

  target_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if TARGET in (
      _render_generic_narrative_step(
        node.proof_step
      )
      or ""
    )
  )

  print(
    "target steps:",
    len(
      target_steps
    ),
  )

  for target_index, target_step in enumerate(
    target_steps,
    1,
  ):
    print("")
    print("=" * 96)
    print(
      "TARGET",
      target_index,
    )
    print("=" * 96)
    print(
      describe_step(
        target_step
      )
    )

    print("")
    print("DIRECT PREMISES")
    print("-" * 96)

    for index, premise in enumerate(
      target_step.premises
    ):
      print(
        f"[{index}]",
        describe_step(
          premise
        ),
      )

    print("")
    print("ANCESTRY BFS")
    print("-" * 96)

    queue = deque(
      (
        premise,
        1,
        (
          index,
        ),
      )
      for index, premise in enumerate(
        target_step.premises
      )
    )
    visited = set()

    while queue:
      step, depth, path = queue.popleft()
      step_id = id(
        step
      )

      if step_id in visited:
        continue

      visited.add(
        step_id
      )

      print(
        "depth=",
        depth,
        "path=",
        ".".join(
          str(
            part
          )
          for part in path
        ),
        "|",
        describe_step(
          step
        ),
      )

      for child_index, premise in enumerate(
        step.premises
      ):
        queue.append(
          (
            premise,
            depth + 1,
            path
            + (
              child_index,
            ),
          )
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
  print("VISIBLE BODY ORDER")
  print("=" * 96)

  interesting = (
    r"$\eta_{6}=E\eta_{5}$ である.",
    "[R5]より",
    r"$H\left(\nu'\eta_{6}\right)",
  )

  for index, paragraph in enumerate(
    body.split(
      "\n\n"
    )
  ):
    if any(
      token in paragraph
      for token in interesting
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
