from __future__ import annotations

import ast
from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

PRODUCTION = (
  REPO_ROOT
  / "toda_group_proof_narrative_renderer.py"
)
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py"
)
TEST_SOURCE = (
  PACKAGE_DIR
  / "tests"
  / "test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py"
)

BACKUP_DIR = (
  PACKAGE_DIR
  / "backup_before_repair53_r5"
)

FUNCTION_NAME = (
  "_phase153_r3_10_connect_public_reference_section"
)

OLD_TARGET_BLOCK = r'''  if (
    target.group_dimension == 15
    and target.sphere_dimension == 8
    and "[R1] より, これらの生成元はそれぞれ"
    in proof_body
  ):
    prop44_reference_number = next(
      (
        entry.number
        for entry in reference_entries
        if entry.reference.locator
        == "Proposition 4.4"
      ),
      None,
    )

    if prop44_reference_number is not None:
      proof_body = proof_body.replace(
        "[R1] より, これらの生成元はそれぞれ",
        (
          "[R"
          + str(
            prop44_reference_number
          )
          + "] より, これらの生成元はそれぞれ"
        ),
        1,
      )
'''

NEW_TARGET_BLOCK = r'''  if (
    target.group_dimension == 15
    and target.sphere_dimension == 8
  ):
    prop515_entry = next(
      (
        entry
        for entry in reference_entries
        if entry.reference.locator
        == "Proposition 5.15"
      ),
      None,
    )
    prop44_reference_number = next(
      (
        entry.number
        for entry in reference_entries
        if entry.reference.locator
        == "Proposition 4.4"
      ),
      None,
    )

    if prop515_entry is not None:
      pi14_7_step = next(
        (
          proof_step
          for proof_step in prop515_entry.proof_steps
          if (
            proof_step.inference_rule is not None
            and "pi_14^7 finite cyclic"
            in proof_step.inference_rule.name
          )
        ),
        None,
      )

      if pi14_7_step is not None:
        pi14_7_latex = (
          render_repository_conclusion_latex(
            pi14_7_step.conclusion
          )
        )
        legacy_pi14_7_block = (
          "既に,\n\n"
          "\\[\n"
          + pi14_7_latex
          + "\n\\]"
        )

        if legacy_pi14_7_block in proof_body:
          proof_body = proof_body.replace(
            legacy_pi14_7_block,
            (
              "[R"
              + str(
                prop515_entry.number
              )
              + "] より,\n\n"
              "\\[\n"
              + pi14_7_latex
              + "\n\\]"
            ),
            1,
          )

    if (
      prop44_reference_number is not None
      and "[R1] より, これらの生成元はそれぞれ"
      in proof_body
    ):
      proof_body = proof_body.replace(
        "[R1] より, これらの生成元はそれぞれ",
        (
          "[R"
          + str(
            prop44_reference_number
          )
          + "] より, これらの生成元はそれぞれ"
        ),
        1,
      )
'''

OLD_AFTER_EXCLUSION = r'''  if (
    len(
      filtered_reference_entries
    )
    != len(
      used_reference_entries
    )
  ):
    return rendered

  filtered_proof_body = (
'''

NEW_AFTER_EXCLUSION = r'''  if (
    len(
      filtered_reference_entries
    )
    != len(
      used_reference_entries
    )
  ):
    return rendered

  filtered_statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      filtered_reference_entries,
    )
  )

  filtered_proof_body = (
'''


def _function_source(
  source: str,
  function_name: str,
) -> str:
  tree = ast.parse(
    source
  )
  function = next(
    (
      node
      for node in tree.body
      if (
        isinstance(
          node,
          ast.FunctionDef,
        )
        and node.name
        == function_name
      )
    ),
    None,
  )

  if function is None:
    raise RuntimeError(
      "missing function: "
      + function_name
    )

  lines = source.splitlines(
    keepends=True
  )

  return "".join(
    lines[
      function.lineno - 1:
      function.end_lineno
    ]
  )


def _replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  tree = ast.parse(
    source
  )
  function = next(
    (
      node
      for node in tree.body
      if (
        isinstance(
          node,
          ast.FunctionDef,
        )
        and node.name
        == function_name
      )
    ),
    None,
  )

  if function is None:
    raise RuntimeError(
      "missing function: "
      + function_name
    )

  lines = source.splitlines(
    keepends=True
  )
  start = sum(
    len(
      line
    )
    for line in lines[
      :function.lineno - 1
    ]
  )
  end = sum(
    len(
      line
    )
    for line in lines[
      :function.end_lineno
    ]
  )

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n"
    + source[
      end:
    ]
  )


def main() -> int:
  if not PRODUCTION.exists():
    raise RuntimeError(
      "missing production file: "
      + str(
        PRODUCTION
      )
    )

  source = PRODUCTION.read_text(
    encoding="utf-8",
  )
  function_source = _function_source(
    source,
    FUNCTION_NAME,
  )

  already_applied = (
    'and "pi_14^7 finite cyclic"\n'
    '            in proof_step.inference_rule.name'
    in function_source
    and (
      "filtered_statement_lines = (\n"
      "    _toda_group_proof_narrative_reference_statement_lines_by_number(\n"
      "      presentation,\n"
      "      filtered_reference_entries,"
      in function_source
    )
  )

  if already_applied:
    print(
      "Phase157-R20 repair53-r5 production repair "
      "is already applied."
    )
  else:
    if OLD_TARGET_BLOCK not in function_source:
      raise RuntimeError(
        "repair53-r3c target block was not found in "
        + FUNCTION_NAME
      )

    if OLD_AFTER_EXCLUSION not in function_source:
      raise RuntimeError(
        "post-exclusion anchor was not found in "
        + FUNCTION_NAME
      )

    updated_function = function_source.replace(
      OLD_TARGET_BLOCK,
      NEW_TARGET_BLOCK,
      1,
    )
    updated_function = updated_function.replace(
      OLD_AFTER_EXCLUSION,
      NEW_AFTER_EXCLUSION,
      1,
    )

    updated_source = _replace_function(
      source,
      FUNCTION_NAME,
      updated_function,
    )

    ast.parse(
      updated_source
    )

    BACKUP_DIR.mkdir(
      parents=True,
      exist_ok=True,
    )
    shutil.copy2(
      PRODUCTION,
      BACKUP_DIR
      / PRODUCTION.name,
    )

    PRODUCTION.write_text(
      updated_source,
      encoding="utf-8",
    )

    print(
      "updated production:",
      PRODUCTION.relative_to(
        REPO_ROOT
      ),
    )
    print(
      "backup:",
      BACKUP_DIR
      / PRODUCTION.name,
    )

  if not TEST_SOURCE.exists():
    raise RuntimeError(
      "missing packaged test: "
      + str(
        TEST_SOURCE
      )
    )

  if TEST_TARGET.exists():
    BACKUP_DIR.mkdir(
      parents=True,
      exist_ok=True,
    )
    shutil.copy2(
      TEST_TARGET,
      BACKUP_DIR
      / TEST_TARGET.name,
    )

  shutil.copy2(
    TEST_SOURCE,
    TEST_TARGET,
  )

  print(
    "updated focused test:",
    TEST_TARGET.relative_to(
      REPO_ROOT
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
