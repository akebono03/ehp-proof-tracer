from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
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

  print(
    "=" * 78
  )
  print(
    f"n={n}, k={k}"
  )

  block_index_by_identity = {
    id(
      block
    ): index
    for index, block in enumerate(
      blocks
    )
  }

  for argument_index, argument in enumerate(
    arguments
  ):
    evidence = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )

    labels = tuple(
      "B"
      + str(
        block_index_by_identity[
          id(
            block
          )
        ]
        + 1
      ).zfill(
        2
      )
      + ":"
      + block.role.value
      for block in evidence
    )

    print(
      f"A{argument_index + 1:02d} "
      f"{argument.role.value}: "
      f"{labels}"
    )
