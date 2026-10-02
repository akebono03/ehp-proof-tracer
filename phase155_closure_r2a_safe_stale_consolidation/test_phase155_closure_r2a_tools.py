from __future__ import annotations

import ast

from phase155_closure_r2a_batches import (
  BATCHES,
)
from phase155_closure_r2a_replacements import (
  REPLACEMENTS,
)
from repair_phase155_closure_r2a import (
  _replace_function,
)


def test_exactly_38_safe_stale_functions_are_replaced():
  assert sum(
    len(
      functions
    )
    for functions in REPLACEMENTS.values()
  ) == 38


def test_exactly_38_focused_nodeids_are_batched():
  nodeids = [
    nodeid
    for _batch_name, batch_nodeids in BATCHES
    for nodeid in batch_nodeids
  ]

  assert len(
    nodeids
  ) == 38
  assert len(
    set(
      nodeids
    )
  ) == 38


def test_replacement_is_whole_function_and_parseable():
  source = (
    "def alpha():\n"
    "  assert False\n\n"
    "def beta():\n"
    "  return 2\n"
  )

  updated = _replace_function(
    source,
    "alpha",
    (
      "def alpha():\n"
      "  assert True\n"
    ),
  )

  ast.parse(
    updated
  )
  assert "assert False" not in updated
  assert "assert True" in updated
  assert "def beta():" in updated


def test_no_production_paths_are_targeted():
  assert all(
    path.startswith(
      "tests/"
    )
    for path in REPLACEMENTS
  )


def test_phase144_and_contract_sensitive_files_are_not_targeted():
  assert all(
    "test_phase144_" not in path
    and "test_phase153_" not in path
    and "test_phase95_" not in path
    and "test_phase96_" not in path
    and "test_phase97_" not in path
    and "test_phase98_" not in path
    for path in REPLACEMENTS
  )
