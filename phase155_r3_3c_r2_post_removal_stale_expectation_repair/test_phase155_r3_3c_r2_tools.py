
from __future__ import annotations

import ast

import apply_phase155_r3_3c_r2 as apply_tool


def test_find_function_requires_one_top_level_definition():
  tree = ast.parse(
    "def test_x():\n"
    "  assert True\n"
  )

  function = apply_tool._find_function(
    tree,
    "test_x",
  )

  assert function.name == "test_x"


def test_replace_functions_in_file_replaces_multiple_named_targets(
  tmp_path,
):
  path = (
    tmp_path
    / "test_x.py"
  )
  path.write_text(
    "def test_a():\n"
    "  assert False\n"
    "\n"
    "def helper():\n"
    "  return 1\n"
    "\n"
    "def test_b():\n"
    "  assert False\n",
    encoding="utf-8",
  )

  apply_tool._replace_functions_in_file(
    path,
    [
      (
        "test_a",
        "def test_a():\n"
        "  assert True\n",
      ),
      (
        "test_b",
        "def test_b():\n"
        "  assert True\n",
      ),
    ],
  )

  source = path.read_text(
    encoding="utf-8",
  )

  assert source.count(
    "assert True"
  ) == 2
  assert "def helper" in source
  ast.parse(
    source
  )


def test_replace_preserves_import_block(
  tmp_path,
):
  path = (
    tmp_path
    / "test_x.py"
  )
  path.write_text(
    "import pytest\n"
    "\n"
    "from module_x import value\n"
    "\n"
    "def test_a():\n"
    "  assert False\n",
    encoding="utf-8",
  )

  apply_tool._replace_functions_in_file(
    path,
    [
      (
        "test_a",
        "def test_a():\n"
        "  assert value\n",
      ),
    ],
  )

  source = path.read_text(
    encoding="utf-8",
  )

  assert source.startswith(
    "import pytest\n\n"
    "from module_x import value\n"
  )
