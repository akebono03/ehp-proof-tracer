from __future__ import annotations

import ast

import audit_phase155_r5 as audit


def test_historical_only_marker_is_historical():
  source = (
    "def test_x():\n"
    "  text = 'Historical only:'\n"
    "  assert text\n"
  )
  tree = ast.parse(source)

  lane, _, evidence = (
    audit._classify_residual(
      "tests/test_probe.py",
      "test_x",
      source,
      tree,
    )
  )

  assert lane == audit.R5_HISTORICAL
  assert evidence[
    "historical_strong"
  ]


def test_audit_module_import_is_audit_only():
  source = (
    "from audit_something import build_inventory\n"
    "\n"
    "def test_x():\n"
    "  assert build_inventory()\n"
  )
  tree = ast.parse(source)

  lane, _, evidence = (
    audit._classify_residual(
      "tests/test_something.py",
      "test_x",
      source,
      tree,
    )
  )

  assert lane == audit.R5_AUDIT
  assert evidence[
    "audit_import"
  ]


def test_cross_group_loop_is_heavy():
  source = (
    "TARGETS = ((3, 3), (5, 3))\n"
    "\n"
    "def test_cross_group_population():\n"
    "  for n, k in TARGETS:\n"
    "    assert n > 0\n"
  )
  tree = ast.parse(source)

  lane, _, evidence = (
    audit._classify_residual(
      "tests/test_cross_group.py",
      "test_cross_group_population",
      source,
      tree,
    )
  )

  assert lane == audit.R5_HEAVY
  assert evidence[
    "heavy_strong"
  ]


def test_plain_residual_is_retained():
  source = (
    "def test_small_contract():\n"
    "  assert 1 + 1 == 2\n"
  )
  tree = ast.parse(source)

  lane, _, _ = (
    audit._classify_residual(
      "tests/test_small.py",
      "test_small_contract",
      source,
      tree,
    )
  )

  assert lane == audit.R5_RESIDUAL


def test_existing_heavy_lane_is_preserved():
  assert (
    audit._lane_for_existing_category(
      audit.CATEGORY_HEAVY
    )
    == audit.R5_HEAVY
  )


def test_existing_canonical_lane_is_preserved():
  assert (
    audit._lane_for_existing_category(
      audit.CATEGORY_INTERNAL
    )
    == audit.R5_CANONICAL
  )
