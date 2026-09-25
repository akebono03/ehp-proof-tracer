from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
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


def _presentation(n, k, max_depth=3):
  report = build_standard_toda_report(n=n, k=k)
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=max_depth,
  )
  return build_toda_group_proof_presentation(replay)


def _step_label(step):
  rule = step.inference_rule
  if rule is not None:
    return rule.name
  return type(step.conclusion).__name__


def main():
  for n, k in ((3, 3), (5, 3), (8, 7), (9, 7)):
    presentation = _presentation(n, k)
    sidecar = build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
    blocks = build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
    arguments = build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=sidecar,
    )
    block_number = {
      id(block): index + 1
      for index, block in enumerate(blocks)
    }

    print("=" * 78)
    print(f"pi_(n+k)^n: n={n}, k={k}, blocks={len(blocks)}, arguments={len(arguments)}")
    print("-" * 78)
    for argument_index, argument in enumerate(arguments, start=1):
      supports = ", ".join(
        f"B{block_number[id(block)]:02d}:{block.role.value}"
        for block in argument.supporting_blocks
      )
      conclusion = argument.conclusion_block
      conclusion_number = block_number[id(conclusion)]
      print(
        f"A{argument_index:02d} {argument.role.value} -> "
        f"B{conclusion_number:02d}:{conclusion.role.value}"
      )
      print(f"  support_count={len(argument.supporting_blocks)}")
      print(f"  supports={supports or '(none)'}")
      print("  conclusion_steps:")
      for step in conclusion.steps:
        print(f"    - {_step_label(step)}")
    print()


if __name__ == "__main__":
  main()
