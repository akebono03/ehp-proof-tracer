from __future__ import annotations

import ast

import build_phase155_r4_4 as build


def test_expand_global_names_follows_assignment_chain():
  dependencies = {
    "A": {
      "B",
    },
    "B": {
      "C",
    },
  }

  assert (
    build._expand_global_names(
      {
        "A",
      },
      dependencies,
    )
    == {
      "A",
      "B",
      "C",
    }
  )


def test_global_production_use_is_detected():
  source = (
    "from toda_rules import make_rule\n"
    "\n"
    "RULE = make_rule()\n"
    "\n"
    "def test_x():\n"
    "  assert RULE is not None\n"
  )

  tree = ast.parse(source)
  functions = {
    node.name: node
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }

  analysis = {
    "imported_production_names": {
      "make_rule": "toda_rules",
    },
    "functions": functions,
    "used_names": {
      "test_x": {
        "RULE",
      },
    },
    "local_calls": {
      "test_x": set(),
    },
    "global_dependencies": {
      "RULE": {
        "make_rule",
      },
    },
  }

  assert (
    build._global_production_modules_used_by_test(
      analysis,
      "test_x",
    )
    == {
      "toda_rules",
    }
  )


def test_reachable_modules_follows_transitive_imports():
  graph = {
    "a": {
      "b",
    },
    "b": {
      "c",
    },
    "c": set(),
  }

  assert (
    build._reachable_modules(
      {
        "a",
      },
      graph,
    )
    == {
      "a",
      "b",
      "c",
    }
  )


def test_canonical_categories_include_global_promotion():
  assert (
    build.CATEGORY_GLOBAL_PROMOTION
    in build.CANONICAL_CATEGORIES
  )


def test_runner_source_uses_pytest_main_not_shell_nodeid_expansion():
  source = build.RUNNER_SOURCE

  assert "pytest.main(" in source
  assert "subprocess" not in source
  assert "--collect-only" in source
  assert "collect batch" in source


def test_runner_ps1_warns_heavy():
  source = build.RUNNER_PS1_SOURCE

  assert "This can be HEAVY." in source
