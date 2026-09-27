from collections import Counter
from dataclasses import dataclass
from enum import Enum

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
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


class SupportCorrespondenceKind(Enum):
  EXACT_PRESENTATION_BLOCK = "exact_presentation_block"
  PARTIAL_PRESENTATION_BLOCK = "partial_presentation_block"
  SEMANTIC_ONLY_BLOCK = "semantic_only_block"
  CHILD_ARGUMENT_REPLACEMENT = "child_argument_replacement"


@dataclass(frozen=True)
class SupportingBlockCorrespondence:
  argument_index: int
  block_role: str
  block_step_count: int
  direct_presentation_step_count: int
  direct_semantic_step_count: int
  correspondence: SupportCorrespondenceKind
  statement_types: tuple[str, ...]


@dataclass(frozen=True)
class ChildArgumentCorrespondence:
  argument_index: int
  child_argument_index: int
  child_argument_role: str
  child_conclusion_block_role: str
  child_block_step_count: int
  direct_presentation_step_count: int
  direct_semantic_step_count: int
  correspondence: SupportCorrespondenceKind
  statement_types: tuple[str, ...]


@dataclass(frozen=True)
class ArgumentCorrespondenceAudit:
  argument_index: int
  argument_role: str
  conclusion_block_role: str
  conclusion_statement_type: str
  direct_presentation_provider_step_count: int
  direct_semantic_provider_step_count: int
  supporting_blocks: tuple[SupportingBlockCorrespondence, ...]
  child_arguments: tuple[ChildArgumentCorrespondence, ...]


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


def _statement_types(block):
  return tuple(
    type(step.conclusion).__name__
    for step in block.steps
  )


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


def _block_correspondence(
  block,
  presentation_provider_ids,
  semantic_provider_ids,
):
  block_step_ids = {
    id(step)
    for step in block.steps
  }
  presentation_matches = block_step_ids & presentation_provider_ids
  semantic_matches = block_step_ids & semantic_provider_ids

  if semantic_matches and not presentation_matches:
    kind = SupportCorrespondenceKind.SEMANTIC_ONLY_BLOCK
  elif presentation_matches == block_step_ids:
    kind = SupportCorrespondenceKind.EXACT_PRESENTATION_BLOCK
  elif presentation_matches:
    kind = SupportCorrespondenceKind.PARTIAL_PRESENTATION_BLOCK
  else:
    raise AssertionError(
      "supporting block has neither direct presentation nor semantic support"
    )

  return (
    kind,
    len(presentation_matches),
    len(semantic_matches),
  )


