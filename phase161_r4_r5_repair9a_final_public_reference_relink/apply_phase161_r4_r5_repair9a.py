from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST_TEMPLATE = (
  PACKAGE_DIR
  / "test_phase161_r4_r5_repair9a_final_public_reference_relink.template.py"
)
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase161_r4_r5_repair9a_final_public_reference_relink.py"
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
  test_source = TEST_TEMPLATE.read_text(
    encoding="utf-8"
  )

  function_name = (
    "render_toda_group_proof_narrative_"
    "multi_argument_with_contributions_markdown"
  )

  current_function = _extract_function(
    source,
    function_name,
  )

  final_relink = """  rendered = (
    link_toda_group_proof_narrative_reference_body_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )

"""

  anchor = """  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
"""

  if final_relink not in current_function:
    if anchor not in current_function:
      raise RuntimeError(
        "Expected final reference_section anchor not found."
      )

    updated_function = current_function.replace(
      anchor,
      final_relink + anchor,
      1,
    )
  else:
    updated_function = current_function

  updated = _replace_function(
    source,
    function_name,
    updated_function,
  )

  ast.parse(
    updated
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
    updated,
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

  (
    OUTPUT_DIR
    / (
      "render_toda_group_proof_narrative_"
      "multi_argument_with_contributions_markdown.py.txt"
    )
  ).write_text(
    updated_function,
    encoding="utf-8",
    newline="\n",
  )

  (
    OUTPUT_DIR
    / "test_phase161_r4_r5_repair9a_final_public_reference_relink.py.txt"
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
    "Added final public Reference-body relink after filtering/restoration."
  )


if __name__ == "__main__":
  main()
