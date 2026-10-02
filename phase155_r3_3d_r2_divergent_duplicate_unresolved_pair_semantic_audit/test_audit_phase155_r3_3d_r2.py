
from __future__ import annotations

import ast

import audit_phase155_r3_3d_r2 as audit


def test_module_name_from_test_path():
  assert (
    audit._module_name_from_test_path(
      "tests/test_x.py"
    )
    == "tests.test_x"
  )


def test_function_nodes_extracts_assertions_and_order(
  tmp_path,
):
  path = tmp_path / "test_x.py"
  path.write_text(
    "def test_a():\n"
    "  assert 1 == 1\n"
    "\n"
    "def test_a():\n"
    "  assert 2 == 2\n",
    encoding="utf-8",
  )

  nodes = audit._function_nodes(
    path,
    "test_a",
  )

  assert len(nodes) == 2
  assert nodes[0]["ordinal"] == 1
  assert nodes[1]["ordinal"] == 2
  assert nodes[0]["assertions"] != nodes[1]["assertions"]


def test_truthy():
  assert audit._truthy("True") is True
  assert audit._truthy("1") is True
  assert audit._truthy("false") is False


def test_row_index_groups_duplicate_ids():
  rows = [
    {"test_id": "a", "value": "1"},
    {"test_id": "a", "value": "2"},
    {"test_id": "b", "value": "3"},
  ]

  index = audit._row_index(
    rows,
    "test_id",
  )

  assert len(index["a"]) == 2
  assert len(index["b"]) == 1
