from collections import Counter, defaultdict
from dataclasses import dataclass

from audit_phase144_6_r5_38 import _owner, build_visibility_occurrences
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import TARGETS, _context


@dataclass(frozen=True)
class ContributionNode:
  key: tuple
  n: int
  k: int
  statement_type: str
  owner_argument_index: int
  owner_argument_role: str
  step_id: int
  provider_anchor: bool
  distance_to_conclusion: int | None
  provider_keys: tuple[str, ...]


@dataclass(frozen=True)
class ArgumentOrderAudit:
  n: int
  k: int
  argument_index: int
  argument_role: str
  node_count: int
  edge_count: int
  unique_topological_order: bool
  max_ready_width: int
  tie_break_steps: int
  stable_order_keys: tuple[tuple, ...]


def _children(presentation):
  result = defaultdict(set)
  for edge in presentation.edges:
    result[id(edge.premise_step)].add(id(edge.parent_step))
  return result


def _reachable(source, target, children):
  if source == target:
    return False
  stack = list(children.get(source, ()))
  seen = set()
  while stack:
    current = stack.pop()
    if current == target:
      return True
    if current in seen:
      continue
    seen.add(current)
    stack.extend(children.get(current, ()))
  return False


def _selected_nodes():
  occurrences = build_visibility_occurrences()
  grouped = defaultdict(list)
  for row in occurrences:
    grouped[(row.n, row.k, row.statement_type, row.statement_repr, row.provider_keys)].append(row)

  presentations = {(n, k): _context(n, k)[0] for n, k in TARGETS}
  children_by_group = {key: _children(value) for key, value in presentations.items()}
  nodes = []

  for key, rows in grouped.items():
    owner = _owner(rows)
    n, k, statement_type, statement_repr, provider_keys = key
    children = children_by_group[(n, k)]
    same_argument = tuple(
      row for row in occurrences
      if row.n == n and row.k == k and row.argument_index == owner.argument_index
    )
    downstream = any(
      row.step_id != owner.step_id and _reachable(owner.step_id, row.step_id, children)
      for row in same_argument
    )
    if not owner.provider_anchor and not downstream:
      continue
    nodes.append(ContributionNode(
      key=key,
      n=n,
      k=k,
      statement_type=statement_type,
      owner_argument_index=owner.argument_index,
      owner_argument_role=owner.argument_role,
      step_id=owner.step_id,
      provider_anchor=owner.provider_anchor,
      distance_to_conclusion=owner.distance_to_conclusion,
      provider_keys=provider_keys,
    ))
  return tuple(nodes), presentations, children_by_group


def _stable_key(node):
  return (
    node.distance_to_conclusion if node.distance_to_conclusion is not None else 10**9,
    0 if node.provider_anchor else 1,
    node.statement_type,
    repr(node.key),
  )


def build_topological_order_audit():
  nodes, presentations, children_by_group = _selected_nodes()
  by_argument = defaultdict(list)
  for node in nodes:
    by_argument[(node.n, node.k, node.owner_argument_index, node.owner_argument_role)].append(node)

  audits = []
  for (n, k, argument_index, argument_role), argument_nodes in by_argument.items():
    children = children_by_group[(n, k)]
    node_by_key = {node.key: node for node in argument_nodes}
    successors = {node.key: set() for node in argument_nodes}
    indegree = {node.key: 0 for node in argument_nodes}

    for left in argument_nodes:
      for right in argument_nodes:
        if left.key == right.key:
          continue
        if _reachable(left.step_id, right.step_id, children):
          successors[left.key].add(right.key)

    # Use transitive reachability as the partial order. Indegree therefore
    # counts all selected predecessors, which is valid for Kahn readiness.
    for source, targets in successors.items():
      for target in targets:
        indegree[target] += 1

    remaining = set(node_by_key)
    stable_order = []
    max_ready_width = 0
    tie_break_steps = 0
    unique = True

    while remaining:
      ready = [key for key in remaining if indegree[key] == 0]
      if not ready:
        raise AssertionError("selected contribution dependency cycle")
      max_ready_width = max(max_ready_width, len(ready))
      if len(ready) != 1:
        unique = False
        tie_break_steps += 1
      ready.sort(key=lambda key: _stable_key(node_by_key[key]))
      chosen = ready[0]
      stable_order.append(chosen)
      remaining.remove(chosen)
      for target in successors[chosen]:
        if target in remaining:
          indegree[target] -= 1

    audits.append(ArgumentOrderAudit(
      n=n,
      k=k,
      argument_index=argument_index,
      argument_role=argument_role,
      node_count=len(argument_nodes),
      edge_count=sum(len(targets) for targets in successors.values()),
      unique_topological_order=unique,
      max_ready_width=max_ready_width,
      tie_break_steps=tie_break_steps,
      stable_order_keys=tuple(stable_order),
    ))

  return tuple(audits), nodes


