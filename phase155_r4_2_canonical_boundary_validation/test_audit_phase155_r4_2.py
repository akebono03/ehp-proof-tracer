
from __future__ import annotations

import ast

import audit_phase155_r4_2 as audit


def _analysis(source: str):
  tree = ast.parse(
    source
  )

  imported_public_names = {}
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
        if root in audit.PUBLIC_MODULES:
          imported_public_names[
            alias.asname
            if alias.asname
            else root
          ] = root
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
      if root not in audit.PUBLIC_MODULES:
        continue
      for alias in node.names:
        imported_public_names[
          alias.asname
          if alias.asname
          else alias.name
        ] = root

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
    "imported_public_names": imported_public_names,
    "functions": functions,
    "used_names": used_names,
    "local_calls": local_calls,
  }


def test_public_module_direct_use_is_detected():
  analysis = _analysis(
    "from web_group_query import build_standard_web_group_query_view\n"
    "\n"
    "def test_x():\n"
    "  assert build_standard_web_group_query_view(3, 3)\n"
  )

  assert (
    audit._public_modules_used_by_test(
      analysis,
      "test_x",
    )
    == {
      "web_group_query",
    }
  )


def test_public_module_use_through_local_helper_is_detected():
  analysis = _analysis(
    "import main as cli_main\n"
    "\n"
    "def _run():\n"
    "  return cli_main.main([])\n"
    "\n"
    "def test_x():\n"
    "  assert _run() == 0\n"
  )

  assert (
    audit._public_modules_used_by_test(
      analysis,
      "test_x",
    )
    == {
      "main",
    }
  )


def test_unused_public_import_does_not_promote():
  analysis = _analysis(
    "import main as cli_main\n"
    "\n"
    "def test_x():\n"
    "  assert True\n"
  )

  assert (
    audit._public_modules_used_by_test(
      analysis,
      "test_x",
    )
    == set()
  )


def test_review_with_public_use_is_promoted():
  category, reason = (
    audit._promoted_category(
      audit.CATEGORY_REVIEW,
      {
        "web_generator_execution",
      },
    )
  )

  assert (
    category
    == audit.CATEGORY_PUBLIC_PROMOTION
  )
  assert (
    "web_generator_execution"
    in reason
  )


def test_historical_precedence_is_preserved():
  category, _ = (
    audit._promoted_category(
      audit.CATEGORY_HISTORICAL,
      {
        "main",
      },
    )
  )

  assert (
    category
    == audit.CATEGORY_HISTORICAL
  )


def test_heavy_precedence_is_preserved():
  category, _ = (
    audit._promoted_category(
      audit.CATEGORY_HEAVY,
      {
        "main",
      },
    )
  )

  assert (
    category
    == audit.CATEGORY_HEAVY
  )


def test_audit_precedence_is_preserved():
  category, _ = (
    audit._promoted_category(
      audit.CATEGORY_AUDIT,
      {
        "web_group_proof",
      },
    )
  )

  assert (
    category
    == audit.CATEGORY_AUDIT
  )


def test_reachable_functions_handles_cycle():
  calls = {
    "test_x": {
      "helper",
    },
    "helper": {
      "test_x",
    },
  }

  assert (
    audit._reachable_functions(
      "test_x",
      calls,
    )
    == {
      "test_x",
      "helper",
    }
  )
