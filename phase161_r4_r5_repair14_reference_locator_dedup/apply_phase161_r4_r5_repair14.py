from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_references.py"
)
FUNCTION_TEMPLATE = (
  PACKAGE_DIR
  / "build_toda_group_proof_narrative_reference_entries.template.py"
)
TEST_TEMPLATE = (
  PACKAGE_DIR
  / "test_phase161_r4_r5_repair14_reference_locator_dedup.template.py"
)
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase161_r4_r5_repair14_reference_locator_dedup.py"
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
    "build_toda_group_proof_narrative_reference_entries",
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
    / "build_toda_group_proof_narrative_reference_entries.py.txt"
  ).write_text(
    replacement,
    encoding="utf-8",
    newline="\n",
  )
  (
    OUTPUT_DIR
    / "test_phase161_r4_r5_repair14_reference_locator_dedup.py.txt"
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
    "Reference entries are now deduplicated by semantic literature identity "
    "(locator when available), using the existing helper."
  )


if __name__ == "__main__":
  main()
