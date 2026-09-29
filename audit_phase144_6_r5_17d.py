from collections import Counter
from dataclasses import dataclass
from enum import Enum

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import build_toda_group_proof_narrative_arguments
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_proof_dependency import extract_toda_recursive_proof_provenance

BASELINE_TARGET = (3, 3)
CROSS_GROUP_TARGETS = ((5, 3), (4, 6), (5, 7), (8, 7), (9, 7))


class GenericProofChainProviderKind(Enum):
  SUPPORTING_BLOCK = "supporting_block"
  CHILD_ARGUMENT = "child_argument"


@dataclass(frozen=True, order=True)
class GenericProofChainType:
  claim_role: str
  provider_kind: str
  provider_role: str


class NoveltyClassification(Enum):
  REUSED_BASELINE_TYPE = "reused_baseline_type"
  EXPLICIT_ROLE_NOVELTY = "explicit_role_novelty"
  CHILD_ARGUMENT_NOVELTY = "child_argument_novelty"
  OTHER_ROLE_SEMANTIC_GAP_CANDIDATE = "other_role_semantic_gap_candidate"


@dataclass(frozen=True)
class NoveltyOccurrence:
  n: int
  k: int
  argument_index: int
  argument_role: str
  chain_type: GenericProofChainType
  classification: NoveltyClassification
  direct_statement_types: tuple[str, ...]
  direct_rule_names: tuple[str, ...]


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


def _direct_provider_steps(presentation, semantic_sidecar, conclusion_block):
  conclusion_ids = {id(step) for step in conclusion_block.steps}
  steps = []
  seen = set()

  for edge in presentation.edges:
    if id(edge.parent_step) not in conclusion_ids:
      continue
    step = edge.premise_step
    if id(step) not in seen:
      seen.add(id(step))
      steps.append(step)

  for semantic in semantic_sidecar.dependency_semantics:
    if id(semantic.dependent_step) not in conclusion_ids:
      continue
    step = semantic.prerequisite_step
    if id(step) not in seen:
      seen.add(id(step))
      steps.append(step)

  return tuple(steps)


def _steps_in_block(direct_steps, block):
  block_ids = {id(step) for step in block.steps}
  return tuple(step for step in direct_steps if id(step) in block_ids)


def _chain_type_for_block(argument, block):
  return GenericProofChainType(
    claim_role=argument.conclusion_block.role.value,
    provider_kind=GenericProofChainProviderKind.SUPPORTING_BLOCK.value,
    provider_role=block.role.value,
  )


def _chain_type_for_child(argument, child):
  return GenericProofChainType(
    claim_role=argument.conclusion_block.role.value,
    provider_kind=GenericProofChainProviderKind.CHILD_ARGUMENT.value,
    provider_role=child.role.value,
  )


def _chain_types_for_target(n, k):
  presentation, semantic_sidecar, blocks, arguments = build_context(n, k)
  types = []
  for argument in arguments:
    for block in argument.supporting_blocks:
      types.append(_chain_type_for_block(argument, block))
    for child_index in argument.child_argument_indices:
      types.append(_chain_type_for_child(argument, arguments[child_index]))
  return tuple(types)


def baseline_chain_types():
  return frozenset(_chain_types_for_target(*BASELINE_TARGET))


def classify_chain_type(chain_type, baseline_types):
  if chain_type in baseline_types:
    return NoveltyClassification.REUSED_BASELINE_TYPE

  if chain_type.provider_kind == GenericProofChainProviderKind.CHILD_ARGUMENT.value:
    return NoveltyClassification.CHILD_ARGUMENT_NOVELTY

  if chain_type.provider_role == "other":
    return NoveltyClassification.OTHER_ROLE_SEMANTIC_GAP_CANDIDATE

  return NoveltyClassification.EXPLICIT_ROLE_NOVELTY


def _rule_name(step):
  inference_rule = step.inference_rule
  if inference_rule is None:
    return "<none>"
  return inference_rule.name


def audit_target(n, k, baseline_types):
  presentation, semantic_sidecar, blocks, arguments = build_context(n, k)
  occurrences = []

  for argument_index, argument in enumerate(arguments):
    direct_steps = _direct_provider_steps(
      presentation,
      semantic_sidecar,
      argument.conclusion_block,
    )

    for block in argument.supporting_blocks:
      matched_steps = _steps_in_block(direct_steps, block)
      if not matched_steps:
        raise AssertionError("supporting block has no direct provider step")

      chain_type = _chain_type_for_block(argument, block)
      occurrences.append(
        NoveltyOccurrence(
          n=n,
          k=k,
          argument_index=argument_index,
          argument_role=argument.role.value,
          chain_type=chain_type,
          classification=classify_chain_type(chain_type, baseline_types),
          direct_statement_types=tuple(sorted({
            type(step.conclusion).__name__
            for step in matched_steps
          })),
          direct_rule_names=tuple(sorted({
            _rule_name(step)
            for step in matched_steps
          })),
        )
      )

    for child_index in argument.child_argument_indices:
      child = arguments[child_index]
      matched_steps = _steps_in_block(direct_steps, child.conclusion_block)
      if not matched_steps:
        raise AssertionError("child Argument has no direct provider step")

      chain_type = _chain_type_for_child(argument, child)
      occurrences.append(
        NoveltyOccurrence(
          n=n,
          k=k,
          argument_index=argument_index,
          argument_role=argument.role.value,
          chain_type=chain_type,
          classification=classify_chain_type(chain_type, baseline_types),
          direct_statement_types=tuple(sorted({
            type(step.conclusion).__name__
            for step in matched_steps
          })),
          direct_rule_names=tuple(sorted({
            _rule_name(step)
            for step in matched_steps
          })),
        )
      )

  return tuple(occurrences)


