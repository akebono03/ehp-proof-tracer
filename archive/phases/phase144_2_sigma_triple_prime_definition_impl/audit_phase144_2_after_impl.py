from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_argument_discourse import (
  classify_toda_group_proof_narrative_argument_discourse,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_purpose_subject,
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


def main():
  report = build_standard_toda_report(
    n=5,
    k=7,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=sidecar,
    )
  )
  ordered = order_toda_group_proof_narrative_arguments(
    arguments
  )
  discourse = (
    classify_toda_group_proof_narrative_argument_discourse(
      arguments
    )
  )

  print("=" * 78)
  print("Phase 144-2 pi_12^5 argument audit after sigma definition change")
  print("=" * 78)
  print(f"blocks={len(blocks)}")
  print(f"arguments={len(arguments)}")
  print(f"ordered_argument_indices={ordered}")

  for argument_index in ordered:
    argument = arguments[
      argument_index
    ]
    subject = (
      extract_toda_group_proof_narrative_argument_purpose_subject(
        argument
      )
    )
    print("-" * 78)
    print(f"argument_index={argument_index}")
    print(f"role={argument.role.value}")
    print(
      "subject="
      f"{getattr(subject, 'name', subject)!r}"
    )
    print(
      "conclusion_block_role="
      f"{argument.conclusion_block.role.value}"
    )
    print(
      "child_argument_indices="
      f"{argument.child_argument_indices}"
    )
    print(
      "discourse="
      f"{discourse[argument_index].value}"
    )


if __name__ == "__main__":
  main()
