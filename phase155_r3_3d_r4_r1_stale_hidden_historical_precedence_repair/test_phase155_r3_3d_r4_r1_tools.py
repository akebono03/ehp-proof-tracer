
from __future__ import annotations

import ast

import apply_phase155_r3_3d_r4_r1 as apply_tool


def test_remove_function_removes_exact_top_level_test():
  source = (
    "def test_old():\n"
    "  assert False\n"
    "\n"
    "def test_keep():\n"
    "  assert True\n"
  )

  result = apply_tool._remove_function(
    source,
    "test_old",
  )

  assert "def test_old" not in result
  assert "def test_keep" in result
  ast.parse(result)


def test_append_function_if_missing_restores_function():
  source = (
    "def test_keep():\n"
    "  assert True\n"
  )
  restored = (
    "def test_old():\n"
    "  assert True\n"
  )

  result = apply_tool._append_function_if_missing(
    source,
    "test_old",
    restored,
  )

  assert "def test_old" in result
  assert "def test_keep" in result
  ast.parse(result)


def test_append_function_if_missing_is_idempotent():
  source = (
    "def test_old():\n"
    "  assert True\n"
  )

  result = apply_tool._append_function_if_missing(
    source,
    "test_old",
    source,
  )

  assert result == source


def test_split_test_id_normalizes_path():
  assert apply_tool._split_test_id(
    r"tests\test_x.py::test_y"
  ) == (
    "tests/test_x.py",
    "test_y",
  )
