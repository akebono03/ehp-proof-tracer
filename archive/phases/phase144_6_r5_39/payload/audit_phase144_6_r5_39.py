from collections import Counter, defaultdict
from dataclasses import dataclass

from audit_phase144_6_r5_38 import (
  build_explanatory_contribution_groups,
  build_visibility_occurrences,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


@dataclass(frozen=True)
class NarrativeNecessityRecord:
  n: int
  k: int
  statement_type: str
  occurrence_count: int
  owner_argument_index: int
  owner_argument_role: str
  provider_key_count: int
  anchor_owned: bool
  bridges_visibility_contributions: bool
  downstream_visibility_count: int
  structural_role: str
  pi6_dedicated_render_present: bool | None


def _group_key_from_occurrence(row):
  return (
    row.n,
    row.k,
    row.statement_type,
    row.statement_repr,
    row.provider_keys,
  )


def _argument_edges(presentation):
  children = defaultdict(set)
  for edge in presentation.edges:
    children[id(edge.premise_step)].add(id(edge.parent_step))
  return children


def _reachable_visibility_steps(start_step_id, visible_ids, children):
  found = set()
  stack = list(children.get(start_step_id, ()))
  seen = set()
  while stack:
    step_id = stack.pop()
    if step_id in seen:
      continue
    seen.add(step_id)
    if step_id in visible_ids:
      found.add(step_id)
    stack.extend(children.get(step_id, ()))
  return found


def build_narrative_necessity_inventory():
  occurrences = build_visibility_occurrences()
  groups = build_explanatory_contribution_groups()
  occurrences_by_group = defaultdict(list)
  for row in occurrences:
    occurrences_by_group[_group_key_from_occurrence(row)].append(row)

  pi6_presentation = _context(3, 3)[0]
  pi6_dedicated = render_toda_group_proof_narrative_markdown(
    pi6_presentation
  )

  records = []
  for group in groups:
    key = (
      group.n,
      group.k,
      group.statement_type,
      group.statement_repr,
      group.provider_keys,
    )
    rows = occurrences_by_group[key]
    owner = next(
      row
      for row in rows
      if (
        row.argument_index == group.owner_argument_index
        and row.argument_role == group.owner_argument_role
      )
    )

    presentation = _context(group.n, group.k)[0]
    children = _argument_edges(presentation)
    same_argument_ids = {
      row.step_id
      for row in occurrences
      if (
        row.n == group.n
        and row.k == group.k
        and row.argument_index == owner.argument_index
      )
    }
    downstream = _reachable_visibility_steps(
      owner.step_id,
      same_argument_ids - {owner.step_id},
      children,
    )
    bridge = bool(downstream)
    anchor_owned = owner.provider_anchor

    if anchor_owned:
      structural_role = "explicit_prerequisite_candidate"
    elif bridge:
      structural_role = "bridge_candidate"
    else:
      structural_role = "derivation_detail_candidate"

    dedicated_present = None
    if (group.n, group.k) == (3, 3):
      normalized_render = "".join(owner.step_render.split())
      normalized_dedicated = "".join(pi6_dedicated.split())
      dedicated_present = normalized_render in normalized_dedicated

    records.append(
      NarrativeNecessityRecord(
        n=group.n,
        k=group.k,
        statement_type=group.statement_type,
        occurrence_count=group.occurrence_count,
        owner_argument_index=group.owner_argument_index,
        owner_argument_role=group.owner_argument_role,
        provider_key_count=len(group.provider_keys),
        anchor_owned=anchor_owned,
        bridges_visibility_contributions=bridge,
        downstream_visibility_count=len(downstream),
        structural_role=structural_role,
        pi6_dedicated_render_present=dedicated_present,
      )
    )
  return tuple(records)


def print_audit():
  rows = build_narrative_necessity_inventory()

  print("=" * 78)
  print("Phase 144-6-R5-39 explanatory contribution narrative-necessity audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. Six-group structural narrative-role candidates")
  print("-" * 78)
  for n, k in TARGETS:
    group_rows = tuple(row for row in rows if (row.n, row.k) == (n, k))
    counts = Counter(row.structural_role for row in group_rows)
    print(
      f"pi_{n + k}^{n}: contributions={len(group_rows)} "
      f"explicit_prerequisite={counts['explicit_prerequisite_candidate']} "
      f"bridge={counts['bridge_candidate']} "
      f"derivation_detail={counts['derivation_detail_candidate']}"
    )
  counts = Counter(row.structural_role for row in rows)
  print(
    f"totals: contributions={len(rows)} "
    f"explicit_prerequisite={counts['explicit_prerequisite_candidate']} "
    f"bridge={counts['bridge_candidate']} "
    f"derivation_detail={counts['derivation_detail_candidate']}"
  )

  print("\\nB. Statement types by structural role")
  print("-" * 78)
  for role in (
    "explicit_prerequisite_candidate",
    "bridge_candidate",
    "derivation_detail_candidate",
  ):
    print(role)
    role_rows = tuple(row for row in rows if row.structural_role == role)
    for name, count in Counter(row.statement_type for row in role_rows).most_common(30):
      print(f"{count:4d}  {name}")

  print("\\nC. Owner roles by structural role")
  print("-" * 78)
  for role in (
    "explicit_prerequisite_candidate",
    "bridge_candidate",
    "derivation_detail_candidate",
  ):
    role_rows = tuple(row for row in rows if row.structural_role == role)
    print(role)
    for name, count in Counter(row.owner_argument_role for row in role_rows).most_common():
      print(f"{count:4d}  {name}")

  print("\\nD. pi_6^3 dedicated Narrative comparison")
  print("-" * 78)
  pi6 = tuple(row for row in rows if (row.n, row.k) == (3, 3))
  for row in pi6:
    print(
      f"type={row.statement_type} role={row.structural_role} "
      f"owner={row.owner_argument_index}:{row.owner_argument_role} "
      f"providers={row.provider_key_count} "
      f"downstream_visibility={row.downstream_visibility_count} "
      f"dedicated_render_present={row.pi6_dedicated_render_present}"
    )
  print(
    "pi6 summary: "
    f"present={sum(row.pi6_dedicated_render_present is True for row in pi6)} "
    f"absent={sum(row.pi6_dedicated_render_present is False for row in pi6)}"
  )

  print("\\nE. Bridge depth")
  print("-" * 78)
  bridge_rows = tuple(row for row in rows if row.bridges_visibility_contributions)
  for count, frequency in sorted(
    Counter(row.downstream_visibility_count for row in bridge_rows).items()
  ):
    print(f"{frequency:4d} bridges with {count} downstream visibility contributions")

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "These are structural narrative-role candidates, not production display "
    "decisions. Direct-anchor ownership suggests an explicit prerequisite; "
    "a non-anchor contribution with downstream visibility contributions is a "
    "bridge candidate; remaining contributions are derivation-detail candidates."
  )
  print(
    "The pi_6^3 dedicated Narrative is used only as a comparison baseline. "
    "Its wording is not encoded as a generic rule."
  )
  print(
    "No production visibility, ownership, renderer, ProofChain, deduplication, "
    "membership, parity matcher, or public route is changed."
  )


if __name__ == "__main__":
  print_audit()
