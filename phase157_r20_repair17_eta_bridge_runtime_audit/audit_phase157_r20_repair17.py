from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(0, str(REPOSITORY_ROOT))

import toda_group_proof_narrative_contribution_renderer as renderer

from toda_calculation_facade import (
  build_standard_toda_report,
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


original_bridge = (
  renderer
  .insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges
)

bridge_calls = 0


def print_eta_paragraphs(label, markdown):
  print("")
  print("=" * 88)
  print(label)
  print("=" * 88)

  found = False

  for index, paragraph in enumerate(
    markdown.split(
      "\n\n"
    )
  ):
    if (
      r"\eta_{5}" in paragraph
      or r"\eta_{6}" in paragraph
      or r"H\left(\nu'\eta_{6}\right)" in paragraph
    ):
      found = True
      print(
        f"[{index}] {paragraph}"
      )

  if not found:
    print("(none)")


def traced_bridge(
  presentation,
  markdown,
):
  global bridge_calls
  bridge_calls += 1

  print_eta_paragraphs(
    "BRIDGE INPUT "
    + str(
      bridge_calls
    ),
    markdown,
  )

  result = original_bridge(
    presentation,
    markdown,
  )

  print_eta_paragraphs(
    "BRIDGE OUTPUT "
    + str(
      bridge_calls
    ),
    result,
  )

  return result


def print_equation57_nodes(
  presentation,
):
  print("")
  print("=" * 88)
  print("EQUATION 5.7 CANDIDATES")
  print("=" * 88)

  found = False

  for index, node in enumerate(
    presentation.nodes
  ):
    step = node.proof_step
    rule_name = (
      None
      if step.inference_rule is None
      else step.inference_rule.name
    )

    if (
      rule_name
      != "Toda Equation 5.7 nu-prime eta_6 Hopf value"
    ):
      continue

    found = True

    print(
      "node",
      index,
      "step id=",
      id(
        step
      ),
      "premises=",
      len(
        step.premises
      ),
    )

    for premise_index, premise in enumerate(
      step.premises
    ):
      conclusion = premise.conclusion

      print(
        "  premise",
        premise_index,
        "type=",
        type(
          conclusion
        ).__name__,
        "id=",
        id(
          premise
        ),
        "rule=",
        (
          None
          if premise.inference_rule is None
          else premise.inference_rule.name
        ),
      )

      if type(
        conclusion
      ).__name__ == "TodaEtaFamilyDefinitionStatement":
        print(
          "    index=",
          conclusion.index,
        )
        print(
          "    element=",
          conclusion.element,
        )

  if not found:
    print("(none)")


def print_eta_definition_nodes(
  presentation,
):
  print("")
  print("=" * 88)
  print("ETA DEFINITION NODES")
  print("=" * 88)

  for index, node in enumerate(
    presentation.nodes
  ):
    step = node.proof_step
    conclusion = step.conclusion

    if type(
      conclusion
    ).__name__ != "TodaEtaFamilyDefinitionStatement":
      continue

    if conclusion.index not in (
      5,
      6,
    ):
      continue

    print(
      "node",
      index,
      "index=",
      conclusion.index,
      "step id=",
      id(
        step
      ),
    )


def main() -> int:
  renderer.insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges = (
    traced_bridge
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

  print_equation57_nodes(
    presentation
  )
  print_eta_definition_nodes(
    presentation
  )

  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )

  print("")
  print("=" * 88)
  print("FINAL ETA-RELATED PARAGRAPHS")
  print("=" * 88)

  for index, paragraph in enumerate(
    rendered.split(
      "\n\n"
    )
  ):
    if (
      r"\eta_{5}" in paragraph
      or r"\eta_{6}" in paragraph
      or r"H\left(\nu'\eta_{6}\right)" in paragraph
    ):
      print(
        f"[{index}] {paragraph}"
      )

  print("")
  print(
    "bridge calls:",
    bridge_calls,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
