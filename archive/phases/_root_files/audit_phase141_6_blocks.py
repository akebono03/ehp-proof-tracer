from collections import Counter

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _pi6_3_presentation():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=3,
    )
  )

  return build_toda_group_proof_presentation(
    replay
  )


def _rule_name(
  proof_step,
):
  inference_rule = (
    proof_step.inference_rule
  )

  if inference_rule is None:
    return proof_step.rule.value

  return inference_rule.name


def main():
  presentation = (
    _pi6_3_presentation()
  )

  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )

  print(
    "Phase 141-6 block audit: "
    "pi_6^3, max_depth=3"
  )
  print(
    "=" * 72
  )

  role_counts = Counter(
    block.role.value
    for block in blocks
  )

  step_role_counts = Counter()

  for index, block in enumerate(
    blocks,
    start=1,
  ):
    print(
      f"[{index:02d}] "
      f"{block.role.value} "
      f"({len(block.steps)} step(s))"
    )

    for step_index, proof_step in enumerate(
      block.steps,
      start=1,
    ):
      statement_type = type(
        proof_step.conclusion
      ).__name__

      step_role_counts[
        block.role.value
      ] += 1

      print(
        f"  {step_index}. "
        f"{statement_type}"
      )
      print(
        f"     rule: "
        f"{_rule_name(proof_step)}"
      )
      print(
        f"     conclusion: "
        f"{proof_step.conclusion!r}"
      )

    print()

  print(
    "=" * 72
  )
  print(
    "block counts:"
  )
  for role, count in sorted(
    role_counts.items()
  ):
    print(
      f"  {role}: {count}"
    )

  print(
    "step counts by block role:"
  )
  for role, count in sorted(
    step_role_counts.items()
  ):
    print(
      f"  {role}: {count}"
    )

  print(
    "semantic sidecar:"
  )
  print(
    "  premise semantics: "
    f"{len(sidecar.premise_semantics)}"
  )
  print(
    "  step semantics: "
    f"{len(sidecar.step_semantics)}"
  )

  print(
    "selected presentation nodes: "
    f"{len(presentation.nodes)}"
  )
  print(
    "selected presentation edges: "
    f"{len(presentation.edges)}"
  )


if __name__ == "__main__":
  main()
