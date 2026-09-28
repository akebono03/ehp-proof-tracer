from collections import defaultdict
from dataclasses import dataclass

from audit_phase144_6_r5_23 import (
  _canonical_fact_targets,
  _step_contains_target,
)
from audit_phase144_6_r5_29 import (
  _anchored_chain_step_ids,
  _local_body,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)


HOPF_KEYS = (
  "hopf_nu_prime",
  "hopf_nu_eta6",
)


@dataclass(frozen=True)
class AttachmentInventory:
  n: int
  k: int
  argument_index: int
  argument_role: str
  base_chain_steps: int
  direct_calculation_attachments: int
  attached_chain_steps: int
  local_steps: int


@dataclass(frozen=True)
class HopfAttachmentPlacement:
  key: str
  argument_index: int
  argument_role: str
  in_base_chain: bool
  direct_calculation_attachment: bool
  in_attached_chain: bool


def _block_by_step_id(local_body):
  return {
    id(step): block
    for block in local_body
    for step in block.steps
  }


def _direct_upstream_calculation_attachment_ids(
  presentation,
  local_body,
  base_chain_ids,
):
  block_by_step_id = _block_by_step_id(local_body)
  local_ids = set(block_by_step_id)
  attachment_ids = set()

  for edge in presentation.edges:
    premise_id = id(edge.premise_step)
    parent_id = id(edge.parent_step)

    if parent_id not in base_chain_ids:
      continue
    if premise_id not in local_ids:
      continue
    if premise_id in base_chain_ids:
      continue
    if (
      block_by_step_id[premise_id].role
      is not TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION
    ):
      continue

    attachment_ids.add(premise_id)

  return frozenset(attachment_ids)


def build_six_group_attachment_inventory():
  rows = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(n, k)

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
      attachments = _direct_upstream_calculation_attachment_ids(
        presentation,
        body,
        base_chain_ids,
      )
      local_ids = {
        id(step)
        for block in body
        for step in block.steps
      }

      rows.append(
        AttachmentInventory(
          n=n,
          k=k,
          argument_index=argument_index,
          argument_role=argument.role.value,
          base_chain_steps=len(base_chain_ids),
          direct_calculation_attachments=len(attachments),
          attached_chain_steps=len(base_chain_ids | attachments),
          local_steps=len(local_ids),
        )
      )

  return tuple(rows)


def build_pi6_hopf_attachment_placements():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  targets = _canonical_fact_targets()
  rows = []

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
    attachments = _direct_upstream_calculation_attachment_ids(
      presentation,
      body,
      base_chain_ids,
    )
    attached = base_chain_ids | attachments

    for key in HOPF_KEYS:
      matching = tuple(
        dict.fromkeys(
          step
          for block in blocks
          for step in block.steps
          if _step_contains_target(step, targets[key])
        )
      )
      rows.append(
        HopfAttachmentPlacement(
          key=key,
          argument_index=argument_index,
          argument_role=argument.role.value,
          in_base_chain=any(
            id(step) in base_chain_ids for step in matching
          ),
          direct_calculation_attachment=any(
            id(step) in attachments for step in matching
          ),
          in_attached_chain=any(
            id(step) in attached for step in matching
          ),
        )
      )

  return tuple(rows)


def _attachment_role_inventory():
  result = defaultdict(int)

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(n, k)

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
      attachments = _direct_upstream_calculation_attachment_ids(
        presentation,
        body,
        base_chain_ids,
      )
      for step_id in attachments:
        result[(n, k, argument.role.value)] += 1

  return result


def print_audit():
  inventory = build_six_group_attachment_inventory()
  placements = build_pi6_hopf_attachment_placements()

  print("=" * 78)
  print("Phase 144-6-R5-30 upstream calculation attachment audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. pi_6^3 Hopf facts")
  print("-" * 78)
  for row in placements:
    print(
      f"{row.key}: argument={row.argument_index} "
      f"role={row.argument_role} "
      f"base_chain={row.in_base_chain} "
      f"direct_calc_attachment={row.direct_calculation_attachment} "
      f"attached_chain={row.in_attached_chain}"
    )

  print("\\nB. Six-group direct upstream CALCULATION attachment impact")
  print("-" * 78)
  totals = [0, 0, 0, 0]
  for n, k in TARGETS:
    rows = tuple(
      row for row in inventory if (row.n, row.k) == (n, k)
    )
    local = sum(row.local_steps for row in rows)
    base = sum(row.base_chain_steps for row in rows)
    attachments = sum(row.direct_calculation_attachments for row in rows)
    attached = sum(row.attached_chain_steps for row in rows)
    totals[0] += local
    totals[1] += base
    totals[2] += attachments
    totals[3] += attached
    print(
      f"pi_{n + k}^{n}: arguments={len(rows)} "
      f"local={local} base_chain={base} "
      f"attachments={attachments} attached_chain={attached}"
    )

  print(
    f"totals: local={totals[0]} base_chain={totals[1]} "
    f"attachments={totals[2]} attached_chain={totals[3]}"
  )

  print("\\nC. Attachment distribution by Argument role")
  print("-" * 78)
  role_inventory = _attachment_role_inventory()
  for key in sorted(role_inventory):
    n, k, role = key
    print(
      f"pi_{n + k}^{n}: role={role} "
      f"attachments={role_inventory[key]}"
    )

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "The audited rule attaches only a CALCULATION premise that directly feeds "
    "an existing provider-anchored chain step, remains inside the same "
    "Argument local body, and is not already in the base chain."
  )
  print(
    "There is no recursive upstream expansion in this audit. "
    "If the Hopf facts are not captured, the rule must be refined rather "
    "than widened recursively."
  )
  print(
    "No production ownership, renderer, frontier, deduplication, ProofChain, "
    "or membership rule is changed."
  )


if __name__ == "__main__":
  print_audit()
