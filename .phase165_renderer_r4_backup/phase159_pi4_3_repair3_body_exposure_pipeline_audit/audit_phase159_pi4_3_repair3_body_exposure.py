from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      ROOT
    ),
  )

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
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
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)


KEYWORDS = (
  "DeltaImage",
  "SuspensionKernel",
  "Surjective",
  "Exactness",
  "pi_{3}^{2}",
  "pi_{4}^{5}",
  "2\\eta_{2}",
  "quotient",
)


def step_summary(
  proof_step,
) -> str:
  statement = proof_step.conclusion
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
    or ""
  )
  rule = getattr(
    getattr(
      proof_step,
      "inference_rule",
      None,
    ),
    "name",
    None,
  )

  return (
    type(
      statement
    ).__name__
    + " | rule="
    + repr(
      rule
    )
    + " | "
    + rendered
  )


def is_interesting(
  proof_step,
) -> bool:
  summary = step_summary(
    proof_step
  )

  return any(
    keyword in summary
    for keyword in KEYWORDS
  )


def print_interesting_nodes(
  title: str,
  presentation,
) -> None:
  print()
  print(
    "===",
    title,
    "===",
  )
  print(
    "node count:",
    len(
      presentation.nodes
    ),
  )

  count = 0

  for node in presentation.nodes:
    proof_step = node.proof_step

    if not is_interesting(
      proof_step
    ):
      continue

    count += 1
    print(
      f"[{count}]",
      step_summary(
        proof_step
      ),
    )
    print(
      "    step_id=",
      id(
        proof_step
      ),
      "depth=",
      getattr(
        node,
        "depth",
        None,
      ),
      "premises=",
      len(
        proof_step.premises
      ),
    )

  print(
    "interesting count:",
    count,
  )


def main() -> int:
  report = build_standard_toda_report(
    n=3,
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
  raw_presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  closure_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      closure_presentation
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      closure_presentation
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      closure_presentation,
      blocks,
      semantic_sidecar,
    )
  )
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      closure_presentation,
      semantic_sidecar,
      arguments,
    )
  )
  ordered_contributions = (
    build_toda_group_proof_narrative_ordered_contributions(
      closure_presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
    )
  )

  print(
    "=== Phase159 pi_4^3 repair3 body exposure pipeline audit ==="
  )
  print(
    "Production code changes: NONE"
  )
  print(
    "Existing test changes: NONE"
  )

  print_interesting_nodes(
    "RAW depth=2 presentation",
    raw_presentation,
  )
  print_interesting_nodes(
    "SEMANTIC CLOSURE presentation",
    closure_presentation,
  )

  print()
  print(
    "=== BLOCKS containing interesting steps ==="
  )

  for block_index, block in enumerate(
    blocks
  ):
    interesting = tuple(
      step
      for step in block.steps
      if is_interesting(
        step
      )
    )

    if not interesting:
      continue

    print(
      "block",
      block_index,
      "role=",
      getattr(
        block,
        "role",
        None,
      ),
    )

    for step in interesting:
      print(
        "   ",
        step_summary(
          step
        ),
      )

  print()
  print(
    "=== ARGUMENT LOCAL BODY ==="
  )

  for argument_index, argument in enumerate(
    arguments
  ):
    local_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        closure_presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )

    print(
      "argument",
      argument_index,
      "local_block_count=",
      len(
        local_blocks
      ),
    )

    for block in local_blocks:
      for step in block.steps:
        if not is_interesting(
          step
        ):
          continue

        print(
          "   ",
          step_summary(
            step
          ),
        )

  print()
  print(
    "=== ORDERED CONTRIBUTIONS ==="
  )

  for argument_index, contributions in enumerate(
    ordered_contributions
  ):
    print(
      "argument",
      argument_index,
      "contribution_count=",
      len(
        contributions
      ),
    )

    for contribution in contributions:
      step = contribution.proof_step

      if not is_interesting(
        step
      ):
        continue

      print(
        "   placement=",
        getattr(
          contribution,
          "placement",
          None,
        ),
        "|",
        step_summary(
          step
        ),
      )

  print()
  print(
    "=== PUBLIC NARRATIVE ==="
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      raw_presentation
    )
  )
  print(
    rendered
  )

  probes = (
    (
      "direct Delta",
      r"\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}",
    ),
    (
      "image Delta",
      r"\operatorname{Im}",
    ),
    (
      "kernel E",
      r"\ker E",
    ),
    (
      "pi3_2",
      r"\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}",
    ),
    (
      "pi4_5_zero",
      r"\pi_{4}^{5} = 0",
    ),
    (
      "E surjective",
      "は全射",
    ),
    (
      "quotient",
      "/",
    ),
  )

  print()
  print(
    "=== PUBLIC PROBES ==="
  )

  for label, probe in probes:
    print(
      label,
      "=>",
      probe in rendered,
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
