from collections import Counter, defaultdict
from dataclasses import fields, is_dataclass

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_aggregate_statement_catalog import (
  is_toda_group_proof_aggregate_statement,
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
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_proof_dependency import extract_toda_recursive_proof_provenance
from toda_rules import TodaEtaFamilyDefinitionStatement


TARGETS = ((3, 3), (5, 3), (4, 6), (5, 7), (8, 7), (9, 7))

FIELD_CAPABILITIES = {
  "ambient_group": "GROUP",
  "source_group": "GROUP",
  "target_group": "GROUP",
  "image_group": "GROUP",
  "transported_group": "GROUP",
  "map": "MAP",
  "subobject_map": "MAP",
  "iterated_suspension_map": "MAP",
  "source_generator": "GENERATOR",
  "image_generator": "GENERATOR",
  "first_generator_image": "GENERATOR",
  "second_generator_image": "GENERATOR",
  "quotient_order": "ORDER",
  "target_order": "ORDER",
  "definition_relation": "RELATION",
  "hopf_relation": "RELATION",
  "suspension_relation": "RELATION",
  "double_suspension_relation": "RELATION",
}


def _context(n, k):
  report = build_standard_toda_report(n=n, k=k)
  group_result = report.candidates[0].source_candidate.group_result
  provenance = extract_toda_recursive_proof_provenance(group_result)
  max_depth = max(node.shortest_depth for node in provenance.nodes)
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=max_depth,
  )
  presentation = build_toda_group_proof_presentation(replay)
  semantic_sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )
  contributions = build_toda_group_proof_narrative_evidence_contribution_sidecar(
    presentation,
    blocks,
  )
  return presentation, semantic_sidecar, blocks, arguments, contributions


def _block_by_step_id(blocks):
  return {
    id(step): block
    for block in blocks
    for step in block.steps
  }


def _visible_argument_indices_by_step_id(
  presentation,
  semantic_sidecar,
  blocks,
  arguments,
):
  result = defaultdict(set)

  for argument_index, argument in enumerate(arguments):
    local_body = extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
    hidden_ids = set(
      _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        blocks,
        local_body,
        semantic_sidecar,
        argument,
      )
    )

    if argument.role is not TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION:
      hidden_ids.update(
        id(step)
        for block in local_body
        for step in block.steps
        if isinstance(step.conclusion, TodaEtaFamilyDefinitionStatement)
      )

    for block in local_body:
      for step in block.steps:
        if id(step) not in hidden_ids:
          result[id(step)].add(argument_index)

  return result


def _argument_indices_by_conclusion_step_id(arguments):
  result = defaultdict(set)
  for argument_index, argument in enumerate(arguments):
    for step in argument.conclusion_block.steps:
      result[id(step)].add(argument_index)
  return result


def _capability_signature(statement):
  if not is_dataclass(statement):
    return ()

  counts = Counter()
  for field in fields(statement):
    capability = FIELD_CAPABILITIES.get(field.name)
    if capability is not None:
      counts[capability] += 1

  return tuple(sorted(counts.items()))


def _candidate_statement_semantic(signature):
  capabilities = dict(signature)

  group_count = capabilities.get("GROUP", 0)
  map_count = capabilities.get("MAP", 0)
  generator_count = capabilities.get("GENERATOR", 0)
  order_count = capabilities.get("ORDER", 0)
  relation_count = capabilities.get("RELATION", 0)

  if relation_count >= 2:
    return "RELATION_AGGREGATE"

  if (
    group_count >= 1
    and map_count >= 1
    and generator_count >= 1
  ):
    return "MAP_TRANSPORT"

  if (
    group_count >= 1
    and generator_count >= 1
  ):
    return "GROUP_DECOMPOSITION_TRANSPORT"

  if (
    group_count >= 1
    and map_count >= 1
    and order_count >= 1
  ):
    return "GROUP_ORDER_TRANSPORT"

  return "UNCLASSIFIED"


