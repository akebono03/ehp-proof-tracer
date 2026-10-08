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
  / "test_phase161_r4_r5_repair11_effective_reference_source_component.template.py"
)
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase161_r4_r5_repair11_effective_reference_source_component.py"
)

BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output"

NEW_FUNCTION_PATH = (
  PACKAGE_DIR
  / "_phase154_r5_reference_source_steps_by_number.template.py"
)


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


def main():
  source = TARGET.read_text(
    encoding="utf-8"
  )
  replacement = NEW_FUNCTION_PATH.read_text(
    encoding="utf-8"
  )
  test_source = TEST_TEMPLATE.read_text(
    encoding="utf-8"
  )

  ast.parse(
    replacement
  )
  ast.parse(
    test_source
  )

  updated = _replace_function(
    source,
    "_phase154_r5_reference_source_steps_by_number",
    replacement,
  )

  ast.parse(
    updated
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
    / "_phase154_r5_reference_source_steps_by_number.py.txt"
  ).write_text(
    replacement,
    encoding="utf-8",
    newline="\n",
  )
  (
    OUTPUT_DIR
    / "test_phase161_r4_r5_repair11_effective_reference_source_component.py.txt"
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
    "Reference linkage now uses the displayed aggregate component premise "
    "when that component is uniquely represented by a premise step."
  )


if __name__ == "__main__":
  main()
