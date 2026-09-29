from collections import Counter
from dataclasses import dataclass
from enum import Enum

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_aggregate_semantics import (
  build_toda_group_proof_narrative_aggregate_semantic_sidecar,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_evidence_contributions import (
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


TARGET = (3, 3)


class AuditEdgeKind(Enum):
  PRESENTATION = "presentation"
  SUPPORTING_BLOCK = "supporting_block"
  CHILD_ARGUMENT = "child_argument"


@dataclass(frozen=True)
class AuditEdge:
  kind: AuditEdgeKind
  consumer_argument_index: int
  consumer_role: str
  provider_role: str
  provider_statement_types: tuple[str, ...]
  contribution: str | None
  child_argument_index: int | None = None


@dataclass(frozen=True)
class ArgumentSupportAudit:
  argument_index: int
  argument_role: str
  conclusion_block_role: str
  conclusion_statement_type: str
  presentation_edges: tuple[AuditEdge, ...]
  supporting_block_edges: tuple[AuditEdge, ...]
  child_argument_edges: tuple[AuditEdge, ...]

  @property
  def all_edges(self):
    return (
      self.presentation_edges
      + self.supporting_block_edges
      + self.child_argument_edges
    )


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


def _statement_types(block):
  return tuple(
    type(step.conclusion).__name__
    for step in block.steps
  )


def audit_argument_support_edges(
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
  contribution_by_edge_key = {
    (
      id(semantic.edge.parent_step),
      id(semantic.edge.premise_step),
      semantic.edge.premise_index,
    ): semantic.contribution.value
    for semantic in contributions.edge_semantics
  }

  presentation_edges = []
  for edge in presentation.edges:
    if edge.parent_step is not conclusion_step:
      continue
    premise_block = block_by_step_id[id(edge.premise_step)]
    presentation_edges.append(
      AuditEdge(
        kind=AuditEdgeKind.PRESENTATION,
        consumer_argument_index=argument_index,
        consumer_role=argument.conclusion_block.role.value,
        provider_role=premise_block.role.value,
        provider_statement_types=(
          type(edge.premise_step.conclusion).__name__,
        ),
        contribution=contribution_by_edge_key[
          (
            id(edge.parent_step),
            id(edge.premise_step),
            edge.premise_index,
          )
        ],
      )
    )

  supporting_block_edges = tuple(
    AuditEdge(
      kind=AuditEdgeKind.SUPPORTING_BLOCK,
      consumer_argument_index=argument_index,
      consumer_role=argument.conclusion_block.role.value,
      provider_role=block.role.value,
      provider_statement_types=_statement_types(block),
      contribution=None,
    )
    for block in argument.supporting_blocks
  )

  child_argument_edges = tuple(
    AuditEdge(
      kind=AuditEdgeKind.CHILD_ARGUMENT,
      consumer_argument_index=argument_index,
      consumer_role=argument.conclusion_block.role.value,
      provider_role=arguments[child_index].role.value,
      provider_statement_types=_statement_types(
        arguments[child_index].conclusion_block
      ),
      contribution=None,
      child_argument_index=child_index,
    )
    for child_index in argument.child_argument_indices
  )

  return ArgumentSupportAudit(
    argument_index=argument_index,
    argument_role=argument.role.value,
    conclusion_block_role=argument.conclusion_block.role.value,
    conclusion_statement_type=type(conclusion_step.conclusion).__name__,
    presentation_edges=tuple(presentation_edges),
    supporting_block_edges=supporting_block_edges,
    child_argument_edges=child_argument_edges,
  )


def audit_pi6_3():
  presentation, blocks, arguments, contributions = build_context(*TARGET)
  return tuple(
    audit_argument_support_edges(
      presentation,
      blocks,
      arguments,
      contributions,
      argument_index,
    )
    for argument_index in range(len(arguments))
  )


def _print_edge(edge):
  extra = ""
  if edge.contribution is not None:
    extra += f" contribution={edge.contribution}"
  if edge.child_argument_index is not None:
    extra += f" child=A{edge.child_argument_index + 1:02d}"
  statements = ", ".join(edge.provider_statement_types)
  print(
    f"    {edge.kind.value}: "
    f"{edge.consumer_role} <- {edge.provider_role}"
    f"{extra} statements=[{statements}]"
  )


def print_audit(audits):
  print("=" * 78)
  print("Phase 144-6-R5-17A-R2 Argument support edge integration audit")
  print("target: pi_6^3")
  print(
    "edge kinds: presentation + supporting_block + child_argument "
    "(audit-only; no production ProofChain)"
  )
  print("=" * 78)

  total_counts = Counter()

  for audit in audits:
    print()
    print(
      f"A{audit.argument_index + 1:02d} "
      f"role={audit.argument_role} "
      f"conclusion_block={audit.conclusion_block_role} "
      f"conclusion={audit.conclusion_statement_type}"
    )
    print(
      "  counts: "
      f"presentation={len(audit.presentation_edges)} "
      f"supporting_block={len(audit.supporting_block_edges)} "
      f"child_argument={len(audit.child_argument_edges)}"
    )

    for edge in audit.all_edges:
      total_counts[edge.kind.value] += 1
      _print_edge(edge)

  print()
  print("Summary")
  print("-" * 78)
  for kind in AuditEdgeKind:
    print(f"{kind.value}: {total_counts[kind.value]}")

  a03 = audits[2]
  print()
  print("A03 definition support")
  print("-" * 78)
  print(
    "presentation edge absent: "
    f"{len(a03.presentation_edges) == 0}"
  )
  print(
    "supporting block roles: "
    + ", ".join(
      edge.provider_role
      for edge in a03.supporting_block_edges
    )
  )

  a01 = audits[0]
  print()
  print("A01 child Argument support")
  print("-" * 78)
  print(
    "child Arguments: "
    + ", ".join(
      (
        f"A{edge.child_argument_index + 1:02d}:"
        f"{edge.provider_role}"
      )
      for edge in a01.child_argument_edges
    )
  )


if __name__ == "__main__":
  print_audit(audit_pi6_3())
