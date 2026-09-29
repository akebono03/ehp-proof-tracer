from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
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


def _primary_component(
  presentation,
  blocks,
  sidecar,
  arguments,
  argument_index,
):
  argument = arguments[
    argument_index
  ]
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
  return (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )


def audit_case(
  n: int,
  k: int,
) -> None:
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  ordered_arguments = (
    order_toda_group_proof_narrative_arguments(
      arguments
    )
  )
  discourse_roles = (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      arguments
    )
  )

  source_index_by_identity = {
    id(
      argument
    ): index
    for index, argument in enumerate(
      arguments
    )
  }
  block_index_by_identity = {
    id(
      block
    ): index
    for index, block in enumerate(
      blocks
    )
  }

  seen_non_exact_block_ids = set()
  seen_exact_contribution_keys = set()

  print("=" * 78)
  print(
    f"n={n}, k={k}"
  )
  print("=" * 78)

  for ordered_position, argument in enumerate(
    ordered_arguments
  ):
    discourse_role = discourse_roles[
      ordered_position
    ]

    if (
      discourse_role
      is TodaGroupProofNarrativeArgumentDiscourseRole
      .DETACHED
    ):
      print(
        f"[Argument {ordered_position + 1}] "
        f"role={argument.role.value}, "
        "discourse=detached -> excluded from main narrative"
      )
      print()
      continue

    argument_index = source_index_by_identity[
      id(
        argument
      )
    ]
    primary_component = _primary_component(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )

    print(
      f"[Argument {ordered_position + 1}] "
      f"source_index={argument_index}, "
      f"role={argument.role.value}, "
      f"discourse={discourse_role.value}, "
      f"primary={primary_component is not None}"
    )

    for block in local_body_blocks:
      block_index = block_index_by_identity[
        id(
          block
        )
      ]

      if (
        block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        status = (
          "SHARED"
          if id(
            block
          ) in seen_non_exact_block_ids
          else "NEW"
        )
        print(
          f"  block B{block_index:02d} "
          f"role={block.role.value}: {status}"
        )
        seen_non_exact_block_ids.add(
          id(
            block
          )
        )
        continue

      contributions = (
        extract_toda_group_proof_narrative_exactness_display_contributions(
          presentation,
          block,
        )
      )
      body_contributions = (
        filter_toda_group_proof_narrative_exactness_body_contributions(
          block,
          contributions,
          primary_component,
        )
      )

      if not body_contributions:
        print(
          f"  block B{block_index:02d} "
          "role=exactness: NO DISPLAY CONTRIBUTION"
        )
        continue

      for contribution in body_contributions:
        key = (
          contribution.kind,
          id(
            contribution.proof_step
          ),
          contribution.latex,
        )
        status = (
          "SHARED"
          if key in seen_exact_contribution_keys
          else "NEW"
        )
        print(
          f"  block B{block_index:02d} "
          f"exactness/{contribution.kind.value}: "
          f"{status}"
        )
        print(
          f"    {contribution.latex}"
        )
        seen_exact_contribution_keys.add(
          key
        )

    print()

  print(
    "SUMMARY "
    f"seen_non_exact_blocks={len(seen_non_exact_block_ids)}, "
    f"seen_exact_contributions={len(seen_exact_contribution_keys)}"
  )
  print()


def main() -> None:
  for n, k in (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ):
    audit_case(
      n,
      k,
    )


if __name__ == "__main__":
  main()