def audit_argument_correspondence(
  presentation,
  semantic_sidecar,
  blocks,
  arguments,
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

  presentation_provider_ids, semantic_provider_ids = (
    _direct_provider_step_ids(
      presentation,
      semantic_sidecar,
      argument.conclusion_block,
    )
  )

  supporting = []
  for block in argument.supporting_blocks:
    kind, presentation_count, semantic_count = _block_correspondence(
      block,
      presentation_provider_ids,
      semantic_provider_ids,
    )
    supporting.append(
      SupportingBlockCorrespondence(
        argument_index=argument_index,
        block_role=block.role.value,
        block_step_count=len(block.steps),
        direct_presentation_step_count=presentation_count,
        direct_semantic_step_count=semantic_count,
        correspondence=kind,
        statement_types=_statement_types(block),
      )
    )

  children = []
  for child_index in argument.child_argument_indices:
    child = arguments[child_index]
    child_block = child.conclusion_block
    child_step_ids = {
      id(step)
      for step in child_block.steps
    }
    presentation_matches = (
      child_step_ids & presentation_provider_ids
    )
    semantic_matches = child_step_ids & semantic_provider_ids

    children.append(
      ChildArgumentCorrespondence(
        argument_index=argument_index,
        child_argument_index=child_index,
        child_argument_role=child.role.value,
        child_conclusion_block_role=child_block.role.value,
        child_block_step_count=len(child_block.steps),
        direct_presentation_step_count=len(presentation_matches),
        direct_semantic_step_count=len(semantic_matches),
        correspondence=(
          SupportCorrespondenceKind.CHILD_ARGUMENT_REPLACEMENT
        ),
        statement_types=_statement_types(child_block),
      )
    )

  return ArgumentCorrespondenceAudit(
    argument_index=argument_index,
    argument_role=argument.role.value,
    conclusion_block_role=argument.conclusion_block.role.value,
    conclusion_statement_type=type(conclusion_step.conclusion).__name__,
    direct_presentation_provider_step_count=len(
      presentation_provider_ids
    ),
    direct_semantic_provider_step_count=len(
      semantic_provider_ids
    ),
    supporting_blocks=tuple(supporting),
    child_arguments=tuple(children),
  )


def audit_pi6_3():
  presentation, semantic_sidecar, blocks, arguments = build_context(*TARGET)
  return tuple(
    audit_argument_correspondence(
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      argument_index,
    )
    for argument_index in range(len(arguments))
  )


def print_audit(audits):
  print("=" * 78)
  print(
    "Phase 144-6-R5-17A-R3 support-edge correspondence / "
    "deduplication audit"
  )
  print("target: pi_6^3")
  print(
    "classification: exact presentation block / partial presentation block / "
    "semantic-only block / child-Argument replacement"
  )
  print("=" * 78)

  totals = Counter()

  for audit in audits:
    print()
    print(
      f"A{audit.argument_index + 1:02d} "
      f"role={audit.argument_role} "
      f"conclusion_block={audit.conclusion_block_role} "
      f"conclusion={audit.conclusion_statement_type}"
    )
    print(
      "  direct providers: "
      f"presentation_steps={audit.direct_presentation_provider_step_count} "
      f"semantic_steps={audit.direct_semantic_provider_step_count}"
    )

    for index, support in enumerate(
      audit.supporting_blocks,
      start=1,
    ):
      totals[support.correspondence.value] += 1
      print(
        f"  S{index:02d} role={support.block_role} "
        f"block_steps={support.block_step_count} "
        f"presentation_matches={support.direct_presentation_step_count} "
        f"semantic_matches={support.direct_semantic_step_count} "
        f"class={support.correspondence.value}"
      )
      print(
        "      statements=["
        + ", ".join(support.statement_types)
        + "]"
      )

    for child in audit.child_arguments:
      totals[child.correspondence.value] += 1
      print(
        f"  C->A{child.child_argument_index + 1:02d} "
        f"role={child.child_argument_role} "
        f"block_role={child.child_conclusion_block_role} "
        f"block_steps={child.child_block_step_count} "
        f"presentation_matches={child.direct_presentation_step_count} "
        f"semantic_matches={child.direct_semantic_step_count} "
        f"class={child.correspondence.value}"
      )
      print(
        "      statements=["
        + ", ".join(child.statement_types)
        + "]"
      )

  print()
  print("Summary")
  print("-" * 78)
  for kind in SupportCorrespondenceKind:
    print(f"{kind.value}: {totals[kind.value]}")

  print()
  print("Deduplication interpretation")
  print("-" * 78)
  print(
    "exact_presentation_block: supporting-block edge duplicates a direct "
    "presentation provider block exactly."
  )
  print(
    "partial_presentation_block: supporting-block edge groups the direct "
    "provider with additional same-role steps; block and ProofStep edges are "
    "different granularities of the same direct support."
  )
  print(
    "semantic_only_block: support exists only through semantic dependency and "
    "must not be removed merely because no presentation edge exists."
  )
  print(
    "child_argument_replacement: a direct provider block has been promoted to "
    "a child NarrativeArgument and should be represented at Argument granularity."
  )


if __name__ == "__main__":
  print_audit(audit_pi6_3())
