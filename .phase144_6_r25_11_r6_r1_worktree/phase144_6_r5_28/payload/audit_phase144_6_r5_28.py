from collections import defaultdict
from dataclasses import dataclass

from audit_phase144_6_r5_23 import (
  _canonical_fact_targets,
  _step_contains_target,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_proof_chains import (
  TodaGroupProofNarrativeProofChainProviderKind,
)


MISSING_6_KEYS = (
  "hopf_nu_prime",
  "pi5_3_group",
  "hopf_nu_eta6",
  "pi7_5_group",
  "hopf_pi7_surjective",
  "delta_zero",
)


@dataclass(frozen=True)
class OwnershipCandidate:
  key: str
  argument_index: int
  argument_role: str
  discourse_position: int
  in_local_body: bool
  in_direct_supporting_provider: bool
  in_child_argument_conclusion: bool
  is_direct_conclusion_premise: bool
  is_argument_conclusion: bool


@dataclass(frozen=True)
class OwnershipInventory:
  n: int
  k: int
  arguments: int
  local_body_step_occurrences: int
  multi_argument_step_identities: int
  direct_provider_step_occurrences: int
  multi_provider_step_identities: int


def _local_bodies(presentation, blocks, semantic_sidecar, arguments):
  return tuple(
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      i,
    )
    for i in range(len(arguments))
  )


def build_missing6_ownership_candidates():
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
    presentation, blocks, semantic_sidecar, arguments
  )
  ordered = order_toda_group_proof_narrative_arguments(arguments)
  discourse_position = {
    id(argument): position
    for position, argument in enumerate(ordered)
  }

  candidates = []

  for key in MISSING_6_KEYS:
    matching_steps = tuple(
      dict.fromkeys(
        step
        for block in blocks
        for step in block.steps
        if _step_contains_target(step, targets[key])
      )
    )

    for argument_index, argument in enumerate(arguments):
      conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
      local_ids = {
        id(step)
        for block in local_bodies[argument_index]
        for step in block.steps
      }
      direct_provider_ids = {
        id(step)
        for provider in proof_chains[argument_index].providers
        if (
          provider.kind
          is TodaGroupProofNarrativeProofChainProviderKind.SUPPORTING_BLOCK
        )
        for step in provider.supporting_block.steps
      }
      child_conclusion_ids = {
        id(step)
        for provider in proof_chains[argument_index].providers
        if (
          provider.kind
          is TodaGroupProofNarrativeProofChainProviderKind.CHILD_ARGUMENT
        )
        for step in arguments[
          provider.child_argument_index
        ].conclusion_block.steps
      }
      direct_premise_ids = (
        set()
        if conclusion_step is None
        else {id(step) for step in conclusion_step.premises}
      )

      if not any(id(step) in local_ids for step in matching_steps):
        continue

      candidates.append(
        OwnershipCandidate(
          key=key,
          argument_index=argument_index,
          argument_role=argument.role.value,
          discourse_position=discourse_position[id(argument)],
          in_local_body=True,
          in_direct_supporting_provider=any(
            id(step) in direct_provider_ids
            for step in matching_steps
          ),
          in_child_argument_conclusion=any(
            id(step) in child_conclusion_ids
            for step in matching_steps
          ),
          is_direct_conclusion_premise=any(
            id(step) in direct_premise_ids
            for step in matching_steps
          ),
          is_argument_conclusion=(
            conclusion_step is not None
            and any(step is conclusion_step for step in matching_steps)
          ),
        )
      )

  return tuple(candidates)


def build_six_group_ownership_inventory():
  inventory = []

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
      presentation, blocks, semantic_sidecar, arguments
    )

    local_owners = defaultdict(set)
    local_occurrences = 0
    provider_owners = defaultdict(set)
    provider_occurrences = 0

    for argument_index, body in enumerate(local_bodies):
      for block in body:
        for step in block.steps:
          local_occurrences += 1
          local_owners[id(step)].add(argument_index)

    for argument_index, chain in enumerate(proof_chains):
      for provider in chain.providers:
        if (
          provider.kind
          is not TodaGroupProofNarrativeProofChainProviderKind.SUPPORTING_BLOCK
        ):
          continue
        for step in provider.supporting_block.steps:
          provider_occurrences += 1
          provider_owners[id(step)].add(argument_index)

    inventory.append(
      OwnershipInventory(
        n=n,
        k=k,
        arguments=len(arguments),
        local_body_step_occurrences=local_occurrences,
        multi_argument_step_identities=sum(
          len(owners) > 1 for owners in local_owners.values()
        ),
        direct_provider_step_occurrences=provider_occurrences,
        multi_provider_step_identities=sum(
          len(owners) > 1 for owners in provider_owners.values()
        ),
      )
    )

  return tuple(inventory)


