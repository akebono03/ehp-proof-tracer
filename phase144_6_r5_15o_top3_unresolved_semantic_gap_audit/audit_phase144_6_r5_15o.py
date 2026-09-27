from collections import Counter, defaultdict
from dataclasses import fields, is_dataclass

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_evidence_contributions import (
  TodaGroupProofNarrativeEvidenceContribution,
  build_toda_group_proof_narrative_evidence_contribution_sidecar,
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
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)
from toda_rules import (
  TodaBracketMembershipStatement,
  TodaEtaFamilyDefinitionStatement,
  TodaNuFamilyDefinitionStatement,
  TodaProp42ExactnessStatement,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)

TOP3_TYPES = (
  TodaProp42ExactnessStatement,
  TodaNuFamilyDefinitionStatement,
  TodaBracketMembershipStatement,
)

EXPECTED_GENERIC_ROLES = {
  TodaProp42ExactnessStatement: (
    TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
  ),
  TodaNuFamilyDefinitionStatement: (
    TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION
  ),
  TodaBracketMembershipStatement: (
    TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP
  ),
}


def _build_full_context(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  provenance = (
    extract_toda_recursive_proof_provenance(
      group_result
    )
  )
  max_depth = max(
    node.shortest_depth
    for node in provenance.nodes
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=max_depth,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )
  contribution_sidecar = (
    build_toda_group_proof_narrative_evidence_contribution_sidecar(
      presentation,
      blocks,
    )
  )
  return (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    contribution_sidecar,
  )


def _block_role_by_step_id(
  blocks,
):
  result = {}

  for block in blocks:
    for step in block.steps:
      result[
        id(
          step
        )
      ] = block.role

  return result


def _visibility_by_step_id(
  presentation,
  semantic_sidecar,
  blocks,
  arguments,
):
  visible = set()
  hidden = set()

  for argument_index, argument in enumerate(
    arguments
  ):
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )

    hidden_step_ids = set(
      _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        blocks,
        local_body_blocks,
        semantic_sidecar,
        argument,
      )
    )

    if (
      argument.role
      is not TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    ):
      hidden_step_ids.update(
        id(
          proof_step
        )
        for block in local_body_blocks
        for proof_step in block.steps
        if isinstance(
          proof_step.conclusion,
          TodaEtaFamilyDefinitionStatement,
        )
      )

    for block in local_body_blocks:
      for proof_step in block.steps:
        step_id = id(
          proof_step
        )

        if step_id in hidden_step_ids:
          hidden.add(
            step_id
          )
        else:
          visible.add(
            step_id
          )

  result = {}

  for node in presentation.nodes:
    step_id = id(
      node.proof_step
    )

    if step_id in visible:
      result[
        step_id
      ] = "VISIBLE"
    elif step_id in hidden:
      result[
        step_id
      ] = "HIDDEN"
    else:
      result[
        step_id
      ] = "OUTSIDE_LOCAL_BODY"

  return result


def _field_signature(
  statement,
):
  if not is_dataclass(
    statement
  ):
    return (
      "<not-dataclass>",
    )

  return tuple(
    (
      field.name,
      type(
        getattr(
          statement,
          field.name,
        )
      ).__name__,
    )
    for field in fields(
      statement
    )
  )


