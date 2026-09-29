from collections import Counter, defaultdict
from dataclasses import dataclass

from audit_phase144_6_r5_23 import (
  _canonical_fact_targets,
  _step_contains_target,
)
from audit_phase144_6_r5_29 import (
  _anchored_chain_step_ids,
  _local_body,
)
from audit_phase144_6_r5_30 import (
  HOPF_KEYS,
  _direct_upstream_calculation_attachment_ids,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_aggregate_semantics import (
  TodaGroupProofNarrativeAggregateSemanticKind,
)
from toda_group_proof_narrative_provenance_catalog import (
  is_toda_group_proof_narrative_provenance_only_statement,
)


@dataclass(frozen=True)
class AttachmentSemanticRecord:
  n: int
  k: int
  argument_index: int
  argument_role: str
  statement_type: str
  inference_rule_name: str | None
  target_block_role: str
  frontier_hidden: bool
  aggregate_kinds: tuple[str, ...]
  provenance_only: bool


@dataclass(frozen=True)
class HopfSemanticRecord:
  key: str
  argument_index: int
  argument_role: str
  attached: bool
  statement_type: str | None
  inference_rule_name: str | None
  target_block_role: str | None
  frontier_hidden: bool | None
  aggregate_kinds: tuple[str, ...]
  provenance_only: bool | None


def _block_by_step_id(blocks):
  return {
    id(step): block
    for block in blocks
    for step in block.steps
  }


def _aggregate_kinds_by_step_id(aggregate_semantic_sidecar):
  result = defaultdict(list)
  for semantic in aggregate_semantic_sidecar.step_semantics:
    value = semantic.kind.value
    if value not in result[id(semantic.proof_step)]:
      result[id(semantic.proof_step)].append(value)
  return {
    step_id: tuple(values)
    for step_id, values in result.items()
  }


def _target_roles_by_premise_id(presentation, block_by_step_id):
  result = defaultdict(list)
  for edge in presentation.edges:
    parent_role = block_by_step_id[id(edge.parent_step)].role.value
    if parent_role not in result[id(edge.premise_step)]:
      result[id(edge.premise_step)].append(parent_role)
  return result


def build_attachment_semantic_records():
  records = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(n, k)
    block_by_step_id = _block_by_step_id(blocks)
    aggregate_by_step_id = _aggregate_kinds_by_step_id(
      aggregate_semantic_sidecar
    )
    target_roles = _target_roles_by_premise_id(
      presentation,
      block_by_step_id,
    )

    for argument_index, argument in enumerate(arguments):
      conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
      if conclusion_step is None:
        continue
      body = _local_body(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
      base_chain_ids, anchors, distances = _anchored_chain_step_ids(
        presentation,
        body,
        proof_chains[argument_index],
        conclusion_step,
      )
      attachment_ids = _direct_upstream_calculation_attachment_ids(
        presentation,
        body,
        base_chain_ids,
      )
      hidden_ids = _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        blocks,
        body,
        semantic_sidecar,
        argument,
      )
      step_by_id = {
        id(step): step
        for block in body
        for step in block.steps
      }

      for step_id in sorted(
        attachment_ids,
        key=lambda candidate: next(
          i for i, node in enumerate(presentation.nodes)
          if id(node.proof_step) == candidate
        ),
      ):
        step = step_by_id[step_id]
        inference_rule = step.inference_rule
        roles = target_roles.get(step_id, ())
        target_role = ",".join(roles) if roles else "none"
        records.append(
          AttachmentSemanticRecord(
            n=n,
            k=k,
            argument_index=argument_index,
            argument_role=argument.role.value,
            statement_type=type(step.conclusion).__name__,
            inference_rule_name=(
              None if inference_rule is None else inference_rule.name
            ),
            target_block_role=target_role,
            frontier_hidden=step_id in hidden_ids,
            aggregate_kinds=aggregate_by_step_id.get(step_id, ()),
            provenance_only=is_toda_group_proof_narrative_provenance_only_statement(
              step.conclusion
            ),
          )
        )

  return tuple(records)


def build_pi6_hopf_semantic_records():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  targets = _canonical_fact_targets()
  block_by_step_id = _block_by_step_id(blocks)
  aggregate_by_step_id = _aggregate_kinds_by_step_id(
    aggregate_semantic_sidecar
  )
  target_roles = _target_roles_by_premise_id(
    presentation,
    block_by_step_id,
  )
  records = []

  for argument_index, argument in enumerate(arguments):
    conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    if conclusion_step is None:
      continue
    body = _local_body(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
    base_chain_ids, anchors, distances = _anchored_chain_step_ids(
      presentation,
      body,
      proof_chains[argument_index],
      conclusion_step,
    )
    attachment_ids = _direct_upstream_calculation_attachment_ids(
      presentation,
      body,
      base_chain_ids,
    )
    hidden_ids = _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      body,
      semantic_sidecar,
      argument,
    )

    for key in HOPF_KEYS:
      matching = tuple(
        dict.fromkeys(
          step
          for block in blocks
          for step in block.steps
          if _step_contains_target(step, targets[key])
        )
      )
      attached = tuple(
        step for step in matching if id(step) in attachment_ids
      )
      step = attached[0] if attached else (matching[0] if matching else None)
      if step is None:
        records.append(
          HopfSemanticRecord(
            key=key,
            argument_index=argument_index,
            argument_role=argument.role.value,
            attached=False,
            statement_type=None,
            inference_rule_name=None,
            target_block_role=None,
            frontier_hidden=None,
            aggregate_kinds=(),
            provenance_only=None,
          )
        )
        continue
      step_id = id(step)
      inference_rule = step.inference_rule
      records.append(
        HopfSemanticRecord(
          key=key,
          argument_index=argument_index,
          argument_role=argument.role.value,
          attached=bool(attached),
          statement_type=type(step.conclusion).__name__,
          inference_rule_name=(
            None if inference_rule is None else inference_rule.name
          ),
          target_block_role=",".join(target_roles.get(step_id, ())) or "none",
          frontier_hidden=step_id in hidden_ids,
          aggregate_kinds=aggregate_by_step_id.get(step_id, ()),
          provenance_only=is_toda_group_proof_narrative_provenance_only_statement(
            step.conclusion
          ),
        )
      )

  return tuple(records)


def _top(counter, limit=20):
  return counter.most_common(limit)


def print_audit():
  records = build_attachment_semantic_records()
  hopf = build_pi6_hopf_semantic_records()

  print("=" * 78)
  print("Phase 144-6-R5-31 upstream calculation attachment semantic audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. pi_6^3 Hopf attachment semantics")
  print("-" * 78)
  for row in hopf:
    print(
      f"{row.key}: argument={row.argument_index} role={row.argument_role} "
      f"attached={row.attached} type={row.statement_type} "
      f"target_role={row.target_block_role} "
      f"frontier_hidden={row.frontier_hidden} "
      f"aggregate={row.aggregate_kinds or '-'} "
      f"provenance_only={row.provenance_only}"
    )
    print(f"  rule={row.inference_rule_name}")

  print("\\nB. Attachment semantic inventory")
  print("-" * 78)
  print(f"attachment_occurrences={len(records)}")
  print(f"frontier_hidden={sum(row.frontier_hidden for row in records)}")
  print(f"frontier_visible={sum(not row.frontier_hidden for row in records)}")
  print(f"aggregate_annotated={sum(bool(row.aggregate_kinds) for row in records)}")
  print(f"provenance_only={sum(row.provenance_only for row in records)}")

  print("\\nStatement types")
  for name, count in _top(Counter(row.statement_type for row in records)):
    print(f"{count:4d}  {name}")

  print("\\nTarget block roles")
  for name, count in _top(Counter(row.target_block_role for row in records)):
    print(f"{count:4d}  {name}")

  print("\\nArgument roles")
  for name, count in _top(Counter(row.argument_role for row in records)):
    print(f"{count:4d}  {name}")

  print("\\nC. Cross classification: statement type x target role x visibility")
  print("-" * 78)
  cross = Counter(
    (
      row.statement_type,
      row.target_block_role,
      "hidden" if row.frontier_hidden else "visible",
    )
    for row in records
  )
  for key, count in _top(cross, 40):
    statement_type, target_role, visibility = key
    print(
      f"{count:4d}  {statement_type} -> {target_role} [{visibility}]"
    )

  print("\\nD. Production-readiness observations")
  print("-" * 78)
  print(
    "This audit classifies the Phase-30 one-hop CALCULATION attachments; "
    "it does not select a production semantic criterion."
  )
  print(
    "A viable criterion should explain both required Hopf attachments while "
    "excluding provenance-only or unrelated internal calculations without "
    "falling back to inference-rule-name special cases."
  )
  print(
    "No production ownership, renderer, frontier, deduplication, ProofChain, "
    "or membership rule is changed."
  )


if __name__ == "__main__":
  print_audit()
