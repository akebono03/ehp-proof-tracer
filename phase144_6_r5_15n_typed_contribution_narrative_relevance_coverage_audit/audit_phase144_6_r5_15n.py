from collections import Counter, defaultdict

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
  extract_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
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
  TodaEtaFamilyDefinitionStatement,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


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
    extract_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar,
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


def _production_visibility_by_step_id(
  presentation,
  semantic_sidecar,
  blocks,
  arguments,
):
  local_occurrences = Counter()
  visible_occurrences = Counter()
  hidden_occurrences = Counter()

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
        local_occurrences[
          step_id
        ] += 1

        if step_id in hidden_step_ids:
          hidden_occurrences[
            step_id
          ] += 1
        else:
          visible_occurrences[
            step_id
          ] += 1

  visibility = {}

  for node in presentation.nodes:
    step_id = id(
      node.proof_step
    )

    if visible_occurrences[
      step_id
    ]:
      visibility[
        step_id
      ] = "VISIBLE"
    elif hidden_occurrences[
      step_id
    ]:
      visibility[
        step_id
      ] = "HIDDEN"
    else:
      visibility[
        step_id
      ] = "OUTSIDE_LOCAL_BODY"

  return visibility


def _statement_type_name(
  statement,
):
  return type(
    statement
  ).__name__


def _print_matrix(
  title,
  matrix,
):
  print()
  print(title)
  print("-" * 118)
  print(
    f"{'contribution':<24}"
    f"{'VISIBLE':>12}"
    f"{'HIDDEN':>12}"
    f"{'OUTSIDE':>12}"
    f"{'TOTAL':>12}"
    f"{'visible_ratio':>18}"
  )

  for contribution in (
    TodaGroupProofNarrativeEvidenceContribution
  ):
    row = matrix[
      contribution.value
    ]
    total = sum(
      row.values()
    )
    visible = row[
      "VISIBLE"
    ]
    ratio = (
      0.0
      if total == 0
      else visible / total
    )

    print(
      f"{contribution.value:<24}"
      f"{visible:>12}"
      f"{row['HIDDEN']:>12}"
      f"{row['OUTSIDE_LOCAL_BODY']:>12}"
      f"{total:>12}"
      f"{ratio:>18.6f}"
    )


def main():
  print("=" * 118)
  print("Phase 144-6-R5-15N typed contribution x Narrative relevance coverage audit")
  print("=" * 118)
  print(
    "Audit only. Production R4 visibility is observed, not changed."
  )

  global_matrix = defaultdict(
    Counter
  )
  global_visible_unresolved_types = Counter()
  global_hidden_unresolved_types = Counter()
  global_visible_resolved = 0
  global_visible_unresolved = 0

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

    visibility_by_step_id = (
      _production_visibility_by_step_id(
        presentation,
        semantic_sidecar,
        blocks,
        arguments,
      )
    )

    target_matrix = defaultdict(
      Counter
    )
    visible_unresolved_types = Counter()

    for semantic in (
      contribution_sidecar.edge_semantics
    ):
      visibility = (
        visibility_by_step_id[
          id(
            semantic.edge.premise_step
          )
        ]
      )
      contribution = (
        semantic.contribution.value
      )

      target_matrix[
        contribution
      ][
        visibility
      ] += 1
      global_matrix[
        contribution
      ][
        visibility
      ] += 1

      if (
        semantic.contribution
        is TodaGroupProofNarrativeEvidenceContribution
        .UNRESOLVED
      ):
        statement_type = (
          _statement_type_name(
            semantic.edge.premise_step.conclusion
          )
        )

        if visibility == "VISIBLE":
          visible_unresolved_types[
            statement_type
          ] += 1
          global_visible_unresolved_types[
            statement_type
          ] += 1
          global_visible_unresolved += 1
        elif visibility == "HIDDEN":
          global_hidden_unresolved_types[
            statement_type
          ] += 1
      elif visibility == "VISIBLE":
        global_visible_resolved += 1

    print()
    print(
      f"TARGET ({n}, {k}) "
      f"edges={len(presentation.edges)} "
      f"arguments={len(arguments)}"
    )
    _print_matrix(
      "Contribution x production visibility",
      target_matrix,
    )

    visible_total = sum(
      row[
        "VISIBLE"
      ]
      for row in target_matrix.values()
    )
    visible_unresolved = target_matrix[
      "unresolved"
    ][
      "VISIBLE"
    ]
    visible_resolved = (
      visible_total
      - visible_unresolved
    )
    visible_resolution_ratio = (
      0.0
      if visible_total == 0
      else visible_resolved / visible_total
    )

    print()
    print(
      f"visible_edges={visible_total}"
    )
    print(
      f"visible_resolved_edges={visible_resolved}"
    )
    print(
      f"visible_unresolved_edges={visible_unresolved}"
    )
    print(
      "visible_resolution_ratio="
      f"{visible_resolution_ratio:.6f}"
    )

    if visible_unresolved_types:
      print(
        "visible_unresolved_statement_types:"
      )
      for name, count in (
        visible_unresolved_types.most_common()
      ):
        print(
          f"  {name:<64} {count:5d}"
        )

  print()
  print("=" * 118)
  print("GLOBAL")
  print("=" * 118)
  _print_matrix(
    "Contribution x production visibility",
    global_matrix,
  )

  visible_total = (
    global_visible_resolved
    + global_visible_unresolved
  )
  visible_resolution_ratio = (
    0.0
    if visible_total == 0
    else (
      global_visible_resolved
      / visible_total
    )
  )

  print()
  print(
    f"visible_edges={visible_total}"
  )
  print(
    "visible_resolved_edges="
    f"{global_visible_resolved}"
  )
  print(
    "visible_unresolved_edges="
    f"{global_visible_unresolved}"
  )
  print(
    "visible_resolution_ratio="
    f"{visible_resolution_ratio:.6f}"
  )

  print()
  print(
    "GLOBAL VISIBLE x UNRESOLVED statement types"
  )
  print("-" * 118)
  for name, count in (
    global_visible_unresolved_types.most_common()
  ):
    print(
      f"{name:<80} {count:6d}"
    )

  print()
  print(
    "GLOBAL HIDDEN x UNRESOLVED statement types"
  )
  print("-" * 118)
  for name, count in (
    global_hidden_unresolved_types.most_common()
  ):
    print(
      f"{name:<80} {count:6d}"
    )

  print()
  print("INTERPRETATION")
  print("-" * 118)
  print(
    "1. Overall 15M resolution ratio is not the primary metric."
  )
  print(
    "2. The primary metric is visible_resolution_ratio: "
    "how much production-visible Narrative evidence already has "
    "typed contribution metadata."
  )
  print(
    "3. VISIBLE x UNRESOLVED is the exact next semantic-extension "
    "population; hidden unresolved edges should not be generalized "
    "merely to improve a global percentage."
  )
  print(
    "4. This audit does not change R4 visibility and does not infer "
    "contribution from n/k or inference-rule names."
  )
  print(
    "5. Statement type names are printed only to inventory unresolved "
    "populations; they are not used to classify any edge."
  )


if __name__ == "__main__":
  main()
