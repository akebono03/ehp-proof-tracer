from collections import Counter, defaultdict
from dataclasses import fields, is_dataclass

from toda_calculation_facade import build_standard_toda_report
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
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
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

SEMANTIC_FIELD_NAMES = {
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
  "bridge_relation": "RELATION",
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


def _argument_visibility(
  presentation,
  semantic_sidecar,
  blocks,
  arguments,
):
  visible_args_by_step_id = defaultdict(set)
  hidden_args_by_step_id = defaultdict(set)

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
        if id(step) in hidden_ids:
          hidden_args_by_step_id[id(step)].add(argument_index)
        else:
          visible_args_by_step_id[id(step)].add(argument_index)

  return visible_args_by_step_id, hidden_args_by_step_id


def _argument_indices_by_conclusion_step_id(arguments):
  result = defaultdict(set)
  for argument_index, argument in enumerate(arguments):
    for step in argument.conclusion_block.steps:
      result[id(step)].add(argument_index)
  return result


def _semantic_field_inventory(statement):
  if not is_dataclass(statement):
    return ()

  result = []
  for field in fields(statement):
    value = getattr(statement, field.name)
    semantic_kind = SEMANTIC_FIELD_NAMES.get(field.name, "UNCLASSIFIED")
    result.append(
      (
        field.name,
        type(value).__name__,
        semantic_kind,
      )
    )
  return tuple(result)


def _semantic_capability_signature(statement):
  inventory = _semantic_field_inventory(statement)
  kinds = Counter(
    semantic_kind
    for _name, _type_name, semantic_kind in inventory
    if semantic_kind != "UNCLASSIFIED"
  )
  return tuple(sorted(kinds.items()))


def _consumer_argument_roles(arguments, indices):
  return tuple(
    sorted(
      arguments[index].role.value
      for index in indices
    )
  )


def main():
  print("=" * 122)
  print("Phase 144-6-R5-15R remaining 9 edge semantic structure audit")
  print("=" * 122)
  print(
    "Audit only. Statement class names select the 15Q population; "
    "candidate semantics are derived from typed fields and edge context."
  )

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
    visible_args_by_step_id, _hidden_args_by_step_id = _argument_visibility(
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

      premise_step_id = id(semantic.edge.premise_step)
      parent_step_id = id(semantic.edge.parent_step)
      consumer_argument_indices = conclusion_args[parent_step_id]

      if not (
        visible_args_by_step_id[premise_step_id]
        & consumer_argument_indices
      ):
        continue

      premise_statement = semantic.edge.premise_step.conclusion
      consumer_statement = semantic.edge.parent_step.conclusion
      premise_block = block_by_step_id[premise_step_id]
      consumer_block = block_by_step_id[parent_step_id]
      inventory = _semantic_field_inventory(premise_statement)
      capability = _semantic_capability_signature(premise_statement)

      rows.append(
        {
          "target": (n, k),
          "premise_type": type(premise_statement).__name__,
          "premise_role": premise_block.role.value,
          "consumer_type": type(consumer_statement).__name__,
          "consumer_role": consumer_block.role.value,
          "argument_roles": _consumer_argument_roles(
            arguments,
            consumer_argument_indices,
          ),
          "inventory": inventory,
          "capability": capability,
        }
      )

  print()
  print(f"edge_local_visible_unresolved_edges={len(rows)}")

  for index, row in enumerate(rows, start=1):
    print()
    print("-" * 122)
    print(
      f"EDGE {index}: target={row['target']} "
      f"premise={row['premise_type']} [{row['premise_role']}] "
      f"-> consumer={row['consumer_type']} [{row['consumer_role']}]"
    )
    print(f"consumer_argument_roles={row['argument_roles']}")
    print(f"semantic_capability_signature={row['capability']}")
    print("typed_fields:")
    for field_name, type_name, semantic_kind in row["inventory"]:
      print(
        f"  {field_name:<32} {type_name:<44} {semantic_kind}"
      )

  print()
  print("=" * 122)
  print("CAPABILITY SIGNATURES")
  print("=" * 122)
  capability_counts = Counter(row["capability"] for row in rows)
  for capability, count in capability_counts.most_common():
    print(f"{count:4d} x {capability}")

  print()
  print("=" * 122)
  print("CONSUMER ROLE x ARGUMENT ROLE")
  print("=" * 122)
  consumer_argument_counts = Counter(
    (
      row["consumer_role"],
      row["argument_roles"],
    )
    for row in rows
  )
  for key, count in consumer_argument_counts.most_common():
    print(
      f"{count:4d} x consumer_role={key[0]:<18} "
      f"argument_roles={key[1]}"
    )

  print()
  print("=" * 122)
  print("FIELD-KIND COVERAGE")
  print("=" * 122)
  field_kind_counts = Counter()
  for row in rows:
    for _field_name, _type_name, semantic_kind in row["inventory"]:
      if semantic_kind != "UNCLASSIFIED":
        field_kind_counts[semantic_kind] += 1
  for semantic_kind, count in field_kind_counts.most_common():
    print(f"{semantic_kind:<20} {count:5d}")

  print()
  print("=" * 122)
  print("AUDIT QUESTIONS FOR 15S")
  print("=" * 122)
  print(
    "1. Can GROUP+MAP+ORDER be represented by generic quotient/order/map "
    "semantics without naming a Toda statement class?"
  )
  print(
    "2. Can GROUP+MAP+GENERATOR represent a generic isomorphism/transport "
    "provider, or is an explicit typed relation kind still missing?"
  )
  print(
    "3. Can RELATION-rich theorem aggregates be decomposed into existing "
    "generic relation/definition contributions rather than assigning one "
    "coarse contribution to the aggregate statement?"
  )
  print(
    "4. Does consumer TARGET versus DEFINITION require different edge "
    "contributions even when the premise typed structure is identical?"
  )
  print(
    "5. Do not promote a field-name heuristic directly into production. "
    "If the audit shows a stable concept, introduce an explicit typed "
    "semantic object or metadata in a later implementation."
  )


if __name__ == "__main__":
  main()
