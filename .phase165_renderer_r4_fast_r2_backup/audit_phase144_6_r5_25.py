from dataclasses import dataclass
from enum import Enum

from audit_phase144_6_r5_23 import (
  _canonical_fact_targets,
  _step_contains_target,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_proof_chains import (
  TodaGroupProofNarrativeProofChainProviderKind,
)


FRONTIER_REQUIRED_KEYS = (
  "pi5_3_group",
  "pi7_5_group",
  "hopf_pi7_surjective",
  "delta_zero",
)


class SuppressionCause(Enum):
  SEEN_NON_EXACT_BLOCK = "seen_non_exact_block"
  NOT_SEEN_BLOCK = "not_seen_block"


@dataclass(frozen=True)
class MultiSuppressionTrace:
  key: str
  source_argument_indices: tuple[int, ...]
  source_block_roles: tuple[str, ...]
  first_render_argument_index: int | None
  later_seen_suppressed_argument_indices: tuple[int, ...]
  cause: SuppressionCause


@dataclass(frozen=True)
class FrontierCandidateSignature:
  n: int
  k: int
  argument_index: int
  argument_role: str
  block_role: str
  is_supporting_provider: bool
  is_direct_conclusion_premise: bool
  statement_type: str
  required_pi6_key: str | None


def _local_bodies(presentation, blocks, semantic_sidecar, arguments):
  return tuple(
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
    for argument_index in range(len(arguments))
  )


def build_multi_suppression_traces():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  targets = _canonical_fact_targets()
  local_bodies = _local_bodies(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )

  ordered_arguments = order_toda_group_proof_narrative_arguments(arguments)
  source_index = {id(argument): i for i, argument in enumerate(arguments)}
  ordered_indices = tuple(source_index[id(a)] for a in ordered_arguments)

  traces = []
  for key in ("hopf_nu_prime", "hopf_nu_eta6"):
    target = targets[key]
    matching_steps = tuple(
      dict.fromkeys(
        step
        for block in blocks
        for step in block.steps
        if _step_contains_target(step, target)
      )
    )
    matching_ids = {id(step) for step in matching_steps}
    source_blocks = tuple(
      block
      for block in blocks
      if any(id(step) in matching_ids for step in block.steps)
    )
    source_block_ids = {id(block) for block in source_blocks}

    source_arguments = tuple(
      index
      for index, body in enumerate(local_bodies)
      if any(id(block) in source_block_ids for block in body)
    )

    seen = set()
    first_render = None
    suppressed = []
    for argument_index in ordered_indices:
      body = local_bodies[argument_index]
      contains = any(id(block) in source_block_ids for block in body)
      if contains:
        if any(id(block) in seen for block in source_blocks):
          suppressed.append(argument_index)
        elif first_render is None:
          first_render = argument_index

      for block in body:
        if block.role is not TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS:
          seen.add(id(block))

    cause = (
      SuppressionCause.SEEN_NON_EXACT_BLOCK
      if suppressed
      else SuppressionCause.NOT_SEEN_BLOCK
    )
    traces.append(
      MultiSuppressionTrace(
        key=key,
        source_argument_indices=source_arguments,
        source_block_roles=tuple(
          dict.fromkeys(block.role.value for block in source_blocks)
        ),
        first_render_argument_index=first_render,
        later_seen_suppressed_argument_indices=tuple(suppressed),
        cause=cause,
      )
    )
  return tuple(traces)


def _pi6_required_key_for_step(step, targets):
  for key in FRONTIER_REQUIRED_KEYS:
    if _step_contains_target(step, targets[key]):
      return key
  return None


def build_frontier_candidate_signatures():
  signatures = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(n, k)
    local_bodies = _local_bodies(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
    targets = _canonical_fact_targets() if (n, k) == (3, 3) else None

    for argument_index, argument in enumerate(arguments):
      hidden = _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        blocks,
        local_bodies[argument_index],
        semantic_sidecar,
        argument,
      )
      supporting_step_ids = {
        id(step)
        for provider in proof_chains[argument_index].providers
        if (
          provider.kind
          is TodaGroupProofNarrativeProofChainProviderKind.SUPPORTING_BLOCK
        )
        for step in provider.supporting_block.steps
      }
      conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
      direct_premise_ids = (
        set()
        if conclusion_step is None
        else {id(step) for step in conclusion_step.premises}
      )

      for block in local_bodies[argument_index]:
        for step in block.steps:
          step_id = id(step)
          if step_id not in hidden:
            continue
          if step_id not in supporting_step_ids:
            continue

          signatures.append(
            FrontierCandidateSignature(
              n=n,
              k=k,
              argument_index=argument_index,
              argument_role=argument.role.value,
              block_role=block.role.value,
              is_supporting_provider=True,
              is_direct_conclusion_premise=step_id in direct_premise_ids,
              statement_type=type(step.conclusion).__name__,
              required_pi6_key=(
                None
                if targets is None
                else _pi6_required_key_for_step(step, targets)
              ),
            )
          )
  return tuple(signatures)


def print_audit():
  suppression = build_multi_suppression_traces()
  candidates = build_frontier_candidate_signatures()

  print("=" * 78)
  print("Phase 144-6-R5-25 multi-Argument suppression + selective frontier relevance audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. Multi-Argument suppression")
  print("-" * 78)
  for trace in suppression:
    print(trace.key)
    print(
      "  source_arguments="
      + ",".join(map(str, trace.source_argument_indices))
    )
    print("  block_roles=" + ",".join(trace.source_block_roles))
    print(f"  first_render_argument={trace.first_render_argument_index}")
    print(
      "  later_seen_suppressed_arguments="
      + (
        ",".join(map(str, trace.later_seen_suppressed_argument_indices))
        if trace.later_seen_suppressed_argument_indices
        else "-"
      )
    )
    print(f"  cause={trace.cause.value}")

  print("\\nB. Hidden direct supporting-provider signature inventory")
  print("-" * 78)
  print(f"candidate_occurrences={len(candidates)}")

  signature_counts = {}
  for candidate in candidates:
    signature = (
      candidate.argument_role,
      candidate.block_role,
      candidate.is_direct_conclusion_premise,
      candidate.statement_type,
    )
    signature_counts[signature] = signature_counts.get(signature, 0) + 1

  for signature, count in sorted(
    signature_counts.items(),
    key=lambda item: (-item[1], item[0]),
  ):
    argument_role, block_role, direct, statement_type = signature
    print(
      f"{count:4d} x argument={argument_role} block={block_role} "
      f"direct_premise={direct} statement={statement_type}"
    )

  print("\\nC. pi_6^3 required frontier facts")
  print("-" * 78)
  required = tuple(
    candidate
    for candidate in candidates
    if candidate.required_pi6_key is not None
  )
  for candidate in required:
    print(
      f"{candidate.required_pi6_key}: "
      f"argument={candidate.argument_index} "
      f"argument_role={candidate.argument_role} "
      f"block_role={candidate.block_role} "
      f"direct_premise={candidate.is_direct_conclusion_premise} "
      f"statement_type={candidate.statement_type}"
    )

  required_signatures = {
    (
      candidate.argument_role,
      candidate.block_role,
      candidate.is_direct_conclusion_premise,
      candidate.statement_type,
    )
    for candidate in required
  }
  matching_non_required = tuple(
    candidate
    for candidate in candidates
    if candidate.required_pi6_key is None
    and (
      candidate.argument_role,
      candidate.block_role,
      candidate.is_direct_conclusion_premise,
      candidate.statement_type,
    ) in required_signatures
  )
  print(
    "non_required_occurrences_sharing_required_signatures="
    f"{len(matching_non_required)}"
  )

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "Do not replace block-level seen suppression until the audit proves that "
    "the missing Hopf facts are specifically lost by seen_non_exact_block_ids."
  )
  print(
    "Do not protect a frontier signature merely because it matches pi_6^3; "
    "a production rule needs a semantic reason that remains valid across groups."
  )
  print(
    "Embedded nu-prime eta_6 membership remains a separate generic "
    "expression-to-membership problem."
  )


if __name__ == "__main__":
  print_audit()
