from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


for n, k in (
  (3, 3),
  (5, 3),
  (8, 7),
  (9, 7),
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  print("=" * 78)
  print(
    f"n={n}, k={k}"
  )

  for argument_index, argument in enumerate(
    arguments
  ):
    body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )

    block_index_by_identity = {
      id(
        block
      ): index
      for index, block in enumerate(
        blocks
      )
    }

    labels = tuple(
      "B"
      + f"{block_index_by_identity[id(block)] + 1:02d}"
      + ":"
      + block.role.value
      for block in body_blocks
    )
    exactness_count = sum(
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
      for block in body_blocks
    )
    conclusion_count = sum(
      block is argument.conclusion_block
      for block in body_blocks
    )

    print(
      f"A{argument_index + 1:02d} "
      f"{argument.role.value}: "
      f"blocks={len(body_blocks)} "
      f"exactness={exactness_count} "
      f"conclusion_count={conclusion_count} "
      f"conclusion_last="
      f"{body_blocks[-1] is argument.conclusion_block}"
    )
    print(
      "  "
      + " -> ".join(
        labels
      )
    )
