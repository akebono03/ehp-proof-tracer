from collections import Counter
from dataclasses import dataclass
from enum import Enum

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
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


class GenericProofChainProviderKind(Enum):
  SUPPORTING_BLOCK = "supporting_block"
  CHILD_ARGUMENT = "child_argument"


@dataclass(frozen=True, order=True)
class GenericProofChainType:
  claim_role: str
  provider_kind: str
  provider_role: str


@dataclass(frozen=True)
class GenericProofChainOccurrence:
  argument_index: int
  argument_role: str
  chain_type: GenericProofChainType
  provider_block_step_count: int
  direct_presentation_match_count: int
  direct_semantic_match_count: int


@dataclass(frozen=True)
class GenericProofChainArgumentAudit:
  argument_index: int
  argument_role: str
  claim_role: str
  occurrences: tuple[GenericProofChainOccurrence, ...]


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
  return presentation, semantic_sidecar, blocks, arguments


def _direct_provider_step_ids(
  presentation,
  semantic_sidecar,
  conclusion_block,
):
  conclusion_step_ids = {
    id(step)
    for step in conclusion_block.steps
  }

  presentation_ids = {
    id(edge.premise_step)
    for edge in presentation.edges
    if id(edge.parent_step) in conclusion_step_ids
  }

  semantic_ids = {
    id(semantic.prerequisite_step)
    for semantic in semantic_sidecar.dependency_semantics
    if id(semantic.dependent_step) in conclusion_step_ids
  }

  return presentation_ids, semantic_ids


def _match_counts(
  block,
  presentation_provider_ids,
  semantic_provider_ids,
):
  block_step_ids = {
    id(step)
    for step in block.steps
  }
  return (
    len(block_step_ids & presentation_provider_ids),
    len(block_step_ids & semantic_provider_ids),
  )


def extract_generic_proof_chain_types(
  presentation,
  semantic_sidecar,
  arguments,
):
  audits = []

  for argument_index, argument in enumerate(arguments):
    claim_role = argument.conclusion_block.role.value
    presentation_provider_ids, semantic_provider_ids = (
      _direct_provider_step_ids(
        presentation,
        semantic_sidecar,
        argument.conclusion_block,
      )
    )
    occurrences = []

    for block in argument.supporting_blocks:
      presentation_count, semantic_count = _match_counts(
        block,
        presentation_provider_ids,
        semantic_provider_ids,
      )
      if presentation_count == 0 and semantic_count == 0:
        raise AssertionError(
          "supporting block is not a direct semantic provider"
        )

      occurrences.append(
        GenericProofChainOccurrence(
          argument_index=argument_index,
          argument_role=argument.role.value,
          chain_type=GenericProofChainType(
            claim_role=claim_role,
            provider_kind=(
              GenericProofChainProviderKind
              .SUPPORTING_BLOCK.value
            ),
            provider_role=block.role.value,
          ),
          provider_block_step_count=len(block.steps),
          direct_presentation_match_count=presentation_count,
          direct_semantic_match_count=semantic_count,
        )
      )

    for child_index in argument.child_argument_indices:
      child = arguments[child_index]
      child_block = child.conclusion_block
      presentation_count, semantic_count = _match_counts(
        child_block,
        presentation_provider_ids,
        semantic_provider_ids,
      )
      if presentation_count == 0 and semantic_count == 0:
        raise AssertionError(
          "child Argument conclusion is not a direct semantic provider"
        )

      occurrences.append(
        GenericProofChainOccurrence(
          argument_index=argument_index,
          argument_role=argument.role.value,
          chain_type=GenericProofChainType(
            claim_role=claim_role,
            provider_kind=(
              GenericProofChainProviderKind
              .CHILD_ARGUMENT.value
            ),
            provider_role=child.role.value,
          ),
          provider_block_step_count=len(child_block.steps),
          direct_presentation_match_count=presentation_count,
          direct_semantic_match_count=semantic_count,
        )
      )

    audits.append(
      GenericProofChainArgumentAudit(
        argument_index=argument_index,
        argument_role=argument.role.value,
        claim_role=claim_role,
        occurrences=tuple(occurrences),
      )
    )

  return tuple(audits)


def audit_pi6_3():
  presentation, semantic_sidecar, blocks, arguments = build_context(*TARGET)
  return extract_generic_proof_chain_types(
    presentation,
    semantic_sidecar,
    arguments,
  )


def generic_chain_type_inventory(audits):
  return Counter(
    occurrence.chain_type
    for audit in audits
    for occurrence in audit.occurrences
  )


def print_audit(audits):
  inventory = generic_chain_type_inventory(audits)

  print("=" * 78)
  print("Phase 144-6-R5-17B generic proof-chain type extraction audit")
  print("target: pi_6^3")
  print(
    "type vocabulary: claim block role <- "
    "(supporting block role | child Argument role)"
  )
  print(
    "excluded from type identity: theorem/rule name, statement class, "
    "node id, element name, graph depth"
  )
  print("=" * 78)

  for audit in audits:
    print()
    print(
      f"A{audit.argument_index + 1:02d} "
      f"argument_role={audit.argument_role} "
      f"claim_role={audit.claim_role}"
    )

    for occurrence in audit.occurrences:
      chain_type = occurrence.chain_type
      print(
        "  "
        f"{chain_type.claim_role} <- "
        f"{chain_type.provider_kind}:{chain_type.provider_role} "
        f"block_steps={occurrence.provider_block_step_count} "
        f"presentation_matches="
        f"{occurrence.direct_presentation_match_count} "
        f"semantic_matches="
        f"{occurrence.direct_semantic_match_count}"
      )

  print()
  print("Generic proof-chain type inventory")
  print("-" * 78)

  for chain_type, count in sorted(
    inventory.items(),
    key=lambda item: (
      item[0].claim_role,
      item[0].provider_kind,
      item[0].provider_role,
    ),
  ):
    print(
      f"{count:>3} x "
      f"{chain_type.claim_role} <- "
      f"{chain_type.provider_kind}:{chain_type.provider_role}"
    )

  print()
  print("Candidate generic chain families")
  print("-" * 78)
  print(
    "Argument composition: "
    "target <- child_argument:establish_order"
  )
  print(
    "Group-structure support: "
    "target <- supporting_block:{membership, group_structure, "
    "map_property, exactness}"
  )
  print(
    "Order support: "
    "order <- supporting_block:{calculation, group_structure, map_property}"
  )
  print(
    "Definition support: "
    "definition <- supporting_block:precondition"
  )
  print()
  print(
    "These are audit candidates only. 17C must apply the same vocabulary "
    "unchanged to the other five representative groups."
  )


if __name__ == "__main__":
  print_audit(audit_pi6_3())
