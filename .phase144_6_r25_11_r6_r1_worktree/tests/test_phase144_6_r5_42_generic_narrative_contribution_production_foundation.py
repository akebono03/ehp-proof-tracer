from collections import Counter

from audit_phase144_6_r5_40 import build_placement_inventory
from audit_phase144_6_r5_41 import build_topological_order_audit
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_contribution_ordering import (
  TodaGroupProofNarrativeContributionPlacement,
  build_toda_group_proof_narrative_ordered_contributions,
)


def _production(n, k):
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(n, k)
  return build_toda_group_proof_narrative_ordered_contributions(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
  )


def _production_rows():
  return tuple(
    row
    for n, k in TARGETS
    for argument_rows in _production(n, k)
    for row in argument_rows
  )


def test_phase144_6_r5_42_reproduces_phase40_selected_population():
  assert len(_production_rows()) == len(build_placement_inventory()) == 190


def test_phase144_6_r5_42_reproduces_phase40_placement_counts():
  expected = Counter(
    row.placement_class
    for row in build_placement_inventory()
  )
  actual = Counter(
    row.placement.value
    for row in _production_rows()
  )
  assert actual == expected


def test_phase144_6_r5_42_returns_one_tuple_per_argument():
  for n, k in TARGETS:
    context = _context(n, k)
    arguments = context[3]
    rows = _production(n, k)
    assert isinstance(rows, tuple)
    assert len(rows) == len(arguments)
    assert all(isinstance(argument_rows, tuple) for argument_rows in rows)


def test_phase144_6_r5_42_pi6_has_five_ordered_contributions():
  rows = _production(3, 3)
  populated = tuple(argument_rows for argument_rows in rows if argument_rows)
  assert len(populated) == 1
  assert len(populated[0]) == 5
  assert all(
    row.placement
    is TodaGroupProofNarrativeContributionPlacement.AT_PROVIDER_ANCHOR
    for row in populated[0]
  )


def test_phase144_6_r5_42_pi6_order_matches_phase41_topological_order():
  audits, nodes = build_topological_order_audit()
  audit = next(
    row
    for row in audits
    if (row.n, row.k) == (3, 3) and row.node_count == 5
  )
  node_by_key = {
    node.key: node
    for node in nodes
    if (
      node.n,
      node.k,
      node.owner_argument_index,
    ) == (3, 3, audit.argument_index)
  }
  expected_step_ids = tuple(
    node_by_key[key].step_id
    for key in audit.stable_order_keys
  )
  actual = _production(3, 3)[audit.argument_index]
  assert tuple(id(row.proof_step) for row in actual) == expected_step_ids


def test_phase144_6_r5_42_every_argument_order_respects_proof_graph():
  for n, k in TARGETS:
    presentation = _context(n, k)[0]
    children = {}
    for edge in presentation.edges:
      children.setdefault(id(edge.premise_step), set()).add(
        id(edge.parent_step)
      )

    def reachable(source, target):
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

    for argument_rows in _production(n, k):
      positions = {
        id(row.proof_step): index
        for index, row in enumerate(argument_rows)
      }
      for left_id, left_position in positions.items():
        for right_id, right_position in positions.items():
          if left_id == right_id:
            continue
          if reachable(left_id, right_id):
            assert left_position < right_position


def test_phase144_6_r5_42_nonunique_phase41_arguments_are_deterministic():
  audits, nodes = build_topological_order_audit()
  nonunique = tuple(
    row
    for row in audits
    if row.node_count > 1 and not row.unique_topological_order
  )
  assert {
    (row.n, row.k, row.argument_index, row.argument_role)
    for row in nonunique
  } == {
    (8, 7, 1, "establish_definition"),
    (9, 7, 2, "establish_definition"),
  }

  for audit in nonunique:
    first = _production(audit.n, audit.k)[audit.argument_index]
    second = _production(audit.n, audit.k)[audit.argument_index]
    assert tuple(id(row.proof_step) for row in first) == tuple(
      id(row.proof_step) for row in second
    )
    assert len(first) == audit.node_count == 10


def test_phase144_6_r5_42_production_module_does_not_import_audit_modules():
  import toda_group_proof_narrative_contribution_ordering as module

  source = open(module.__file__, encoding="utf-8").read()
  assert "from audit_" not in source
  assert "import audit_" not in source


def test_phase144_6_r5_42_provider_keys_follow_chain_membership_not_necessity():
  import inspect
  import toda_group_proof_narrative_contribution_ordering as module

  source = inspect.getsource(module._provider_keys_for_step)
  assert "if step_id in chain_ids:" in source
  assert "necessity.get(step_id" not in source
