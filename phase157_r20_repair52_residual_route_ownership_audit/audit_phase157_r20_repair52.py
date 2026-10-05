from __future__ import annotations

import inspect
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

from proof import (
  Relation,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
  _append_narrative_for_step,
  _append_phase134_11_pi8_5_fact,
  _phase134_24_render_pi15_8_narrative,
  _render_phase134_9_pi8_5_narrative_markdown,
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


TARGETS = (
  (3, 1, "pi_4^3"),
  (5, 3, "pi_8^5"),
  (8, 7, "pi_15^8"),
)


def build_data(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
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

  return (
    raw,
    presentation,
    rendered,
  )


def rule_name(
  step,
) -> str | None:
  rule = step.inference_rule
  return (
    None
    if rule is None
    else rule.name
  )


def print_pi4_3(
  presentation,
  rendered: str,
) -> None:
  print("")
  print("pi_4^3 ownership")
  print("-" * 96)

  root = presentation.root_step
  root_rendered = (
    _render_generic_narrative_step(
      root
    )
  )

  print(
    "root rendered:",
    repr(
      root_rendered
    ),
  )
  print(
    "root rule:",
    repr(
      rule_name(
        root
      )
    ),
  )
  print(
    "root occurrences:",
    rendered.count(
      root_rendered
    )
    if root_rendered
    else 0,
  )

  print("")
  print(
    "visible reflexive-looking steps:"
  )

  found = False

  for node in presentation.nodes:
    step = node.proof_step
    step_rendered = (
      _render_generic_narrative_step(
        step
      )
    )

    if not step_rendered:
      continue

    if (
      r"\eta_{3} = \eta_{3}"
      not in step_rendered
      and r"\eta_{3}=\eta_{3}"
      not in step_rendered
    ):
      continue

    found = True
    print(
      "  type=",
      type(
        step.conclusion
      ).__name__,
    )
    print(
      "  rule=",
      repr(
        rule_name(
          step
        )
      ),
    )
    print(
      "  rendered=",
      repr(
        step_rendered
      ),
    )
    print(
      "  premise count=",
      len(
        step.premises
      ),
    )
    print(
      "  conclusion repr=",
      repr(
        step.conclusion
      ),
    )

    if isinstance(
      step.conclusion,
      Relation,
    ):
      print(
        "  lhs==rhs:",
        step.conclusion.lhs
        == step.conclusion.rhs,
      )

  if not found:
    print(
      "  no matching presentation step found"
    )

  print("")
  print(
    "legacy renderer owner:",
    _append_narrative_for_step.__name__,
  )


def print_pi8_5(
  presentation,
  rendered: str,
) -> None:
  print("")
  print("pi_8^5 ownership")
  print("-" * 96)

  paragraphs = tuple(
    paragraph.strip()
    for paragraph in rendered.split(
      "\n\n"
    )
    if paragraph.strip()
  )

  for index, paragraph in enumerate(
    paragraphs
  ):
    if paragraph == "を得る.":
      before = (
        paragraphs[
          index - 1
        ]
        if index > 0
        else ""
      )
      after = (
        paragraphs[
          index + 1
        ]
        if index + 1
        < len(
          paragraphs
        )
        else ""
      )
      print(
        "fragment paragraph:",
        index,
      )
      print(
        "  before:",
        repr(
          before
        ),
      )
      print(
        "  fragment:",
        repr(
          paragraph
        ),
      )
      print(
        "  after:",
        repr(
          after
        ),
      )

  source = inspect.getsource(
    _append_phase134_11_pi8_5_fact
  )

  print("")
  print(
    "dedicated route:",
    _render_phase134_9_pi8_5_narrative_markdown.__name__,
  )
  print(
    "fact renderer:",
    _append_phase134_11_pi8_5_fact.__name__,
  )
  print(
    "explicit root fragment source:",
    '"を得る."' in source,
  )


def print_pi15_8(
  presentation,
  rendered: str,
) -> None:
  print("")
  print("pi_15^8 ownership")
  print("-" * 96)

  paragraphs = tuple(
    paragraph.strip()
    for paragraph in rendered.split(
      "\n\n"
    )
    if paragraph.strip()
  )

  for index, paragraph in enumerate(
    paragraphs
  ):
    if paragraph not in {
      "である.",
      "を得る.",
    }:
      continue

    before = (
      paragraphs[
        index - 1
      ]
      if index > 0
      else ""
    )
    after = (
      paragraphs[
        index + 1
      ]
      if index + 1
      < len(
        paragraphs
      )
      else ""
    )

    print(
      "fragment paragraph:",
      index,
    )
    print(
      "  before:",
      repr(
        before
      ),
    )
    print(
      "  fragment:",
      repr(
        paragraph
      ),
    )
    print(
      "  after:",
      repr(
        after
      ),
    )

  source = inspect.getsource(
    _phase134_24_render_pi15_8_narrative
  )

  print("")
  print(
    "dedicated route:",
    _phase134_24_render_pi15_8_narrative.__name__,
  )
  print(
    "explicit 'である.' source:",
    '"である."' in source,
  )
  print(
    "explicit 'を得る.' source:",
    '"を得る."' in source,
  )


def main() -> int:
  print("=" * 96)
  print("Phase157-R20 repair52 - residual route ownership audit")
  print("=" * 96)
  print("Production code changes: none")
  print("pytest: not run")

  for n, k, label in TARGETS:
    (
      raw,
      presentation,
      rendered,
    ) = build_data(
      n,
      k,
    )

    if label == "pi_4^3":
      print_pi4_3(
        presentation,
        rendered,
      )
    elif label == "pi_8^5":
      print_pi8_5(
        presentation,
        rendered,
      )
    elif label == "pi_15^8":
      print_pi15_8(
        presentation,
        rendered,
      )

  print("")
  print("AUDIT COMPLETE")
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
