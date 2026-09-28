from collections import Counter
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
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
)


VISIBILITY_GAP_KEYS = (
  "pi5_3_group",
  "pi7_5_group",
  "hopf_pi7_surjective",
  "delta_zero",
)


@dataclass(frozen=True)
class HiddenAnchoredRecord:
  n: int
  k: int
  argument_index: int
  argument_role: str
  block_role: str
  statement_type: str
  inference_rule_name: str | None
  provider_anchor: bool
  distance_to_conclusion: int | None


@dataclass(frozen=True)
class Pi6GapPlacement:
  key: str
  argument_index: int
  argument_role: str
  in_chain: bool
  provider_anchor: bool
  frontier_hidden: bool
  block_role: str | None
  statement_type: str | None
  distance_to_conclusion: int | None


def _effective_hidden_ids(
  presentation,
  blocks,
  local_body,
  semantic_sidecar,
  argument,
):
  hidden = set(
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_body,
      semantic_sidecar,
      argument,
    )
  )
  if argument.role.value != "establish_definition":
    hidden.update(
      id(step)
      for block in local_body
      for step in block.steps
      if isinstance(step.conclusion, TodaEtaFamilyDefinitionStatement)
    )
  return frozenset(hidden)


def build_hidden_anchored_inventory():
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
      chain_ids, anchors, distances = _anchored_chain_step_ids(
        presentation,
        body,
        proof_chains[argument_index],
        conclusion_step,
      )
      hidden_ids = _effective_hidden_ids(
        presentation,
        blocks,
        body,
        semantic_sidecar,
        argument,
      )
      block_by_step_id = {
        id(step): block
        for block in body
        for step in block.steps
      }
      step_by_id = {
        id(step): step
        for block in body
        for step in block.steps
      }

      for step_id in chain_ids & hidden_ids:
        step = step_by_id.get(step_id)
        block = block_by_step_id.get(step_id)
        if step is None or block is None:
          continue
        rule = step.inference_rule
        records.append(
          HiddenAnchoredRecord(
            n=n,
            k=k,
            argument_index=argument_index,
            argument_role=argument.role.value,
            block_role=block.role.value,
            statement_type=type(step.conclusion).__name__,
            inference_rule_name=None if rule is None else rule.name,
            provider_anchor=step_id in anchors,
            distance_to_conclusion=distances.get(step_id),
          )
        )

  return tuple(records)


def build_pi6_gap_placements():
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
    chain_ids, anchors, distances = _anchored_chain_step_ids(
      presentation,
      body,
      proof_chains[argument_index],
      conclusion_step,
    )
    hidden_ids = _effective_hidden_ids(
      presentation,
      blocks,
      body,
      semantic_sidecar,
      argument,
    )
    block_by_step_id = {
      id(step): block
      for block in body
      for step in block.steps
    }

    for key in VISIBILITY_GAP_KEYS:
      matches = tuple(
        dict.fromkeys(
          step
          for block in blocks
          for step in block.steps
          if _step_contains_target(step, targets[key])
        )
      )
      selected = next(
        (
          step for step in matches
          if id(step) in chain_ids
        ),
        matches[0] if matches else None,
      )
      if selected is None:
        rows.append(
          Pi6GapPlacement(
            key=key,
            argument_index=argument_index,
            argument_role=argument.role.value,
            in_chain=False,
            provider_anchor=False,
            frontier_hidden=False,
            block_role=None,
            statement_type=None,
            distance_to_conclusion=None,
          )
        )
        continue
      step_id = id(selected)
      block = block_by_step_id.get(step_id)
      rows.append(
        Pi6GapPlacement(
          key=key,
          argument_index=argument_index,
          argument_role=argument.role.value,
          in_chain=step_id in chain_ids,
          provider_anchor=step_id in anchors,
          frontier_hidden=step_id in hidden_ids,
          block_role=None if block is None else block.role.value,
          statement_type=type(selected.conclusion).__name__,
          distance_to_conclusion=distances.get(step_id),
        )
      )

  return tuple(rows)


def _top(counter, limit=30):
  return counter.most_common(limit)


def print_audit():
  inventory = build_hidden_anchored_inventory()
  placements = build_pi6_gap_placements()

  print("=" * 78)
  print("Phase 144-6-R5-34 provider-anchored visibility gap audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. pi_6^3 genuine visibility-gap facts")
  print("-" * 78)
  for row in placements:
    print(
      f"{row.key}: argument={row.argument_index} role={row.argument_role} "
      f"in_chain={row.in_chain} anchor={row.provider_anchor} "
      f"hidden={row.frontier_hidden} block_role={row.block_role} "
      f"type={row.statement_type} distance={row.distance_to_conclusion}"
    )

  print("\\nB. Six-group hidden provider-anchored chain population")
  print("-" * 78)
  for n, k in TARGETS:
    rows = tuple(
      row for row in inventory
      if (row.n, row.k) == (n, k)
    )
    print(
      f"pi_{n + k}^{n}: hidden_anchored_occurrences={len(rows)} "
      f"direct_provider_anchors={sum(row.provider_anchor for row in rows)}"
    )
  print(
    f"totals: hidden_anchored_occurrences={len(inventory)} "
    f"direct_provider_anchors={sum(row.provider_anchor for row in inventory)}"
  )

  print("\\nC. Semantic distribution")
  print("-" * 78)
  print("Block roles")
  for name, count in _top(Counter(row.block_role for row in inventory)):
    print(f"{count:4d}  {name}")

  print("\\nStatement types")
  for name, count in _top(Counter(row.statement_type for row in inventory)):
    print(f"{count:4d}  {name}")

  print("\\nArgument roles")
  for name, count in _top(Counter(row.argument_role for row in inventory)):
    print(f"{count:4d}  {name}")

  print("\\nDistance to conclusion")
  for distance, count in sorted(
    Counter(row.distance_to_conclusion for row in inventory).items(),
    key=lambda item: (-1 if item[0] is None else item[0]),
  ):
    print(f"{count:4d}  {distance}")

  print("\\nD. Cross classification")
  print("-" * 78)
  cross = Counter(
    (
      row.argument_role,
      row.block_role,
      row.statement_type,
      "anchor" if row.provider_anchor else "chain",
    )
    for row in inventory
  )
  for key, count in _top(cross, 40):
    print(f"{count:4d}  {key}")

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "This audit measures steps that are simultaneously on a provider-anchored "
    "contribution chain and hidden by the current effective Argument frontier."
  )
  print(
    "A production visibility rule is justified only if the four pi_6^3 gaps "
    "belong to a structurally selective population across all six groups. "
    "Inference-rule names are diagnostic only and are not a selection rule."
  )
  print(
    "No production frontier, renderer, ownership, deduplication, ProofChain, "
    "membership, parity matcher, or public route is changed."
  )


if __name__ == "__main__":
  print_audit()
