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
  visible_argument_indices_by_step_id = defaultdict(set)
  hidden_argument_indices_by_step_id = defaultdict(set)
  local_argument_indices_by_step_id = defaultdict(set)

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
        step_id = id(step)
        local_argument_indices_by_step_id[step_id].add(argument_index)
        if step_id in hidden_ids:
          hidden_argument_indices_by_step_id[step_id].add(argument_index)
        else:
          visible_argument_indices_by_step_id[step_id].add(argument_index)

  return (
    visible_argument_indices_by_step_id,
    hidden_argument_indices_by_step_id,
    local_argument_indices_by_step_id,
  )


def _argument_indices_by_conclusion_step_id(arguments):
  result = defaultdict(set)
  for argument_index, argument in enumerate(arguments):
    for step in argument.conclusion_block.steps:
      result[id(step)].add(argument_index)
  return result


def _field_signature(statement):
  if not is_dataclass(statement):
    return ("<not-dataclass>",)
  return tuple(
    (field.name, type(getattr(statement, field.name)).__name__)
    for field in fields(statement)
  )


def main():
  print("=" * 118)
  print("Phase 144-6-R5-15Q remaining visible unresolved edge audit")
  print("=" * 118)
  print("Audit only. No production contribution or visibility rule is changed.")

  global_rows = []
  statement_types = Counter()
  consumer_types = Counter()
  role_pairs = Counter()
  edge_locality = Counter()
  signatures = Counter()

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      contributions,
    ) = _context(n, k)

    block_by_step_id = _block_by_step_id(blocks)
    (
      visible_args_by_step_id,
      hidden_args_by_step_id,
      local_args_by_step_id,
    ) = _argument_visibility(
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
    )
    argument_indices_by_conclusion_step_id = (
      _argument_indices_by_conclusion_step_id(arguments)
    )

    target_rows = []

    for semantic in contributions.edge_semantics:
      if (
        semantic.contribution
        is not TodaGroupProofNarrativeEvidenceContribution.UNRESOLVED
      ):
        continue

      premise_step_id = id(semantic.edge.premise_step)
      if not visible_args_by_step_id[premise_step_id]:
        continue

      parent_step_id = id(semantic.edge.parent_step)
      premise_statement = semantic.edge.premise_step.conclusion
      consumer_statement = semantic.edge.parent_step.conclusion
      premise_block = block_by_step_id[premise_step_id]
      consumer_block = block_by_step_id[parent_step_id]

      consumer_argument_indices = (
        argument_indices_by_conclusion_step_id[parent_step_id]
      )
      same_argument_visible = bool(
        visible_args_by_step_id[premise_step_id]
        & consumer_argument_indices
      )
      same_argument_hidden = bool(
        hidden_args_by_step_id[premise_step_id]
        & consumer_argument_indices
      )
      same_argument_local = bool(
        local_args_by_step_id[premise_step_id]
        & consumer_argument_indices
      )

      if same_argument_visible:
        locality = "EDGE_LOCAL_VISIBLE"
      elif same_argument_hidden:
        locality = "EDGE_LOCAL_HIDDEN"
      elif same_argument_local:
        locality = "EDGE_LOCAL_OTHER"
      elif consumer_argument_indices:
        locality = "CONSUMER_ARGUMENT_NO_PREMISE_LOCAL"
      else:
        locality = "CONSUMER_NOT_ARGUMENT_CONCLUSION"

      row = (
        n,
        k,
        type(premise_statement).__name__,
        premise_block.role.value,
        type(consumer_statement).__name__,
        consumer_block.role.value,
        locality,
        _field_signature(premise_statement),
      )
      target_rows.append(row)
      global_rows.append(row)

      statement_types[type(premise_statement).__name__] += 1
      consumer_types[type(consumer_statement).__name__] += 1
      role_pairs[
        (
          premise_block.role.value,
          consumer_block.role.value,
        )
      ] += 1
      edge_locality[locality] += 1
      signatures[
        (
          type(premise_statement).__name__,
          _field_signature(premise_statement),
        )
      ] += 1

    print()
    print(f"TARGET ({n}, {k})")
    print("-" * 118)
    print(f"step_global_visible_unresolved_edges={len(target_rows)}")
    print("edge_locality:")
    local_counter = Counter(row[6] for row in target_rows)
    for key, count in local_counter.most_common():
      print(f"  {key:<40} {count:5d}")
    print("statement_types:")
    local_statements = Counter(row[2] for row in target_rows)
    for key, count in local_statements.most_common():
      print(f"  {key:<72} {count:5d}")
    print("premise_role -> consumer_role:")
    local_pairs = Counter((row[3], row[5]) for row in target_rows)
    for key, count in local_pairs.most_common():
      print(f"  {key[0]:<20} -> {key[1]:<20} {count:5d}")

  print()
  print("=" * 118)
  print("GLOBAL")
  print("=" * 118)
  print(f"step_global_visible_unresolved_edges={len(global_rows)}")

  print()
  print("EDGE LOCALITY")
  print("-" * 118)
  for key, count in edge_locality.most_common():
    print(f"{key:<44} {count:6d}")

  print()
  print("PREMISE STATEMENT TYPES")
  print("-" * 118)
  for key, count in statement_types.most_common():
    print(f"{key:<78} {count:6d}")

  print()
  print("PREMISE ROLE -> CONSUMER ROLE")
  print("-" * 118)
  for key, count in role_pairs.most_common():
    print(f"{key[0]:<22} -> {key[1]:<22} {count:6d}")

  print()
  print("CONSUMER STATEMENT TYPES")
  print("-" * 118)
  for key, count in consumer_types.most_common(30):
    print(f"{key:<78} {count:6d}")

  print()
  print("PREMISE FIELD SIGNATURES")
  print("-" * 118)
  for key, count in signatures.most_common(30):
    statement_type, signature = key
    print(f"{count:6d} x {statement_type}")
    print(f"         {signature}")

  print()
  print("EDGE-LOCAL VISIBLE DETAILS")
  print("-" * 118)
  edge_local_visible_rows = [
    row
    for row in global_rows
    if row[6] == "EDGE_LOCAL_VISIBLE"
  ]
  print(f"edge_local_visible_unresolved_edges={len(edge_local_visible_rows)}")
  detail_counter = Counter(
    (
      row[2],
      row[3],
      row[4],
      row[5],
    )
    for row in edge_local_visible_rows
  )
  for key, count in detail_counter.most_common():
    print(
      f"{count:5d} x premise={key[0]} [{key[1]}] "
      f"-> consumer={key[2]} [{key[3]}]"
    )

  print()
  print("INTERPRETATION GUIDE")
  print("-" * 118)
  print(
    "EDGE_LOCAL_VISIBLE: premise is visible inside an Argument whose conclusion "
    "is this edge's consumer; strongest candidate for a real contribution gap."
  )
  print(
    "EDGE_LOCAL_HIDDEN: the same consumer Argument explicitly hides the premise; "
    "step-global 15P counting overstates this edge's Narrative relevance."
  )
  print(
    "CONSUMER_ARGUMENT_NO_PREMISE_LOCAL: premise is visible somewhere else, "
    "but not in the consumer Argument local body; this is step-global overcount."
  )
  print(
    "CONSUMER_NOT_ARGUMENT_CONCLUSION: consumer is not itself an Argument "
    "conclusion; inspect ownership before adding vocabulary."
  )


if __name__ == "__main__":
  main()
