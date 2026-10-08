from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TARGET = (
  REPO_ROOT
  / "toda_literature_statement_boundary.py"
)
TEST_TEMPLATE = (
  PACKAGE_DIR
  / "test_phase161_r4_r5_repair16_prop51_higher_eta_fixed_boundary.template.py"
)
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase161_r4_r5_repair16_prop51_higher_eta_fixed_boundary.py"
)

BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output"

FIXED_RULE = (
  '  "Toda Proposition 5.1 higher eta group relation": '
  '"higher_eta_group_relation",\n'
)
LOCATOR_RULE = (
  '  "Toda Proposition 5.1 higher eta group relation": '
  '"Proposition 5.1",\n'
)


def _assignment_source(
  source: str,
  name: str,
) -> str:
  tree = ast.parse(
    source
  )

  node = next(
    node
    for node in tree.body
    if (
      isinstance(
        node,
        ast.Assign,
      )
      and any(
        isinstance(
          target,
          ast.Name,
        )
        and target.id == name
        for target in node.targets
      )
    )
  )
  lines = source.splitlines()

  return "\n".join(
    lines[
      node.lineno - 1:
      node.end_lineno
    ]
  ) + "\n"


def _insert_after_dictionary_open(
  source: str,
  dictionary_name: str,
  entry: str,
) -> str:
  if entry.strip() in source:
    return source

  marker = (
    dictionary_name
    + " = {\n"
  )

  if marker not in source:
    raise RuntimeError(
      f"Dictionary not found: {dictionary_name}"
    )

  return source.replace(
    marker,
    marker + entry,
    1,
  )


def main():
  source = TARGET.read_text(
    encoding="utf-8"
  )
  test_source = TEST_TEMPLATE.read_text(
    encoding="utf-8"
  )

  updated = _insert_after_dictionary_open(
    source,
    "_FIXED_RULE_COMPONENT_KEYS",
    FIXED_RULE,
  )
  updated = _insert_after_dictionary_open(
    updated,
    "_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME",
    LOCATOR_RULE,
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
    / "_FIXED_RULE_COMPONENT_KEYS.py.txt"
  ).write_text(
    _assignment_source(
      updated,
      "_FIXED_RULE_COMPONENT_KEYS",
    ),
    encoding="utf-8",
    newline="\n",
  )
  (
    OUTPUT_DIR
    / "_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME.py.txt"
  ).write_text(
    _assignment_source(
      updated,
      "_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME",
    ),
    encoding="utf-8",
    newline="\n",
  )
  (
    OUTPUT_DIR
    / "test_phase161_r4_r5_repair16_prop51_higher_eta_fixed_boundary.py.txt"
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
    "Registered Toda Proposition 5.1 higher eta group relation as "
    "FIXED_STATEMENT / higher_eta_group_relation."
  )


if __name__ == "__main__":
  main()
