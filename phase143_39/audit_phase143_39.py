from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_contribution_ownership import (
  filter_toda_group_proof_narrative_exactness_body_contributions,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  extract_toda_group_proof_narrative_exactness_display_contributions,
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

    print(
      f"A{argument_index + 1:02d} "
      f"{argument.role.value}: "
      f"primary="
      f"{primary_component is not None}"
    )

    for block_index, block in enumerate(
      blocks
    ):
      if (
        block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        continue

      contributions = (
        extract_toda_group_proof_narrative_exactness_display_contributions(
          presentation,
          block,
        )
      )
      filtered = (
        filter_toda_group_proof_narrative_exactness_body_contributions(
          block,
          contributions,
          primary_component,
        )
      )

      before = ",".join(
        contribution.kind.value
        for contribution in contributions
      )
      after = ",".join(
        contribution.kind.value
        for contribution in filtered
      )

      print(
        f"  B{block_index + 1:02d}: "
        f"[{before}] -> [{after}]"
      )