def _candidate_owner_rule(candidate):
  if candidate.is_argument_conclusion:
    return 0
  if candidate.is_direct_conclusion_premise:
    return 1
  if candidate.in_child_argument_conclusion:
    return 2
  if candidate.in_direct_supporting_provider:
    return 3
  return 4


def build_missing6_owner_selection():
  candidates = build_missing6_ownership_candidates()
  selected = {}

  for key in MISSING_6_KEYS:
    key_candidates = tuple(
      candidate for candidate in candidates if candidate.key == key
    )
    if not key_candidates:
      selected[key] = None
      continue

    selected[key] = min(
      key_candidates,
      key=lambda candidate: (
        _candidate_owner_rule(candidate),
        candidate.discourse_position,
        candidate.argument_index,
      ),
    )

  return selected


def print_audit():
  candidates = build_missing6_ownership_candidates()
  inventory = build_six_group_ownership_inventory()
  selected = build_missing6_owner_selection()

  print("=" * 78)
  print("Phase 144-6-R5-28 Narrative contribution ownership audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. pi_6^3 missing-6 ownership candidates")
  print("-" * 78)
  for key in MISSING_6_KEYS:
    print(key)
    for candidate in candidates:
      if candidate.key != key:
        continue
      print(
        f"  argument={candidate.argument_index} "
        f"role={candidate.argument_role} "
        f"discourse={candidate.discourse_position} "
        f"supporting_provider={candidate.in_direct_supporting_provider} "
        f"child_conclusion={candidate.in_child_argument_conclusion} "
        f"direct_premise={candidate.is_direct_conclusion_premise} "
        f"argument_conclusion={candidate.is_argument_conclusion}"
      )

  print("\\nB. Six-group ownership ambiguity inventory")
  print("-" * 78)
  totals = [0, 0, 0, 0]
  for item in inventory:
    totals[0] += item.local_body_step_occurrences
    totals[1] += item.multi_argument_step_identities
    totals[2] += item.direct_provider_step_occurrences
    totals[3] += item.multi_provider_step_identities
    print(
      f"pi_{item.n + item.k}^{item.n}: "
      f"arguments={item.arguments} "
      f"local_occurrences={item.local_body_step_occurrences} "
      f"multi_argument_steps={item.multi_argument_step_identities} "
      f"provider_occurrences={item.direct_provider_step_occurrences} "
      f"multi_provider_steps={item.multi_provider_step_identities}"
    )
  print(
    "totals: "
    f"local_occurrences={totals[0]} "
    f"multi_argument_steps={totals[1]} "
    f"provider_occurrences={totals[2]} "
    f"multi_provider_steps={totals[3]}"
  )

  print("\\nC. Hypothetical structural owner selection")
  print("-" * 78)
  print(
    "priority: argument_conclusion > direct_premise > child_conclusion "
    "> direct_supporting_provider > local_body; tie-break by discourse order"
  )
  for key in MISSING_6_KEYS:
    owner = selected[key]
    if owner is None:
      print(f"{key}: owner=None")
      continue
    print(
      f"{key}: argument={owner.argument_index} "
      f"role={owner.argument_role} discourse={owner.discourse_position} "
      f"class={_candidate_owner_rule(owner)}"
    )

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "This is an ownership audit, not a visibility implementation. "
    "The priority rule is hypothetical and must not be treated as production semantics."
  )
  print(
    "A useful ownership model must assign the missing facts without turning "
    "every shared local-body dependency into a displayed contribution."
  )
  print(
    "Embedded nu-prime eta_6 membership remains outside the missing-6 ownership audit."
  )


if __name__ == "__main__":
  print_audit()