def print_audit():
  audits, nodes = build_topological_order_audit()
  print("=" * 78)
  print("Phase 144-6-R5-41 contribution topological-order determinism audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. Six-group determinism summary")
  print("-" * 78)
  for n, k in TARGETS:
    rows = tuple(a for a in audits if (a.n, a.k) == (n, k))
    multi = tuple(a for a in rows if a.node_count > 1)
    print(
      f"pi_{n+k}^{n}: arguments={len(rows)} multi={len(multi)} "
      f"unique={sum(a.unique_topological_order for a in multi)} "
      f"tie_break={sum(not a.unique_topological_order for a in multi)} "
      f"max_width={max((a.max_ready_width for a in rows), default=0)}"
    )

  print("\\nB. Multi-contribution Arguments")
  print("-" * 78)
  for a in sorted(
    (a for a in audits if a.node_count > 1),
    key=lambda x: (x.n, x.k, x.argument_index),
  ):
    print(
      f"pi_{a.n+a.k}^{a.n} arg={a.argument_index}:{a.argument_role} "
      f"nodes={a.node_count} edges={a.edge_count} "
      f"unique={a.unique_topological_order} "
      f"max_ready_width={a.max_ready_width} tie_break_steps={a.tie_break_steps}"
    )

  print("\\nC. Tie-break width distribution")
  print("-" * 78)
  for width, count in sorted(Counter(a.max_ready_width for a in audits if a.node_count > 1).items()):
    print(f"width={width}: {count} arguments")

  print("\\nD. pi_6^3 determinism")
  print("-" * 78)
  pi6 = tuple(a for a in audits if (a.n, a.k) == (3, 3))
  for a in pi6:
    print(
      f"arg={a.argument_index}:{a.argument_role} nodes={a.node_count} "
      f"edges={a.edge_count} unique={a.unique_topological_order} "
      f"max_ready_width={a.max_ready_width} tie_break_steps={a.tie_break_steps}"
    )
    node_by_key = {node.key: node for node in nodes if (node.n, node.k, node.owner_argument_index) == (3, 3, a.argument_index)}
    for position, key in enumerate(a.stable_order_keys, start=1):
      node = node_by_key[key]
      print(
        f"  {position}. {node.statement_type} "
        f"distance={node.distance_to_conclusion} "
        f"anchor={node.provider_anchor} providers={len(node.provider_keys)}"
      )

  print("\\nE. Stable-order sufficiency")
  print("-" * 78)
  multi = tuple(a for a in audits if a.node_count > 1)
  print(f"multi_arguments={len(multi)}")
  print(f"unique_without_tiebreak={sum(a.unique_topological_order for a in multi)}")
  print(f"requires_existing_stable_tiebreak={sum(not a.unique_topological_order for a in multi)}")
  print(f"max_ready_width={max((a.max_ready_width for a in multi), default=0)}")

  print("\\nDecision boundary")
  print("-" * 78)
  print("This audit measures topological-order determinism only.")
  print("For non-unique DAGs, the diagnostic stable key is not a production ordering rule.")
  print("No production contribution placement/order API, renderer, ProofChain, visibility, ownership, deduplication, membership, parity matcher, public route, or dedicated pi_6^3 renderer is changed.")


if __name__ == "__main__":
  print_audit()
