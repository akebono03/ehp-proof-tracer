from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(ROOT),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
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
  r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
)


def _base_presentation():
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
  return build_toda_group_proof_presentation(
    replay
  )


def _render_contribution(
  presentation,
) -> str:
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )

  return (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )


def _print_matches(
  label: str,
  rendered: str,
) -> None:
  print("")
  print("=" * 78)
  print(label)
  print("=" * 78)
  print(
    "target occurrence count:",
    rendered.count(
      TARGET
    ),
  )

  for index, paragraph in enumerate(
    rendered.split(
      "\n\n"
    )
  ):
    if TARGET not in paragraph:
      continue

    print("")
    print(
      f"[paragraph {index}]"
    )
    print(
      paragraph.strip()
    )


def _injective_nodes(
  presentation,
):
  matches = []

  for index, node in enumerate(
    presentation.nodes
  ):
    rendered = str(
      node.proof_step.conclusion
    )

    if (
      "Injective" in type(
        node.proof_step.conclusion
      ).__name__
      and "Suspension" in type(
        node.proof_step.conclusion
      ).__name__
    ):
      matches.append(
        (
          index,
          node.proof_step,
        )
      )

  return tuple(
    matches
  )


def _print_injective_nodes(
  label: str,
  presentation,
) -> None:
  matches = _injective_nodes(
    presentation
  )

  print("")
  print("=" * 78)
  print(label)
  print("=" * 78)
  print(
    "matching SuspensionInjective node count:",
    len(
      matches
    ),
  )

  for index, proof_step in matches:
    conclusion = proof_step.conclusion
    inference_rule = proof_step.inference_rule

    print("")
    print(
      f"[node {index}]"
    )
    print(
      "step id:",
      id(
        proof_step
      ),
    )
    print(
      "conclusion type:",
      type(
        conclusion
      ).__name__,
    )
    print(
      "conclusion:",
      conclusion,
    )
    print(
      "inference rule:",
      (
        inference_rule.name
        if inference_rule is not None
        else None
      ),
    )
    print(
      "premise count:",
      len(
        proof_step.premises
      ),
    )

    for premise_index, premise in enumerate(
      proof_step.premises
    ):
      print(
        f"  premise {premise_index}:",
        type(
          premise.conclusion
        ).__name__,
        premise.conclusion,
      )


def main() -> None:
  base = _base_presentation()
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      base
    )
  )

  _print_injective_nodes(
    "BASE PRESENTATION INJECTIVE NODES",
    base,
  )
  _print_injective_nodes(
    "SEMANTIC CLOSURE PRESENTATION INJECTIVE NODES",
    closure,
  )

  base_rendered = _render_contribution(
    base
  )
  closure_rendered = _render_contribution(
    closure
  )
  public_rendered = (
    render_toda_group_proof_narrative_markdown(
      base
    )
  )

  _print_matches(
    "BASE CONTRIBUTION RENDERER",
    base_rendered,
  )
  _print_matches(
    "SEMANTIC CLOSURE CONTRIBUTION RENDERER",
    closure_rendered,
  )
  _print_matches(
    "FINAL PUBLIC NARRATIVE",
    public_rendered,
  )


if __name__ == "__main__":
  main()
