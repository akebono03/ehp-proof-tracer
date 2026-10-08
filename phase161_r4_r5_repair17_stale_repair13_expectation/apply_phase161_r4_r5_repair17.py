from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase161_r4_r5_repair13_reference_selection_source_binding.py"
)
FUNCTION_TEMPLATE = (
  PACKAGE_DIR
  / "test_function.template.py"
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


def main():
  source = TARGET.read_text(
    encoding="utf-8"
  )
  replacement = FUNCTION_TEMPLATE.read_text(
    encoding="utf-8"
  )

  ast.parse(
    replacement
  )

  function_name = (
    "test_phase161_r4_r5_repair13_"
    "reference_selection_binds_prop51_component_source"
  )

  updated = _replace_function(
    source,
    function_name,
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

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  (
    OUTPUT_DIR
    / "test_phase161_r4_r5_repair13_reference_selection_source_binding.py.txt"
  ).write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Updated:",
    TARGET,
  )
  print(
    "Production changes: NONE"
  )
  print(
    "Imports changed: NONE"
  )
  print(
    "Updated stale repair13 expectation to the post-repair14 Reference-entry contract."
  )


if __name__ == "__main__":
  main()
