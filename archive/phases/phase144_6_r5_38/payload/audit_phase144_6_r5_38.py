from collections import Counter, defaultdict
from dataclasses import dataclass

from audit_phase144_6_r5_35 import (
  _effective_hidden_ids,
  _local_body,
  _necessity_for_chain,
)
from audit_phase144_6_r5_37 import (
  _is_rendering_fallback,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)


@dataclass(frozen=True)
class VisibilityOccurrence:
  n: int
  k: int
  argument_index: int
  argument_role: str
  block_role: str
  statement_type: str
  statement_repr: str
  provider_anchor: bool
  distance_to_conclusion: int | None
  step_render: str
  step_id: int
  provider_keys: tuple[str, ...]


@dataclass(frozen=True)
class ContributionGroup:
  n: int
  k: int
  statement_type: str
  statement_repr: str
  provider_keys: tuple[str, ...]
  occurrence_count: int
  argument_indices: tuple[int, ...]
  argument_roles: tuple[str, ...]
  anchor_occurrences: int
  chain_occurrences: int
  owner_argument_index: int
  owner_argument_role: str


def _provider_key(provider):
  if provider.supporting_block is not None:
    return "block:" + str(id(provider.supporting_block))
  return "child_argument:" + str(provider.child_argument_index)


def _provider_keys_for_step(
  presentation,
  local_body,
  proof_chain,
  conclusion_step,
  step_id,
):
  keys = []
  for provider in proof_chain.providers:
    if provider.supporting_block is None:
      continue
    provider_chain = type(proof_chain)(
      argument_index=proof_chain.argument_index,
      argument=proof_chain.argument,
      providers=(provider,),
    )
    chain_ids, anchors, distances, reachable, necessity = _necessity_for_chain(
      presentation,
      local_body,
      provider_chain,
      conclusion_step,
    )
    if step_id in chain_ids:
      keys.append(_provider_key(provider))
  return tuple(keys)


def build_visibility_occurrences():
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
      hidden_ids = _effective_hidden_ids(
        presentation,
        blocks,
        body,
        semantic_sidecar,
        argument,
      )
      chain_ids, anchors, distances, reachable, necessity = _necessity_for_chain(
        presentation,
        body,
        proof_chains[argument_index],
        conclusion_step,
      )
      block_by_id = {
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
        if not necessity.get(step_id, ()):
          continue
        step = step_by_id.get(step_id)
        block = block_by_id.get(step_id)
        if step is None or block is None:
          continue
        rendered = _render_generic_narrative_step(step)
        if _is_rendering_fallback(step, rendered):
          continue
        rows.append(
          VisibilityOccurrence(
            n=n,
            k=k,
            argument_index=argument_index,
            argument_role=argument.role.value,
            block_role=block.role.value,
            statement_type=type(step.conclusion).__name__,
            statement_repr=repr(step.conclusion),
            provider_anchor=step_id in anchors,
            distance_to_conclusion=distances.get(step_id),
            step_render=rendered,
            step_id=step_id,
            provider_keys=_provider_keys_for_step(
              presentation,
              body,
              proof_chains[argument_index],
              conclusion_step,
              step_id,
            ),
          )
        )
  return tuple(rows)


def _owner(rows):
  ordered = sorted(
    rows,
    key=lambda row: (
      0 if row.provider_anchor else 1,
      row.distance_to_conclusion
      if row.distance_to_conclusion is not None
      else 10**9,
      row.argument_index,
    ),
  )
  return ordered[0]


def build_explanatory_contribution_groups():
  occurrences = build_visibility_occurrences()
  grouped = defaultdict(list)
  for row in occurrences:
    key = (
      row.n,
      row.k,
      row.statement_type,
      row.statement_repr,
      row.provider_keys,
    )
    grouped[key].append(row)

  groups = []
  for (
    n,
    k,
    statement_type,
    statement_repr,
    provider_keys,
  ), rows in grouped.items():
    owner = _owner(rows)
    groups.append(
      ContributionGroup(
        n=n,
        k=k,
        statement_type=statement_type,
        statement_repr=statement_repr,
        provider_keys=provider_keys,
        occurrence_count=len(rows),
        argument_indices=tuple(sorted({row.argument_index for row in rows})),
        argument_roles=tuple(sorted({row.argument_role for row in rows})),
        anchor_occurrences=sum(row.provider_anchor for row in rows),
        chain_occurrences=sum(not row.provider_anchor for row in rows),
        owner_argument_index=owner.argument_index,
        owner_argument_role=owner.argument_role,
      )
    )
  return tuple(groups)


def print_audit():
  occurrences = build_visibility_occurrences()
  groups = build_explanatory_contribution_groups()

  print("=" * 78)
  print("Phase 144-6-R5-38 visibility-gap explanatory contribution dedup/ownership audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. Six-group dedup")
  print("-" * 78)
  for n, k in TARGETS:
    occ = tuple(row for row in occurrences if (row.n, row.k) == (n, k))
    grp = tuple(row for row in groups if (row.n, row.k) == (n, k))
    print(
      f"pi_{n + k}^{n}: visibility_occurrences={len(occ)} "
      f"contribution_groups={len(grp)} dedup={len(occ)-len(grp)}"
    )
  print(
    f"totals: visibility_occurrences={len(occurrences)} "
    f"contribution_groups={len(groups)} "
    f"dedup={len(occurrences)-len(groups)}"
  )

  print("\\nB. Multiplicity")
  print("-" * 78)
  for multiplicity, count in sorted(
    Counter(group.occurrence_count for group in groups).items()
  ):
    print(f"{count:4d} groups x {multiplicity} occurrences")

  print("\\nC. Cross-Argument ownership")
  print("-" * 78)
  cross = tuple(group for group in groups if len(group.argument_indices) > 1)
  print(
    f"cross_argument_groups={len(cross)} "
    f"single_argument_groups={len(groups)-len(cross)}"
  )
  print("Owner roles")
  for role, count in Counter(group.owner_argument_role for group in groups).most_common():
    print(f"{count:4d}  {role}")

  print("\\nD. Statement types after dedup")
  print("-" * 78)
  for name, count in Counter(group.statement_type for group in groups).most_common(40):
    print(f"{count:4d}  {name}")

  print("\\nE. Provider-key cardinality")
  print("-" * 78)
  for cardinality, count in sorted(
    Counter(len(group.provider_keys) for group in groups).items()
  ):
    print(f"{count:4d} groups with {cardinality} provider keys")

  print("\\nF. High-multiplicity contribution examples")
  print("-" * 78)
  examples = sorted(
    groups,
    key=lambda group: (-group.occurrence_count, group.n, group.k),
  )[:30]
  for group in examples:
    print(
      f"pi_{group.n + group.k}^{group.n}: "
      f"occ={group.occurrence_count} args={group.argument_indices} "
      f"owner={group.owner_argument_index}:{group.owner_argument_role} "
      f"anchors={group.anchor_occurrences} chains={group.chain_occurrences} "
      f"providers={len(group.provider_keys)} type={group.statement_type}"
    )

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "A contribution group is keyed by group, exact statement semantics, and "
    "the direct SUPPORTING_BLOCK provider set whose anchored chain contains "
    "the step. This distinguishes the same mathematical statement used for "
    "different explanatory providers."
  )
  print(
    "Ownership is diagnostic only: prefer a direct-anchor occurrence, then "
    "shorter distance to the Argument conclusion, then earlier Argument index."
  )
  print(
    "No production ownership, visibility, renderer, ProofChain, deduplication, "
    "membership, parity matcher, or public route is changed."
  )


if __name__ == "__main__":
  print_audit()
