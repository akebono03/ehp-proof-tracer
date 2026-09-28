from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
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


def build_arguments(
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
  return build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )


def source_index_by_argument_identity(
  source,
  argument,
):
  for index, candidate in enumerate(
    source
  ):
    if candidate is argument:
      return index
  return None


def source_index_by_conclusion_identity(
  source,
  argument,
):
  for index, candidate in enumerate(
    source
  ):
    if (
      candidate.conclusion_block
      is argument.conclusion_block
    ):
      return index
  return None


def main():
  source = build_arguments(
    9,
    7,
  )
  ordered = (
    order_toda_group_proof_narrative_arguments(
      source
    )
  )

  print(
    "pi_16^9 compact argument-ordering diagnosis"
  )
  print("=" * 72)
  print(
    f"source_count={len(source)}"
  )
  print(
    f"ordered_count={len(ordered)}"
  )

  print()
  print("SOURCE")
  for index, argument in enumerate(
    source
  ):
    print(
      f"{index}: "
      f"role={argument.role.value} "
      f"conclusion={argument.conclusion_block.role.value} "
      f"children={argument.child_argument_indices}"
    )

  print()
  print("ORDERED")

  argument_identity_indices = []
  conclusion_identity_indices = []

  for position, argument in enumerate(
    ordered
  ):
    argument_source_index = (
      source_index_by_argument_identity(
        source,
        argument,
      )
    )
    conclusion_source_index = (
      source_index_by_conclusion_identity(
        source,
        argument,
      )
    )

    argument_identity_indices.append(
      argument_source_index
    )
    conclusion_identity_indices.append(
      conclusion_source_index
    )

    print(
      f"{position}: "
      f"arg_source={argument_source_index} "
      f"conclusion_source={conclusion_source_index} "
      f"role={argument.role.value} "
      f"conclusion={argument.conclusion_block.role.value} "
      f"children={argument.child_argument_indices}"
    )

  argument_identity_indices = tuple(
    argument_identity_indices
  )
  conclusion_identity_indices = tuple(
    conclusion_identity_indices
  )

  print()
  print("SUMMARY")
  print(
    "ordered_argument_identity_indices="
    f"{argument_identity_indices}"
  )
  print(
    "ordered_conclusion_identity_indices="
    f"{conclusion_identity_indices}"
  )
  print(
    "expected=(1, 0)"
  )

  if (
    conclusion_identity_indices
    == (
      1,
      0,
    )
  ):
    print(
      "RESULT=ORDERING_CONTRACT_MATCH"
    )
  else:
    print(
      "RESULT=ORDERING_CONTRACT_MISMATCH"
    )


if __name__ == "__main__":
  main()
