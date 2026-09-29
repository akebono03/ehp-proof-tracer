from collections import Counter
from dataclasses import dataclass
from enum import Enum

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_aggregate_statement_catalog import (
  is_toda_group_proof_aggregate_statement,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_provenance_catalog import (
  is_toda_group_proof_narrative_provenance_only_statement,
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

TARGETS = ((3, 3), (5, 3), (4, 6), (5, 7), (8, 7), (9, 7))


class ArchitectureCandidate(Enum):
  EVIDENCE_FIRST = "evidence_first"
  ARGUMENT_FIRST = "argument_first"


class ArchitectureDecision(Enum):
  ACCEPT = "accept"
  REJECT = "reject"


@dataclass(frozen=True)
class ArchitectureCriterion:
  name: str
  evidence_first: ArchitectureDecision
  argument_first: ArchitectureDecision
  reason: str


@dataclass(frozen=True)
class ArchitectureAuditSummary:
  group_count: int
  argument_count: int
  supporting_block_count: int
  child_argument_edge_count: int
  semantic_only_support_count: int
  other_provider_count: int
  aggregate_other_provider_count: int
  provenance_only_other_provider_count: int
  unresolved_other_provider_count: int
  local_body_boundary_violations: int


def build_context(n, k):
  report = build_standard_toda_report(n=n, k=k)
  group_result = report.candidates[0].source_candidate.group_result
  provenance = extract_toda_recursive_proof_provenance(group_result)
  max_depth = max(node.shortest_depth for node in provenance.nodes)
  replay = build_toda_group_result_proof_replay(group_result, max_depth=max_depth)
  presentation = build_toda_group_proof_presentation(replay)
  semantic_sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )
  return presentation, semantic_sidecar, blocks, arguments


def _direct_provider_ids(presentation, semantic_sidecar, conclusion_block):
  conclusion_ids = {id(step) for step in conclusion_block.steps}
  presentation_ids = {
    id(edge.premise_step)
    for edge in presentation.edges
    if id(edge.parent_step) in conclusion_ids
  }
  semantic_ids = {
    id(item.prerequisite_step)
    for item in semantic_sidecar.dependency_semantics
    if id(item.dependent_step) in conclusion_ids
  }
  return presentation_ids, semantic_ids


def _other_direct_provider_statements(
  presentation,
  argument,
):
  conclusion_ids = {id(step) for step in argument.conclusion_block.steps}
  direct_steps = tuple(
    edge.premise_step
    for edge in presentation.edges
    if id(edge.parent_step) in conclusion_ids
  )
  result = []
  seen = set()

  for block in argument.supporting_blocks:
    if block.role is not TodaGroupProofNarrativeMathematicalBlockRole.OTHER:
      continue
    block_ids = {id(step) for step in block.steps}
    for step in direct_steps:
      if id(step) not in block_ids or id(step) in seen:
        continue
      seen.add(id(step))
      result.append(step.conclusion)

  return tuple(result)


def audit_architecture_inputs():
  argument_count = 0
  supporting_block_count = 0
  child_argument_edge_count = 0
  semantic_only_support_count = 0
  other_provider_count = 0
  aggregate_other_provider_count = 0
  provenance_only_other_provider_count = 0
  unresolved_other_provider_count = 0
  local_body_boundary_violations = 0

  for n, k in TARGETS:
    presentation, semantic_sidecar, blocks, arguments = build_context(n, k)
    argument_count += len(arguments)

    for argument_index, argument in enumerate(arguments):
      supporting_block_count += len(argument.supporting_blocks)
      child_argument_edge_count += len(argument.child_argument_indices)
      presentation_ids, semantic_ids = _direct_provider_ids(
        presentation,
        semantic_sidecar,
        argument.conclusion_block,
      )

      for block in argument.supporting_blocks:
        block_ids = {id(step) for step in block.steps}
        presentation_matches = block_ids & presentation_ids
        semantic_matches = block_ids & semantic_ids
        if not presentation_matches and semantic_matches:
          semantic_only_support_count += 1

      for statement in _other_direct_provider_statements(
        presentation,
        argument,
      ):
        other_provider_count += 1
        aggregate = is_toda_group_proof_aggregate_statement(statement)
        provenance_only = (
          is_toda_group_proof_narrative_provenance_only_statement(statement)
        )
        if aggregate:
          aggregate_other_provider_count += 1
        if provenance_only:
          provenance_only_other_provider_count += 1
        if not aggregate and not provenance_only:
          unresolved_other_provider_count += 1

      local_body = (
        extract_toda_group_proof_narrative_argument_local_body_blocks(
          presentation,
          blocks,
          semantic_sidecar,
          arguments,
          argument_index,
        )
      )
      local_body_ids = {id(block) for block in local_body}
      for other_index, other_argument in enumerate(arguments):
        if other_index == argument_index:
          continue
        if id(other_argument.conclusion_block) in local_body_ids:
          local_body_boundary_violations += 1

  return ArchitectureAuditSummary(
    group_count=len(TARGETS),
    argument_count=argument_count,
    supporting_block_count=supporting_block_count,
    child_argument_edge_count=child_argument_edge_count,
    semantic_only_support_count=semantic_only_support_count,
    other_provider_count=other_provider_count,
    aggregate_other_provider_count=aggregate_other_provider_count,
    provenance_only_other_provider_count=provenance_only_other_provider_count,
    unresolved_other_provider_count=unresolved_other_provider_count,
    local_body_boundary_violations=local_body_boundary_violations,
  )


def architecture_criteria(summary):
  return (
    ArchitectureCriterion(
      name="argument_boundary_is_existing_production_structure",
      evidence_first=ArchitectureDecision.REJECT,
      argument_first=ArchitectureDecision.ACCEPT,
      reason=(
        "NarrativeArgument already owns supporting_blocks and "
        "child_argument_indices, and local-body traversal stops at other "
        "Argument conclusions."
      ),
    ),
    ArchitectureCriterion(
      name="semantic_only_support_must_survive",
      evidence_first=ArchitectureDecision.REJECT,
      argument_first=ArchitectureDecision.ACCEPT,
      reason=(
        f"{summary.semantic_only_support_count} direct supports are semantic-only; "
        "raw presentation-edge evidence cannot be the sole skeleton."
      ),
    ),
    ArchitectureCriterion(
      name="child_argument_composition_must_be_first_class",
      evidence_first=ArchitectureDecision.REJECT,
      argument_first=ArchitectureDecision.ACCEPT,
      reason=(
        f"{summary.child_argument_edge_count} child-Argument dependencies exist "
        "across the six representative groups."
      ),
    ),
    ArchitectureCriterion(
      name="other_role_does_not_require_new_mathematical_role",
      evidence_first=ArchitectureDecision.REJECT,
      argument_first=ArchitectureDecision.ACCEPT,
      reason=(
        f"All {summary.other_provider_count} OTHER direct providers are explained "
        "by aggregate/provenance-only semantic catalogs."
      ),
    ),
    ArchitectureCriterion(
      name="recursive_evidence_closure_must_not_define_narrative_scope",
      evidence_first=ArchitectureDecision.REJECT,
      argument_first=ArchitectureDecision.ACCEPT,
      reason=(
        "Argument local-body traversal provides an explicit boundary at other "
        "Argument conclusions; unrestricted evidence closure does not."
      ),
    ),
  )


def decide_architecture(summary):
  criteria = architecture_criteria(summary)
  evidence_first_accepts = all(
    criterion.evidence_first is ArchitectureDecision.ACCEPT
    for criterion in criteria
  )
  argument_first_accepts = all(
    criterion.argument_first is ArchitectureDecision.ACCEPT
    for criterion in criteria
  )

  if evidence_first_accepts:
    raise AssertionError("evidence-first unexpectedly satisfies all criteria")
  if not argument_first_accepts:
    raise AssertionError("argument-first does not satisfy all criteria")
  if summary.unresolved_other_provider_count != 0:
    raise AssertionError("unresolved OTHER provider remains")
  if summary.local_body_boundary_violations != 0:
    raise AssertionError("Argument local-body boundary violation remains")

  return ArchitectureCandidate.ARGUMENT_FIRST


def print_audit():
  summary = audit_architecture_inputs()
  criteria = architecture_criteria(summary)
  decision = decide_architecture(summary)

  print("=" * 78)
  print("Phase 144-6-R5-17E production ProofChain architecture decision audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nRepresentative population")
  print("-" * 78)
  print(f"groups: {summary.group_count}")
  print(f"arguments: {summary.argument_count}")
  print(f"supporting blocks: {summary.supporting_block_count}")
  print(f"child-Argument edges: {summary.child_argument_edge_count}")
  print(f"semantic-only supports: {summary.semantic_only_support_count}")
  print(f"OTHER direct providers: {summary.other_provider_count}")
  print(f"  aggregate: {summary.aggregate_other_provider_count}")
  print(f"  provenance-only: {summary.provenance_only_other_provider_count}")
  print(f"  unresolved: {summary.unresolved_other_provider_count}")
  print(f"local-body boundary violations: {summary.local_body_boundary_violations}")

  print("\\nArchitecture criteria")
  print("-" * 78)
  for criterion in criteria:
    print(criterion.name)
    print(f"  evidence_first={criterion.evidence_first.value}")
    print(f"  argument_first={criterion.argument_first.value}")
    print(f"  reason={criterion.reason}")

  print("\\nDecision")
  print("-" * 78)
  print(f"selected architecture: {decision.value}")
  print(
    "Production direction: NarrativeArgument + semantic providers -> "
    "ProofChain -> Narrative."
  )
  print(
    "EvidenceContribution remains supporting annotation/classification data; "
    "it must not become the top-level Narrative skeleton."
  )
  print(
    "ProofChain must preserve supporting-block and child-Argument boundaries, "
    "and must retain aggregate/provenance-only semantic axes without inventing "
    "new mathematical block roles."
  )

  print("\\nImplementation boundary")
  print("-" * 78)
  print("17E adds no production ProofChain class and changes no renderer.")
  print(
    "The next implementation phase may introduce the minimal production "
    "ProofChain representation from this accepted Argument-first architecture."
  )


if __name__ == "__main__":
  print_audit()
