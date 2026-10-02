
from __future__ import annotations

import ast

import apply_phase155_r3_3d_r4 as apply_tool
import verify_phase155_r3_3d_r4 as verify_tool


def test_unique_hidden_name_is_deterministic():
  existing = {
    "test_x",
  }

  value = (
    apply_tool._unique_hidden_name(
      existing,
      "test_x",
      1,
    )
  )

  assert (
    value
    == "test_x_phase155_hidden_coverage_1"
  )


def test_unique_hidden_name_avoids_collision():
  existing = {
    "test_x",
    "test_x_phase155_hidden_coverage_1",
  }

  value = (
    apply_tool._unique_hidden_name(
      existing,
      "test_x",
      1,
    )
  )

  assert (
    value
    == "test_x_phase155_hidden_coverage_1_2"
  )


def test_apply_file_operations_renames_shadowed_definition():
  source = (
    "def test_x():\n"
    "  assert True\n"
    "\n"
    "def test_x():\n"
    "  assert False\n"
  )

  new_source, renamed, removed = (
    apply_tool._apply_file_operations(
      source,
      [
        {
          "function_name": "test_x",
          "recommendation": (
            "preserve_hidden_coverage_before_cleanup"
          ),
        }
      ],
      set(),
    )
  )

  assert (
    "def test_x_phase155_hidden_coverage_1():"
    in new_source
  )
  assert (
    new_source.count(
      "def test_x():"
    )
    == 1
  )
  assert len(renamed) == 1
  assert removed == []
  ast.parse(
    new_source
  )


def test_apply_file_operations_removes_cleanup_ready_shadow():
  source = (
    "def test_x():\n"
    "  assert True\n"
    "\n"
    "def test_x():\n"
    "  assert False\n"
  )

  new_source, renamed, removed = (
    apply_tool._apply_file_operations(
      source,
      [
        {
          "function_name": "test_x",
          "recommendation": (
            "shadowed_definition_cleanup_ready"
          ),
        }
      ],
      set(),
    )
  )

  assert (
    new_source.count(
      "def test_x():"
    )
    == 1
  )
  assert renamed == []
  assert removed == []
  ast.parse(
    new_source
  )


def test_apply_file_operations_removes_pair_older_function():
  source = (
    "def test_old():\n"
    "  assert True\n"
    "\n"
    "def test_keep():\n"
    "  assert True\n"
  )

  new_source, renamed, removed = (
    apply_tool._apply_file_operations(
      source,
      [],
      {
        "test_old",
      },
    )
  )

  assert "def test_old" not in new_source
  assert "def test_keep" in new_source
  assert renamed == []
  assert removed == [
    "test_old",
  ]


def test_verify_top_level_counts_detects_duplicate():
  path_source = (
    "def test_x():\n"
    "  pass\n"
    "\n"
    "def test_x():\n"
    "  pass\n"
  )
  tree = ast.parse(
    path_source
  )
  names = [
    node.name
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  ]

  assert names.count(
    "test_x"
  ) == 2
