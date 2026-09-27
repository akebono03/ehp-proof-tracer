from collections import defaultdict
from dataclasses import dataclass

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_aggregate_semantics import (
  build_toda_group_proof_narrative_aggregate_semantic_sidecar,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
  build_toda_group_proof_narrative_arguments,
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
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_proof_dependency import extract_toda_recursive_proof_provenance


TARGET = (3, 3)


@dataclass(frozen=True)
class ChainEdge:
  parent_step_id: int
  premise_step_id: int
  parent_role: str
  premise_role: str
  contribution: str
  premise_statement_type: str


@dataclass(frozen=True)
class ArgumentChainAudit:
  argument_index: int
  argument_role: str
  conclusion_statement_type: str
  conclusion_block_role: str
  supporting_block_roles: tuple[str, ...]
  child_argument_indices: tuple[int, ...]
  direct_presentation_edge_count: int
  reached_step_count: int
  edge_count: int
  unresolved_edge_count: int
  contribution_counts: tuple[tuple[str, int], ...]
  role_counts: tuple[tuple[str, int], ...]
  edges: tuple[ChainEdge, ...]


def build_context(n=3, k=3):
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
  aggregate_sidecar = (
    build_toda_group_proof_narrative_aggregate_semantic_sidecar(
      presentation
    )
  )
  contributions = (
    build_toda_group_proof_narrative_evidence_contribution_sidecar(
      presentation,
      blocks,
      aggregate_semantic_sidecar=aggregate_sidecar,
    )
  )
  return presentation, blocks, arguments, contributions


def audit_argument_chain(
  presentation,
  blocks,
  arguments,
  contributions,
  argument_index,
):
  argument = arguments[argument_index]
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(argument)
  )
  if conclusion_step is None:
    raise ValueError(
      f"argument {argument_index} has no unique conclusion step"
    )

  block_by_step_id = {
    id(step): block
    for block in blocks
    for step in block.steps
  }
  edges_by_parent_id = defaultdict(list)
  for edge in presentation.edges:
    edges_by_parent_id[id(edge.parent_step)].append(edge)

  contribution_by_edge_key = {
    (
      id(semantic.edge.parent_step),
      id(semantic.edge.premise_step),
      semantic.edge.premise_index,
    ): semantic.contribution
    for semantic in contributions.edge_semantics
  }

  conclusion_step_id = id(conclusion_step)
  direct_presentation_edge_count = len(
    edges_by_parent_id[conclusion_step_id]
  )

  pending = [conclusion_step]
  reached_step_ids = set()
  audited_edges = []

  while pending:
    parent_step = pending.pop()
    parent_id = id(parent_step)
    if parent_id in reached_step_ids:
      continue
    reached_step_ids.add(parent_id)

    for edge in edges_by_parent_id[parent_id]:
      premise_step = edge.premise_step
      premise_id = id(premise_step)
      contribution = contribution_by_edge_key[
        (parent_id, premise_id, edge.premise_index)
      ]
      audited_edges.append(
        ChainEdge(
          parent_step_id=parent_id,
          premise_step_id=premise_id,
          parent_role=block_by_step_id[parent_id].role.value,
          premise_role=block_by_step_id[premise_id].role.value,
          contribution=contribution.value,
          premise_statement_type=type(premise_step.conclusion).__name__,
        )
      )
      if premise_id not in reached_step_ids:
        pending.append(premise_step)

  contribution_counts = defaultdict(int)
  role_counts = defaultdict(int)
  unresolved_edge_count = 0
  for edge in audited_edges:
    contribution_counts[edge.contribution] += 1
    role_counts[edge.premise_role] += 1
    if (
      edge.contribution
      == TodaGroupProofNarrativeEvidenceContribution.UNRESOLVED.value
    ):
      unresolved_edge_count += 1

  return ArgumentChainAudit(
    argument_index=argument_index,
    argument_role=argument.role.value,
    conclusion_statement_type=type(conclusion_step.conclusion).__name__,
    conclusion_block_role=argument.conclusion_block.role.value,
    supporting_block_roles=tuple(
      block.role.value
      for block in argument.supporting_blocks
    ),
    child_argument_indices=argument.child_argument_indices,
    direct_presentation_edge_count=direct_presentation_edge_count,
    reached_step_count=len(reached_step_ids),
    edge_count=len(audited_edges),
    unresolved_edge_count=unresolved_edge_count,
    contribution_counts=tuple(sorted(contribution_counts.items())),
    role_counts=tuple(sorted(role_counts.items())),
    edges=tuple(audited_edges),
  )


def audit_pi6_3():
  presentation, blocks, arguments, contributions = build_context(*TARGET)
  return tuple(
    audit_argument_chain(
      presentation,
      blocks,
      arguments,
      contributions,
      argument_index,
    )
    for argument_index in range(len(arguments))
  )


def _print_audit(audits):
  print("=" * 78)
  print("Phase 144-6-R5-17A-R1 Narrative proof-chain selection diagnostic")
  print("target: pi_6^3")
  print("policy: reverse traversal from each Argument conclusion; no depth cutoff")
  print("=" * 78)

  for audit in audits:
    print()
    print(
      f"A{audit.argument_index + 1:02d} "
      f"role={audit.argument_role} "
      f"conclusion={audit.conclusion_statement_type}"
    )
    print(
      f"conclusion_block_role={audit.conclusion_block_role} "
      f"direct_presentation_edges={audit.direct_presentation_edge_count}"
    )
    print(
      "supporting_block_roles="
      + (
        ", ".join(audit.supporting_block_roles)
        if audit.supporting_block_roles
        else "(none)"
      )
    )
    print(
      "child_argument_indices="
      + (
        ", ".join(str(index) for index in audit.child_argument_indices)
        if audit.child_argument_indices
        else "(none)"
      )
    )
    print(
      f"reached_steps={audit.reached_step_count} "
      f"edges={audit.edge_count} "
      f"unresolved_edges={audit.unresolved_edge_count}"
    )
    if audit.direct_presentation_edge_count == 0:
      print(
        "diagnostic: conclusion step has no direct presentation edge; "
        "do not infer that the Argument has no Narrative support."
      )
    print("contributions:")
    for contribution, count in audit.contribution_counts:
      print(f"  {count:4d}  {contribution}")
    print("premise roles:")
    for role, count in audit.role_counts:
      print(f"  {count:4d}  {role}")
    print("chain edges:")
    for index, edge in enumerate(audit.edges, start=1):
      print(
        f"  E{index:03d} "
        f"{edge.parent_role} <- {edge.premise_role} "
        f"[{edge.contribution}] "
        f"{edge.premise_statement_type}"
      )


if __name__ == "__main__":
  _print_audit(audit_pi6_3())
