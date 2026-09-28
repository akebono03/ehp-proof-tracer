from collections import Counter
from dataclasses import dataclass

from audit_phase144_6_r5_23 import (
  _canonical_fact_targets,
  _step_contains_target,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
  classify_toda_group_proof_narrative_argument_discourse_roles,
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
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
)


HOPF_KEYS = (
  "hopf_nu_prime",
  "hopf_nu_eta6",
)


@dataclass(frozen=True)
class DedupGroupAudit:
  n: int
  k: int
  visible_occurrences: int
  block_assembly_kept_occurrences: int
  step_assembly_kept_occurrences: int
  released_occurrences: int
  repeated_visible_occurrences: int
  unique_visible_steps: int


@dataclass(frozen=True)
class HopfDedupAudit:
  key: str
  ordered_position: int
  argument_index: int
  argument_role: str
  visible: bool
  block_assembly_kept: bool
  step_assembly_kept: bool
  released_by_step_dedup: bool


def _ordered_active_argument_rows(arguments):
  ordered = order_toda_group_proof_narrative_arguments(arguments)
  discourse = classify_toda_group_proof_narrative_argument_discourse_roles(
    arguments
  )
  source_index = {id(argument): index for index, argument in enumerate(arguments)}
  rows = []
  for position, argument in enumerate(ordered):
    if discourse[position] is TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED:
      continue
    rows.append((position, source_index[id(argument)], argument))
  return tuple(rows)


def _visible_non_exact_steps(
  presentation,
  blocks,
  semantic_sidecar,
  arguments,
  argument_index,
  argument,
):
  local = extract_toda_group_proof_narrative_argument_local_body_blocks(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    argument_index,
  )
  hidden = {
    id(step)
    for block in local
    for step in block.steps
    if (
      argument.role is not TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
      and isinstance(step.conclusion, TodaEtaFamilyDefinitionStatement)
    )
  }
  hidden.update(
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local,
      semantic_sidecar,
      argument,
    )
  )
  return tuple(
    (block, step)
    for block in local
    if block.role is not TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
    for step in block.steps
    if id(step) not in hidden
  )


def build_group_dedup_audit():
  result = []
  for n, k in TARGETS:
    presentation, semantic_sidecar, blocks, arguments, aggregate_sidecar, chains = _context(n, k)
    visible_occurrences = []
    block_kept = []
    step_kept = []
    seen_blocks = set()
    seen_steps = set()

    for position, argument_index, argument in _ordered_active_argument_rows(arguments):
      visible = _visible_non_exact_steps(
        presentation, blocks, semantic_sidecar, arguments, argument_index, argument
      )
      for block, step in visible:
        visible_occurrences.append((argument_index, block, step))
        if id(block) not in seen_blocks:
          block_kept.append((argument_index, block, step))
        if id(step) not in seen_steps:
          step_kept.append((argument_index, block, step))
      seen_blocks.update(id(block) for block, step in visible)
      seen_steps.update(id(step) for block, step in visible)

    counts = Counter(id(step) for _, _, step in visible_occurrences)
    repeated = sum(count - 1 for count in counts.values() if count > 1)
    block_keys = {(a, id(b), id(s)) for a, b, s in block_kept}
    step_keys = {(a, id(b), id(s)) for a, b, s in step_kept}
    released = len(step_keys - block_keys)

    result.append(
      DedupGroupAudit(
        n=n,
        k=k,
        visible_occurrences=len(visible_occurrences),
        block_assembly_kept_occurrences=len(block_kept),
        step_assembly_kept_occurrences=len(step_kept),
        released_occurrences=released,
        repeated_visible_occurrences=repeated,
        unique_visible_steps=len(counts),
      )
    )
  return tuple(result)


def build_pi6_hopf_dedup_audit():
  presentation, semantic_sidecar, blocks, arguments, aggregate_sidecar, chains = _context(3, 3)
  targets = _canonical_fact_targets()
  matching_by_key = {
    key: {
      id(step)
      for block in blocks
      for step in block.steps
      if _step_contains_target(step, targets[key])
    }
    for key in HOPF_KEYS
  }
  rows = []
  seen_blocks = set()
  seen_steps = set()

  for position, argument_index, argument in _ordered_active_argument_rows(arguments):
    visible = _visible_non_exact_steps(
      presentation, blocks, semantic_sidecar, arguments, argument_index, argument
    )
    for key in HOPF_KEYS:
      matches = tuple(
        (block, step)
        for block, step in visible
        if id(step) in matching_by_key[key]
      )
      if not matches:
        rows.append(
          HopfDedupAudit(
            key=key,
            ordered_position=position,
            argument_index=argument_index,
            argument_role=argument.role.value,
            visible=False,
            block_assembly_kept=False,
            step_assembly_kept=False,
            released_by_step_dedup=False,
          )
        )
        continue
      block_kept = any(id(block) not in seen_blocks for block, step in matches)
      step_kept = any(id(step) not in seen_steps for block, step in matches)
      rows.append(
        HopfDedupAudit(
          key=key,
          ordered_position=position,
          argument_index=argument_index,
          argument_role=argument.role.value,
          visible=True,
          block_assembly_kept=block_kept,
          step_assembly_kept=step_kept,
          released_by_step_dedup=step_kept and not block_kept,
        )
      )
    seen_blocks.update(id(block) for block, step in visible)
    seen_steps.update(id(step) for block, step in visible)

  return tuple(rows)


def print_audit():
  groups = build_group_dedup_audit()
  hopf = build_pi6_hopf_dedup_audit()

  print("=" * 78)
  print("Phase 144-6-R5-32 visible contribution assembly / dedup audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. pi_6^3 Hopf facts under hypothetical step-level visible dedup")
  print("-" * 78)
  for row in hopf:
    print(
      f"{row.key}: ordered_position={row.ordered_position} "
      f"argument={row.argument_index} role={row.argument_role} "
      f"visible={row.visible} block_kept={row.block_assembly_kept} "
      f"step_kept={row.step_assembly_kept} "
      f"released={row.released_by_step_dedup}"
    )

  print("\\nB. Six-group visible non-exact assembly inventory")
  print("-" * 78)
  totals = [0, 0, 0, 0, 0, 0]
  for row in groups:
    print(
      f"pi_{row.n + row.k}^{row.n}: "
      f"visible_occurrences={row.visible_occurrences} "
      f"block_kept={row.block_assembly_kept_occurrences} "
      f"step_kept={row.step_assembly_kept_occurrences} "
      f"released={row.released_occurrences} "
      f"repeated_visible={row.repeated_visible_occurrences} "
      f"unique_visible={row.unique_visible_steps}"
    )
    values = (
      row.visible_occurrences,
      row.block_assembly_kept_occurrences,
      row.step_assembly_kept_occurrences,
      row.released_occurrences,
      row.repeated_visible_occurrences,
      row.unique_visible_steps,
    )
    totals = [left + right for left, right in zip(totals, values)]
  print(
    "totals: visible_occurrences={} block_kept={} step_kept={} "
    "released={} repeated_visible={} unique_visible={}".format(*totals)
  )

  print("\\nC. Exactness boundary")
  print("-" * 78)
  print(
    "This hypothetical step-level dedup applies only to visible NON-EXACT "
    "ProofSteps. Existing exactness contribution keys remain outside this "
    "audit and are not replaced."
  )

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "A production change is justified only if step-level visible dedup "
    "preserves required contributions without creating broad repeated output. "
    "This audit does not change renderer behavior."
  )


if __name__ == "__main__":
  print_audit()
