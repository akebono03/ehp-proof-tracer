from collections import Counter
from dataclasses import dataclass
from enum import Enum

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_aggregate_statement_catalog import (
  is_toda_group_proof_aggregate_statement,
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

TARGETS = ((5, 3), (4, 6), (5, 7), (8, 7), (9, 7))


class OtherSemanticResolution(Enum):
  AGGREGATE_STATEMENT = "aggregate_statement"
  PROVENANCE_ONLY_STATEMENT = "provenance_only_statement"
  EXISTING_ROLE_CANDIDATE = "existing_role_candidate"
  UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class OtherProviderOccurrence:
  n: int
  k: int
  argument_index: int
  argument_role: str
  claim_role: str
  statement_type: str
  rule_name: str
  resolution: OtherSemanticResolution
  aggregate: bool
  provenance_only: bool


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


def _rule_name(step):
  if step.inference_rule is None:
    return "<none>"
  return step.inference_rule.name


def _direct_presentation_provider_steps(presentation, conclusion_block):
  conclusion_ids = {id(step) for step in conclusion_block.steps}
  result = []
  seen = set()
  for edge in presentation.edges:
    if id(edge.parent_step) not in conclusion_ids:
      continue
    step = edge.premise_step
    if id(step) in seen:
      continue
    seen.add(id(step))
    result.append(step)
  return tuple(result)


def _classify_statement(statement):
  aggregate = is_toda_group_proof_aggregate_statement(statement)
  provenance_only = is_toda_group_proof_narrative_provenance_only_statement(
    statement
  )

  if aggregate and provenance_only:
    raise AssertionError(
      "OTHER provider statement belongs to both aggregate and provenance-only catalogs"
    )
  if aggregate:
    return OtherSemanticResolution.AGGREGATE_STATEMENT
  if provenance_only:
    return OtherSemanticResolution.PROVENANCE_ONLY_STATEMENT
  return OtherSemanticResolution.UNRESOLVED


def audit_other_providers():
  occurrences = []

  for n, k in TARGETS:
    presentation, semantic_sidecar, blocks, arguments = build_context(n, k)

    for argument_index, argument in enumerate(arguments):
      direct_steps = _direct_presentation_provider_steps(
        presentation,
        argument.conclusion_block,
      )

      for block in argument.supporting_blocks:
        if block.role is not TodaGroupProofNarrativeMathematicalBlockRole.OTHER:
          continue

        block_ids = {id(step) for step in block.steps}
        matched_steps = tuple(
          step for step in direct_steps if id(step) in block_ids
        )
        if not matched_steps:
          raise AssertionError("OTHER supporting block has no direct provider step")

        for step in matched_steps:
          statement = step.conclusion
          aggregate = is_toda_group_proof_aggregate_statement(statement)
          provenance_only = (
            is_toda_group_proof_narrative_provenance_only_statement(statement)
          )
          occurrences.append(
            OtherProviderOccurrence(
              n=n,
              k=k,
              argument_index=argument_index,
              argument_role=argument.role.value,
              claim_role=argument.conclusion_block.role.value,
              statement_type=type(statement).__name__,
              rule_name=_rule_name(step),
              resolution=_classify_statement(statement),
              aggregate=aggregate,
              provenance_only=provenance_only,
            )
          )

  return tuple(occurrences)


def print_audit():
  occurrences = audit_other_providers()

  print("=" * 78)
  print("Phase 144-6-R5-17D-R1 OTHER semantic-role resolution audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nOccurrence summary")
  print("-" * 78)
  print(f"OTHER direct-provider occurrences: {len(occurrences)}")
  counts = Counter(item.resolution for item in occurrences)
  for resolution in OtherSemanticResolution:
    print(f"{resolution.value}: {counts[resolution]}")

  print("\\nStatement-type resolution")
  print("-" * 78)
  signatures = Counter(
    (
      item.statement_type,
      item.resolution.value,
      item.aggregate,
      item.provenance_only,
    )
    for item in occurrences
  )
  for signature, count in sorted(signatures.items()):
    statement_type, resolution, aggregate, provenance_only = signature
    print(
      f"{count:>3} x {statement_type} "
      f"resolution={resolution} "
      f"aggregate={aggregate} provenance_only={provenance_only}"
    )

  print("\\nOccurrence detail")
  print("-" * 78)
  for item in occurrences:
    print(
      f"pi_{item.n + item.k}^{item.n} "
      f"A{item.argument_index + 1:02d} "
      f"claim={item.claim_role} "
      f"statement={item.statement_type}"
    )
    print(f"    rule={item.rule_name}")
    print(
      f"    resolution={item.resolution.value} "
      f"aggregate={item.aggregate} "
      f"provenance_only={item.provenance_only}"
    )

  print("\\nResolution interpretation")
  print("-" * 78)
  print(
    "aggregate_statement: the statement already has an explicit aggregate "
    "semantic axis and renderer. Do not force it into an unrelated single "
    "mathematical block role during this audit."
  )
  print(
    "provenance_only_statement: the statement is already explicitly classified "
    "as provenance-only. Its appearance as a direct Argument provider must be "
    "resolved at the ProofChain/Narrative selection boundary rather than by "
    "inventing a mathematical block role."
  )
  print(
    "unresolved: no existing semantic catalog explains the OTHER provider; "
    "only this class would justify investigating a new role."
  )

  unresolved = tuple(
    item for item in occurrences
    if item.resolution is OtherSemanticResolution.UNRESOLVED
  )
  print("\\nProduction decision input")
  print("-" * 78)
  if unresolved:
    print(
      f"unresolved OTHER providers remain: {len(unresolved)}. "
      "17E must not finalize the architecture yet."
    )
  else:
    print(
      "unresolved OTHER providers remain: 0. "
      "All audited OTHER occurrences are explained by existing semantic "
      "catalogs; no new mathematical block role is justified by this audit."
    )


if __name__ == "__main__":
  print_audit()
