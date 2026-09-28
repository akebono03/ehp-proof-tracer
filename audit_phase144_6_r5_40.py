from collections import Counter, defaultdict
from dataclasses import dataclass

from audit_phase144_6_r5_38 import ContributionGroup, _owner, build_visibility_occurrences
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import TARGETS, _context


@dataclass(frozen=True)
class PlacementRecord:
  n: int
  k: int
  statement_type: str
  structural_role: str
  owner_argument_index: int
  owner_argument_role: str
  provider_key_count: int
  provider_anchor: bool
  distance_to_conclusion: int | None
  dependency_predecessor_count: int
  dependency_successor_count: int
  placement_class: str


def _group_key(row):
  return (row.n, row.k, row.statement_type, row.statement_repr, row.provider_keys)


def _build_groups(occurrences):
  grouped = defaultdict(list)
  for row in occurrences:
    grouped[_group_key(row)].append(row)
  groups = []
  owners = {}
  for key, rows in grouped.items():
    owner = _owner(rows)
    n, k, statement_type, statement_repr, provider_keys = key
    groups.append(ContributionGroup(
      n=n, k=k, statement_type=statement_type, statement_repr=statement_repr,
      provider_keys=provider_keys, occurrence_count=len(rows),
      argument_indices=tuple(sorted({row.argument_index for row in rows})),
      argument_roles=tuple(sorted({row.argument_role for row in rows})),
      anchor_occurrences=sum(row.provider_anchor for row in rows),
      chain_occurrences=sum(not row.provider_anchor for row in rows),
      owner_argument_index=owner.argument_index, owner_argument_role=owner.argument_role,
    ))
    owners[key] = owner
  return tuple(groups), owners


def _children_by_step_id(presentation):
  children = defaultdict(set)
  for edge in presentation.edges:
    children[id(edge.premise_step)].add(id(edge.parent_step))
  return children


def _reachable(start_id, target_id, children):
  if start_id == target_id:
    return False
  stack = list(children.get(start_id, ()))
  seen = set()
  while stack:
    current = stack.pop()
    if current == target_id:
      return True
    if current in seen:
      continue
    seen.add(current)
    stack.extend(children.get(current, ()))
  return False


def build_placement_inventory():
  occurrences = build_visibility_occurrences()
  groups, owners = _build_groups(occurrences)
  presentations = {(n, k): _context(n, k)[0] for n, k in TARGETS}
  children_by_group = {
    key: _children_by_step_id(presentation)
    for key, presentation in presentations.items()
  }
  selected = []
  for group in groups:
    key = (group.n, group.k, group.statement_type, group.statement_repr, group.provider_keys)
    owner = owners[key]
    children = children_by_group[(group.n, group.k)]
    same_argument_rows = tuple(
      row for row in occurrences
      if row.n == group.n and row.k == group.k and row.argument_index == owner.argument_index
    )
    downstream = {
      row.step_id for row in same_argument_rows
      if row.step_id != owner.step_id and _reachable(owner.step_id, row.step_id, children)
    }
    if owner.provider_anchor:
      structural_role = "explicit_prerequisite_candidate"
    elif downstream:
      structural_role = "bridge_candidate"
    else:
      structural_role = "derivation_detail_candidate"
    if structural_role != "derivation_detail_candidate":
      selected.append((group, owner, structural_role))

  by_owner_argument = defaultdict(list)
  for item in selected:
    group, owner, _ = item
    by_owner_argument[(group.n, group.k, owner.argument_index)].append(item)

  records = []
  for group, owner, structural_role in selected:
    children = children_by_group[(group.n, group.k)]
    peers = by_owner_argument[(group.n, group.k, owner.argument_index)]
    predecessors = 0
    successors = 0
    for _, peer_owner, _ in peers:
      if peer_owner.step_id == owner.step_id:
        continue
      if _reachable(peer_owner.step_id, owner.step_id, children):
        predecessors += 1
      if _reachable(owner.step_id, peer_owner.step_id, children):
        successors += 1
    if owner.provider_anchor:
      placement = "at_provider_anchor"
    elif successors:
      placement = "before_dependent_contribution"
    else:
      placement = "before_argument_conclusion"
    records.append(PlacementRecord(
      n=group.n, k=group.k, statement_type=group.statement_type,
      structural_role=structural_role, owner_argument_index=owner.argument_index,
      owner_argument_role=owner.argument_role, provider_key_count=len(group.provider_keys),
      provider_anchor=owner.provider_anchor, distance_to_conclusion=owner.distance_to_conclusion,
      dependency_predecessor_count=predecessors, dependency_successor_count=successors,
      placement_class=placement,
    ))
  return tuple(records)


def print_audit():
  rows = build_placement_inventory()
  print("=" * 78)
  print("Phase 144-6-R5-40 Narrative contribution placement/order audit")
  print("production changes: none")
  print("=" * 78)
  print("\nA. Six-group placement classes")
  print("-" * 78)
  for n, k in TARGETS:
    rs = tuple(r for r in rows if (r.n, r.k) == (n, k))
    c = Counter(r.placement_class for r in rs)
    print(f"pi_{n+k}^{n}: selected={len(rs)} anchor={c['at_provider_anchor']} before_dependent={c['before_dependent_contribution']} before_conclusion={c['before_argument_conclusion']}")
  c = Counter(r.placement_class for r in rows)
  print(f"totals: selected={len(rows)} anchor={c['at_provider_anchor']} before_dependent={c['before_dependent_contribution']} before_conclusion={c['before_argument_conclusion']}")

  print("\nB. Structural role x placement")
  print("-" * 78)
  for key, count in sorted(Counter((r.structural_role, r.placement_class) for r in rows).items()):
    print(f"{count:4d}  {key[0]} -> {key[1]}")

  print("\nC. Owner Argument concentration")
  print("-" * 78)
  owners = Counter((r.n, r.k, r.owner_argument_index, r.owner_argument_role) for r in rows)
  for (n, k, index, role), count in owners.most_common():
    if count >= 2:
      print(f"pi_{n+k}^{n} arg={index}:{role} contributions={count}")

  print("\nD. Dependency-order evidence")
  print("-" * 78)
  print(f"with_predecessor={sum(r.dependency_predecessor_count > 0 for r in rows)}")
  print(f"with_successor={sum(r.dependency_successor_count > 0 for r in rows)}")
  print(f"isolated_in_selected_set={sum(r.dependency_predecessor_count == 0 and r.dependency_successor_count == 0 for r in rows)}")

  print("\nE. pi_6^3 placement/order")
  print("-" * 78)
  for index, r in enumerate((r for r in rows if (r.n, r.k) == (3, 3)), start=1):
    print(f"{index}. type={r.statement_type} owner={r.owner_argument_index}:{r.owner_argument_role} placement={r.placement_class} distance={r.distance_to_conclusion} predecessors={r.dependency_predecessor_count} successors={r.dependency_successor_count} providers={r.provider_key_count}")

  print("\nF. Statement types by placement")
  print("-" * 78)
  for placement in ("at_provider_anchor", "before_dependent_contribution", "before_argument_conclusion"):
    print(placement)
    for name, count in Counter(r.statement_type for r in rows if r.placement_class == placement).most_common(20):
      print(f"{count:4d}  {name}")

  print("\nDecision boundary")
  print("-" * 78)
  print("Placement classes are diagnostic only; they do not insert hidden contributions or define final prose order.")
  print("No production visibility, ownership, renderer, ProofChain, deduplication, membership, parity matcher, public route, or dedicated pi_6^3 renderer is changed.")


if __name__ == "__main__":
  print_audit()
