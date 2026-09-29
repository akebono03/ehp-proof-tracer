from toda_group_proof_narrative_argument_body import (
  extract_toda_group_proof_narrative_argument_body_blocks,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_primary_exactness_component,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
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
    relevant_groups = (
      extract_toda_group_proof_narrative_argument_relevant_groups(
        presentation,
        blocks,
        argument,
      )
    )
    evidence = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    components = (
      build_toda_group_proof_narrative_exactness_method_components(
        evidence
      )
    )
    primary_component = (
      select_toda_group_proof_narrative_primary_exactness_component(
        relevant_groups,
        components,
      )
    )
    body_blocks = (
      extract_toda_group_proof_narrative_argument_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
        primary_component,
      )
    )
    conclusion_count = sum(
      block is argument.conclusion_block
      for block in body_blocks
    )

    print(
      f"A{argument_index + 1:02d} "
      f"{argument.role.value}: "
      f"body={len(body_blocks)} "
      f"conclusion_count={conclusion_count} "
      f"conclusion_last="
      f"{body_blocks[-1] is argument.conclusion_block}"
    )

    if (
      conclusion_count != 1
      or body_blocks[
        -1
      ]
      is not argument.conclusion_block
    ):
      raise AssertionError(
        "argument conclusion must appear "
        "exactly once at the end"
      )