def main():
  print("=" * 118)
  print("Phase 144-6-R5-15O top-3 unresolved semantic gap audit")
  print("=" * 118)
  print(
    "Audit only. No production classification or visibility is changed."
  )

  global_counts = defaultdict(
    Counter
  )
  global_roles = defaultdict(
    Counter
  )
  global_consumers = defaultdict(
    Counter
  )
  global_field_signatures = defaultdict(
    Counter
  )

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      contribution_sidecar,
    ) = _build_full_context(
      n,
      k,
    )

    block_role_by_step_id = (
      _block_role_by_step_id(
        blocks
      )
    )
    visibility_by_step_id = (
      _visibility_by_step_id(
        presentation,
        semantic_sidecar,
        blocks,
        arguments,
      )
    )

    print()
    print(
      f"TARGET ({n}, {k})"
    )

    for semantic in (
      contribution_sidecar.edge_semantics
    ):
      statement = (
        semantic.edge.premise_step.conclusion
      )

      if not isinstance(
        statement,
        TOP3_TYPES,
      ):
        continue

      statement_type = type(
        statement
      )
      type_name = (
        statement_type.__name__
      )
      visibility = (
        visibility_by_step_id[
          id(
            semantic.edge.premise_step
          )
        ]
      )
      role = (
        block_role_by_step_id[
          id(
            semantic.edge.premise_step
          )
        ].value
      )
      contribution = (
        semantic.contribution.value
      )
      consumer_type = type(
        semantic.edge.parent_step.conclusion
      ).__name__

      global_counts[
        type_name
      ][
        (
          visibility,
          contribution,
        )
      ] += 1
      global_roles[
        type_name
      ][
        role
      ] += 1
      global_consumers[
        type_name
      ][
        consumer_type
      ] += 1
      global_field_signatures[
        type_name
      ][
        _field_signature(
          statement
        )
      ] += 1

    for statement_type in TOP3_TYPES:
      type_name = (
        statement_type.__name__
      )
      local_total = sum(
        count
        for (
          visibility,
          contribution,
        ), count in global_counts[
          type_name
        ].items()
      )
      print(
        f"  cumulative {type_name:<42} "
        f"{local_total:5d}"
      )

  print()
  print("=" * 118)
  print("GLOBAL TOP-3 GAP")
  print("=" * 118)

  projected_visible_resolutions = 0

  for statement_type in TOP3_TYPES:
    type_name = (
      statement_type.__name__
    )
    print()
    print(type_name)
    print("-" * 118)

    expected_role = (
      EXPECTED_GENERIC_ROLES[
        statement_type
      ].value
    )
    print(
      f"expected_generic_block_role={expected_role}"
    )

    print("block_roles:")
    for role, count in (
      global_roles[
        type_name
      ].most_common()
    ):
      print(
        f"  {role:<24} {count:6d}"
      )

    print(
      "visibility_x_current_contribution:"
    )
    for key, count in sorted(
      global_counts[
        type_name
      ].items()
    ):
      visibility, contribution = key
      print(
        f"  {visibility:<20} "
        f"{contribution:<24} "
        f"{count:6d}"
      )

      if (
        visibility == "VISIBLE"
        and contribution
        == TodaGroupProofNarrativeEvidenceContribution
        .UNRESOLVED.value
      ):
        projected_visible_resolutions += (
          count
        )

    print("field_signatures:")
    for signature, count in (
      global_field_signatures[
        type_name
      ].most_common()
    ):
      print(
        f"  {count:6d} x {signature}"
      )

    print("top_consumer_statement_types:")
    for consumer, count in (
      global_consumers[
        type_name
      ].most_common(
        12
      )
    ):
      print(
        f"  {consumer:<72} {count:6d}"
      )

  print()
  print("=" * 118)
  print("PROJECTION")
  print("=" * 118)
  print(
    "top3_visible_unresolved_edges="
    f"{projected_visible_resolutions}"
  )
  print(
    "15N_visible_edges=2698"
  )
  print(
    "15N_visible_resolved_edges=1730"
  )
  projected_resolved = (
    1730
    + projected_visible_resolutions
  )
  print(
    "projected_visible_resolved_edges="
    f"{projected_resolved}"
  )
  print(
    "projected_visible_resolution_ratio="
    f"{projected_resolved / 2698:.6f}"
  )

  print()
  print("INTERPRETATION")
  print("-" * 118)
  print(
    "1. If each top-3 statement population already has one stable generic "
    "block role, the semantic information exists before the 15M mapper."
  )
  print(
    "2. In that case the gap is a mapper-vocabulary gap, not a proof-depth "
    "or statement-shape problem."
  )
  print(
    "3. The next implementation should extend typed EvidenceContribution "
    "from generic block roles, not from n/k or inference-rule names."
  )
  print(
    "4. Statement class names are used here only to select the 15N top-3 "
    "audit population and to print diagnostics; they are not proposed as "
    "production classification rules."
  )


if __name__ == "__main__":
  main()