def audit_cross_groups():
  baseline_types = baseline_chain_types()
  return tuple(
    occurrence
    for n, k in CROSS_GROUP_TARGETS
    for occurrence in audit_target(n, k, baseline_types)
  )


def novelty_occurrences():
  return tuple(
    occurrence
    for occurrence in audit_cross_groups()
    if occurrence.classification is not NoveltyClassification.REUSED_BASELINE_TYPE
  )


def _format_chain_type(chain_type):
  return (
    f"{chain_type.claim_role} <- "
    f"{chain_type.provider_kind}:{chain_type.provider_role}"
  )


def print_audit():
  occurrences = audit_cross_groups()
  novelties = tuple(
    item for item in occurrences
    if item.classification is not NoveltyClassification.REUSED_BASELINE_TYPE
  )

  print("=" * 78)
  print("Phase 144-6-R5-17D failure / novelty classification audit")
  print("targets: pi_8^5, pi_10^4, pi_12^5, pi_15^8, pi_16^9")
  print("production changes: none")
  print("=" * 78)

  counts = Counter(item.classification for item in occurrences)
  print("\\nClassification summary")
  print("-" * 78)
  for classification in NoveltyClassification:
    print(f"{classification.value}: {counts[classification]}")

  type_counts = Counter(item.chain_type for item in novelties)
  print("\\nNovel chain types")
  print("-" * 78)
  for chain_type, count in sorted(type_counts.items()):
    classifications = sorted({
      item.classification.value
      for item in novelties
      if item.chain_type == chain_type
    })
    print(
      f"{count:>3} x {_format_chain_type(chain_type)} "
      f"class={','.join(classifications)}"
    )

  print("\\nNovelty occurrences")
  print("-" * 78)
  for item in novelties:
    print(
      f"pi_{item.n + item.k}^{item.n} "
      f"A{item.argument_index + 1:02d} "
      f"{_format_chain_type(item.chain_type)} "
      f"class={item.classification.value}"
    )
    print(
      "    direct_statement_types=["
      + ", ".join(item.direct_statement_types)
      + "]"
    )
    print(
      "    direct_rule_names=["
      + ", ".join(item.direct_rule_names)
      + "]"
    )

  other_items = tuple(
    item for item in novelties
    if item.classification
    is NoveltyClassification.OTHER_ROLE_SEMANTIC_GAP_CANDIDATE
  )
  print("\\nOTHER semantic-gap inventory")
  print("-" * 78)
  other_signatures = Counter(
    (
      item.chain_type.claim_role,
      item.direct_statement_types,
      item.direct_rule_names,
    )
    for item in other_items
  )
  for signature, count in sorted(other_signatures.items()):
    claim_role, statement_types, rule_names = signature
    print(
      f"{count:>3} x claim={claim_role} "
      f"statements=[{', '.join(statement_types)}] "
      f"rules=[{', '.join(rule_names)}]"
    )

  child_items = tuple(
    item for item in novelties
    if item.classification is NoveltyClassification.CHILD_ARGUMENT_NOVELTY
  )
  print("\\nChild-Argument novelty inventory")
  print("-" * 78)
  child_counts = Counter(item.chain_type for item in child_items)
  for chain_type, count in sorted(child_counts.items()):
    print(f"{count:>3} x {_format_chain_type(chain_type)}")

  explicit_items = tuple(
    item for item in novelties
    if item.classification is NoveltyClassification.EXPLICIT_ROLE_NOVELTY
  )
  print("\\nExplicit-role novelty inventory")
  print("-" * 78)
  explicit_counts = Counter(item.chain_type for item in explicit_items)
  for chain_type, count in sorted(explicit_counts.items()):
    print(f"{count:>3} x {_format_chain_type(chain_type)}")

  print("\\n17D decision boundary")
  print("-" * 78)
  print(
    "explicit_role_novelty: structurally representable by an already explicit "
    "Narrative block role; not a schema failure."
  )
  print(
    "child_argument_novelty: structurally representable at Argument granularity; "
    "17E must decide whether child Definition is canonical Narrative composition."
  )
  print(
    "other_role_semantic_gap_candidate: schema can carry it, but OTHER is not "
    "yet a satisfactory mathematical role; inspect signatures before production."
  )
  print(
    "No role additions or production ProofChain changes are made in this audit."
  )


if __name__ == "__main__":
  print_audit()
