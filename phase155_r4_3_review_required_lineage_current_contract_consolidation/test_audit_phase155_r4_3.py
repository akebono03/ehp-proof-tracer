
from __future__ import annotations

import ast

import audit_phase155_r4_3 as audit


def _analysis(
  source: str,
  production_modules: set[str],
):
  tree = ast.parse(source)

  imported_production_names = {}
  imported_test_helpers = set()

  for node in tree.body:
    if isinstance(
      node,
      ast.Import,
    ):
      for alias in node.names:
        root = alias.name.split(
          ".",
          1,
        )[0]
        if root in production_modules:
          imported_production_names[
            alias.asname
            if alias.asname
            else root
          ] = root
        if root == "tests":
          imported_test_helpers.add(
            alias.asname
            if alias.asname
            else root
          )

    elif isinstance(
      node,
      ast.ImportFrom,
    ):
      if node.module is None:
        continue
      root = node.module.split(
        ".",
        1,
      )[0]

      if root in production_modules:
        for alias in node.names:
          imported_production_names[
            alias.asname
            if alias.asname
            else alias.name
          ] = root

      if root == "tests":
        for alias in node.names:
          imported_test_helpers.add(
            alias.asname
            if alias.asname
            else alias.name
          )

  functions = {
    node.name: node
    for node in tree.body
    if isinstance(
      node,
      (
        ast.FunctionDef,
        ast.AsyncFunctionDef,
      ),
    )
  }

  used_names = {}
  local_calls = {}

  for name, node in functions.items():
    used_names[name] = {
      child.id
      for child in ast.walk(
        node
      )
      if isinstance(
        child,
        ast.Name,
      )
    }
    local_calls[name] = {
      child.func.id
      for child in ast.walk(
        node
      )
      if (
        isinstance(
          child,
          ast.Call,
        )
        and isinstance(
          child.func,
          ast.Name,
        )
        and child.func.id
        in functions
      )
    }

  return {
    "imported_production_names": imported_production_names,
    "imported_test_helpers": imported_test_helpers,
    "functions": functions,
    "used_names": used_names,
    "local_calls": local_calls,
  }


def test_current_production_direct_use_is_owned():
  analysis = _analysis(
    "from toda_rules import make_rule\n"
    "\n"
    "def test_x():\n"
    "  assert make_rule()\n",
    {
      "toda_rules",
    },
  )

  modules, helpers = (
    audit._ownership_for_test(
      analysis,
      "test_x",
    )
  )

  assert modules == {
    "toda_rules",
  }
  assert helpers == set()


def test_current_production_use_through_helper_is_owned():
  analysis = _analysis(
    "from proof_repository import ProofRepository\n"
    "\n"
    "def _make():\n"
    "  return ProofRepository()\n"
    "\n"
    "def test_x():\n"
    "  assert _make() is not None\n",
    {
      "proof_repository",
    },
  )

  modules, _ = (
    audit._ownership_for_test(
      analysis,
      "test_x",
    )
  )

  assert modules == {
    "proof_repository",
  }


def test_tests_helper_without_production_is_lineage_support():
  analysis = _analysis(
    "from tests.test_a import make_data\n"
    "\n"
    "def test_x():\n"
    "  assert make_data()\n",
    set(),
  )

  modules, helpers = (
    audit._ownership_for_test(
      analysis,
      "test_x",
    )
  )

  category, _ = audit._reclassify(
    audit.CATEGORY_REVIEW,
    modules,
    helpers,
  )

  assert modules == set()
  assert helpers == {
    "make_data",
  }
  assert (
    category
    == audit.CATEGORY_LINEAGE_SUPPORT
  )


def test_review_with_production_ownership_is_internal_canonical():
  category, reason = (
    audit._reclassify(
      audit.CATEGORY_REVIEW,
      {
        "toda_rules",
      },
      set(),
    )
  )

  assert (
    category
    == audit.CATEGORY_INTERNAL
  )
  assert "toda_rules" in reason


def test_historical_lane_is_preserved():
  category, _ = (
    audit._reclassify(
      audit.CATEGORY_HISTORICAL,
      {
        "toda_rules",
      },
      set(),
    )
  )

  assert (
    category
    == audit.CATEGORY_HISTORICAL
  )


def test_existing_public_lane_is_preserved():
  category, _ = (
    audit._reclassify(
      audit.CATEGORY_PUBLIC,
      {
        "toda_rules",
      },
      set(),
    )
  )

  assert (
    category
    == audit.CATEGORY_PUBLIC
  )


def test_reachable_functions_handles_cycle():
  assert (
    audit._reachable_functions(
      "test_x",
      {
        "test_x": {
          "helper",
        },
        "helper": {
          "test_x",
        },
      },
    )
    == {
      "test_x",
      "helper",
    }
  )
