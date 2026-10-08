from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
HELPER_TEMPLATE = (
  PACKAGE_DIR
  / "reference_selection_helpers.template.py"
)
TEST_TEMPLATE = (
  PACKAGE_DIR
  / "test_phase161_r4_r5_repair13_reference_selection_source_binding.template.py"
)
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase161_r4_r5_repair13_reference_selection_source_binding.py"
)

BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output"


def _functions(
  source: str,
):
  tree = ast.parse(
    source
  )

  return {
    node.name: node
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }


def _replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  functions = _functions(
    source
  )

  if function_name not in functions:
    raise RuntimeError(
      f"Missing function: {function_name}"
    )

  node = functions[
    function_name
  ]
  lines = source.splitlines(
    keepends=True
  )
  replacement_lines = [
    line + "\n"
    for line in replacement.rstrip(
      "\n"
    ).split(
      "\n"
    )
  ]

  return "".join(
    lines[
      :node.lineno - 1
    ]
    + replacement_lines
    + lines[
      node.end_lineno:
    ]
  )


def _insert_before_function(
  source: str,
  function_name: str,
  addition: str,
) -> str:
  functions = _functions(
    source
  )

  if function_name not in functions:
    raise RuntimeError(
      f"Missing insertion anchor: {function_name}"
    )

  node = functions[
    function_name
  ]
  lines = source.splitlines(
    keepends=True
  )
  addition_lines = [
    line + "\n"
    for line in addition.rstrip(
      "\n"
    ).split(
      "\n"
    )
  ]

  return "".join(
    lines[
      :node.lineno - 1
    ]
    + addition_lines
    + [
      "\n",
      "\n",
    ]
    + lines[
      node.lineno - 1:
    ]
  )


def _extract_function(
  source: str,
  function_name: str,
) -> str:
  node = _functions(
    source
  )[
    function_name
  ]
  lines = source.splitlines()

  return "\n".join(
    lines[
      node.lineno - 1:
      node.end_lineno
    ]
  ) + "\n"


def main():
  source = TARGET.read_text(
    encoding="utf-8"
  )
  helper_template = HELPER_TEMPLATE.read_text(
    encoding="utf-8"
  )
  test_source = TEST_TEMPLATE.read_text(
    encoding="utf-8"
  )

  helper_tree = ast.parse(
    helper_template
  )
  helper_functions = {
    node.name: node
    for node in helper_tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }

  new_helper_name = (
    "_select_toda_group_proof_narrative_"
    "reference_entries_and_statement_lines"
  )
  wrapper_name = (
    "_toda_group_proof_narrative_"
    "reference_statement_lines_by_number"
  )

  new_helper_node = helper_functions[
    new_helper_name
  ]
  wrapper_node = helper_functions[
    wrapper_name
  ]
  helper_lines = helper_template.splitlines()

  new_helper_source = "\n".join(
    helper_lines[
      new_helper_node.lineno - 1:
      new_helper_node.end_lineno
    ]
  ) + "\n"
  wrapper_source = "\n".join(
    helper_lines[
      wrapper_node.lineno - 1:
      wrapper_node.end_lineno
    ]
  ) + "\n"

  functions = _functions(
    source
  )

  if new_helper_name not in functions:
    source = _insert_before_function(
      source,
      wrapper_name,
      new_helper_source,
    )

  source = _replace_function(
    source,
    wrapper_name,
    wrapper_source,
  )

  render_name = (
    "render_toda_group_proof_narrative_"
    "multi_argument_with_contributions_markdown"
  )
  render_source = _extract_function(
    source,
    render_name,
  )

  old = """  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )
"""

  new = """  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    _select_toda_group_proof_narrative_reference_entries_and_statement_lines(
      presentation,
      reference_entries,
    )
  )
"""

  if old not in render_source:
    if new not in render_source:
      raise RuntimeError(
        "Expected Reference statement-selection anchor not found."
      )
  else:
    render_source = render_source.replace(
      old,
      new,
      1,
    )
    source = _replace_function(
      source,
      render_name,
      render_source,
    )

  ast.parse(
    source
  )
  ast.parse(
    test_source
  )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    TARGET,
    BACKUP_DIR / TARGET.name,
  )

  TARGET.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )
  TEST_TARGET.write_text(
    test_source,
    encoding="utf-8",
    newline="\n",
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  for function_name in (
    new_helper_name,
    wrapper_name,
    render_name,
  ):
    (
      OUTPUT_DIR
      / (
        function_name
        + ".py.txt"
      )
    ).write_text(
      _extract_function(
        source,
        function_name,
      ),
      encoding="utf-8",
      newline="\n",
    )

  (
    OUTPUT_DIR
    / "test_phase161_r4_r5_repair13_reference_selection_source_binding.py.txt"
  ).write_text(
    test_source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Updated:",
    TARGET,
  )
  print(
    "Wrote:",
    TEST_TARGET,
  )
  print(
    "Production imports changed: NONE"
  )
  print(
    "Reference statement selection now binds the displayed fixed component "
    "step into the Reference entry before downstream filtering/linkage."
  )


if __name__ == "__main__":
  main()