def main():
  print("=" * 118)
  print("Phase 144-6-R5-15S aggregate semantic metadata design audit")
  print("=" * 118)
  print("Audit only. Candidate semantic names are diagnostic, not production API.")

  rows = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      contributions,
    ) = _context(n, k)

    block_by_step_id = _block_by_step_id(blocks)
    visible_args = _visible_argument_indices_by_step_id(
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
    )
    conclusion_args = _argument_indices_by_conclusion_step_id(arguments)

    for semantic in contributions.edge_semantics:
      if (
        semantic.contribution
        is not TodaGroupProofNarrativeEvidenceContribution.UNRESOLVED
      ):
        continue

      premise_id = id(semantic.edge.premise_step)
      parent_id = id(semantic.edge.parent_step)
      consumer_argument_indices = conclusion_args[parent_id]

      if not (
        visible_args[premise_id]
        & consumer_argument_indices
      ):
        continue

      statement = semantic.edge.premise_step.conclusion
      signature = _capability_signature(statement)

      rows.append(
        {
          "target": (n, k),
          "premise_type": type(statement).__name__,
          "premise_role": block_by_step_id[premise_id].role.value,
          "consumer_type": type(semantic.edge.parent_step.conclusion).__name__,
          "consumer_role": block_by_step_id[parent_id].role.value,
          "argument_roles": tuple(
            sorted(
              arguments[index].role.value
              for index in consumer_argument_indices
            )
          ),
          "aggregate_catalog": is_toda_group_proof_aggregate_statement(
            statement
          ),
          "signature": signature,
          "candidate_semantic": _candidate_statement_semantic(signature),
        }
      )

  print()
  print(f"remaining_edge_local_visible_unresolved={len(rows)}")

  print()
  print("EDGE DESIGN INVENTORY")
  print("-" * 118)
  for index, row in enumerate(rows, start=1):
    print(
      f"{index:2d}. target={row['target']} "
      f"premise={row['premise_type']} [{row['premise_role']}] "
      f"consumer={row['consumer_type']} [{row['consumer_role']}]"
    )
    print(
      f"    argument_roles={row['argument_roles']} "
      f"aggregate_catalog={row['aggregate_catalog']}"
    )
    print(
      f"    capability={row['signature']} "
      f"candidate_statement_semantic={row['candidate_semantic']}"
    )

  print()
  print("CANDIDATE STATEMENT SEMANTICS")
  print("-" * 118)
  candidate_counts = Counter(
    row["candidate_semantic"]
    for row in rows
  )
  for key, count in candidate_counts.most_common():
    print(f"{key:<40} {count:5d}")

  print()
  print("AGGREGATE CATALOG COVERAGE")
  print("-" * 118)
  catalog_counts = Counter(
    row["aggregate_catalog"]
    for row in rows
  )
  for key, count in catalog_counts.items():
    print(f"aggregate_catalog={str(key):<5} {count:5d}")

  print()
  print("SAME STATEMENT SEMANTIC x DIFFERENT CONSUMER PURPOSE")
  print("-" * 118)
  purposes_by_semantic = defaultdict(set)
  for row in rows:
    purposes_by_semantic[row["candidate_semantic"]].add(
      (
        row["consumer_role"],
        row["argument_roles"],
      )
    )
  for semantic_name, purposes in sorted(purposes_by_semantic.items()):
    print(f"{semantic_name}:")
    for purpose in sorted(purposes, key=repr):
      print(f"  {purpose}")

  print()
  print("DESIGN OPTION COMPARISON")
  print("-" * 118)
  print(
    "A. Extend MathematicalBlockRole only"
  )
  print(
    "   Granularity: step display role. "
    "Problem: statement meaning and edge contribution remain conflated."
  )
  print(
    "B. Extend existing Narrative StepSemanticRole"
  )
  print(
    "   Granularity: proof step. Reuses validated sidecar architecture. "
    "Problem: current StepSemanticRole describes Narrative function "
    "(definition introduction), not reusable mathematical aggregate meaning."
  )
  print(
    "C. Add explicit aggregate statement semantic metadata sidecar"
  )
  print(
    "   Granularity: proof step/statement meaning. Keeps mathematical "
    "aggregate meaning separate from consumer-specific edge contribution."
  )
  print(
    "D. Put semantic kind on EvidenceContribution edge only"
  )
  print(
    "   Granularity: premise edge. Problem: the same premise meaning is "
    "duplicated across consumers and cannot independently drive block/rendering semantics."
  )

  print()
  print("DESIGN INVARIANTS")
  print("-" * 118)
  print(
    "1. Statement semantic metadata must describe what the premise means, "
    "not what a particular consumer uses it for."
  )
  print(
    "2. EvidenceContribution remains edge-specific and may depend on both "
    "statement semantic metadata and consumer/Argument purpose."
  )
  print(
    "3. Generic block role remains a presentation grouping vocabulary; "
    "it should not be forced to encode every aggregate theorem kind."
  )
  print(
    "4. Existing aggregate catalog membership is not sufficient semantic metadata."
  )
  print(
    "5. Field-shape inference in this audit is diagnostic only; production "
    "metadata should be explicit and typed."
  )
  print(
    "6. No n/k-specific rule or inference-rule-name parsing is needed by the design."
  )

  print()
  print("MINIMAL PROTOTYPE RECOMMENDATION")
  print("-" * 118)
  print(
    "Storage: a separate Narrative aggregate-statement semantic sidecar, "
    "validated against presentation proof steps."
  )
  print(
    "First semantic vocabulary to prototype from the 9-edge population:"
  )
  print(
    "  GROUP_ORDER_TRANSPORT"
  )
  print(
    "  MAP_TRANSPORT"
  )
  print(
    "  GROUP_DECOMPOSITION_TRANSPORT"
  )
  print(
    "  RELATION_AGGREGATE"
  )
  print(
    "Do not yet modify EvidenceContribution or MathematicalBlockRole."
  )
  print(
    "Next prototype should test whether these explicit statement semantics, "
    "combined with consumer role/Argument purpose, can classify the 9 edges "
    "without statement-class branching."
  )


if __name__ == "__main__":
  main()
