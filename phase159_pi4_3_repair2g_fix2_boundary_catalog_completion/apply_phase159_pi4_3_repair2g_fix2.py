from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
BOUNDARY_PATH = ROOT / "toda_literature_statement_boundary.py"
TEST_PATH = (
  ROOT
  / "tests"
  / "test_phase159_pi4_3_repair2g_reference_policy.py"
)


def function_span(
  source: str,
  function_name: str,
) -> tuple[int, int]:
  marker = "def " + function_name + "("
  start = source.find(marker)
  if start < 0:
    raise RuntimeError(
      f"{function_name}: function not found"
    )

  match = re.search(
    r"\n(?=def [A-Za-z0-9_]+\()",
    source[start + 1:],
  )
  if match is None:
    return start, len(source)

  end = start + 1 + match.start() + 1
  return start, end


def patch_boundary_catalog() -> None:
  source = BOUNDARY_PATH.read_text(
    encoding="utf-8"
  )

  if "_EQUATION_51_COMPONENTS = (" not in source:
    anchor = "\n\n_PROPOSITION_22_COMPONENTS = (\n"
    if anchor not in source:
      raise RuntimeError(
        "boundary catalog anchor for Proposition 2.2 not found"
      )

    addition = '''

_EQUATION_51_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="basic_sphere_group_relations",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
)
'''
    source = source.replace(
      anchor,
      addition + anchor,
      1,
    )

  dict_marker = "_FIXED_COMPONENTS_BY_REFERENCE = {\n"
  if dict_marker not in source:
    raise RuntimeError(
      "_FIXED_COMPONENTS_BY_REFERENCE dictionary not found"
    )

  dict_start = source.index(dict_marker)
  dict_end = source.index("\n}\n", dict_start) + 3
  dict_source = source[dict_start:dict_end]

  if '  "(5.1)": _EQUATION_51_COMPONENTS,\n' not in dict_source:
    insertion = '  "(5.1)": _EQUATION_51_COMPONENTS,\n'
    source = (
      source[:dict_start + len(dict_marker)]
      + insertion
      + source[dict_start + len(dict_marker):]
    )

  fixed_map_marker = "_FIXED_RULE_COMPONENT_KEYS = {\n"
  if fixed_map_marker not in source:
    raise RuntimeError(
      "_FIXED_RULE_COMPONENT_KEYS dictionary not found"
    )
  fixed_start = source.index(fixed_map_marker)
  fixed_end = source.index("\n}\n", fixed_start) + 3
  fixed_source = source[fixed_start:fixed_end]

  required_fixed = (
    (
      "Toda (5.1) below-diagonal zero",
      "basic_sphere_group_relations",
    ),
    (
      "Toda (5.1) diagonal free cyclic",
      "basic_sphere_group_relations",
    ),
  )

  for rule_name, component_key in reversed(required_fixed):
    line = (
      f'  "{rule_name}": '
      f'"{component_key}",\n'
    )
    if line not in fixed_source:
      source = (
        source[:fixed_start + len(fixed_map_marker)]
        + line
        + source[fixed_start + len(fixed_map_marker):]
      )
      fixed_end += len(line)
      fixed_source = source[fixed_start:fixed_end]

  locator_marker = "_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME = {\n"
  if locator_marker not in source:
    raise RuntimeError(
      "_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME dictionary not found"
    )
  locator_start = source.index(locator_marker)
  locator_end = source.index("\n}\n", locator_start) + 3
  locator_source = source[locator_start:locator_end]

  required_locators = (
    "Toda (5.1) below-diagonal zero",
    "Toda (5.1) diagonal free cyclic",
  )

  for rule_name in reversed(required_locators):
    line = f'  "{rule_name}": "(5.1)",\n'
    if line not in locator_source:
      source = (
        source[:locator_start + len(locator_marker)]
        + line
        + source[locator_start + len(locator_marker):]
      )
      locator_end += len(line)
      locator_source = source[locator_start:locator_end]

  BOUNDARY_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )


def patch_focused_test() -> None:
  source = TEST_PATH.read_text(
    encoding="utf-8"
  )

  function_name = (
    "test_phase159_repair2g_phase49_keeps_given_contract_with_51_metadata"
  )
  start, end = function_span(
    source,
    function_name,
  )

  replacement = '''def test_phase159_repair2g_phase49_keeps_given_contract_with_51_metadata():
  phase49 = _build_phase49_result()

  assert all(
    step.rule.value == "given"
    for step in phase49[
      "premise_steps"
    ]
  )

  fixed_51_steps = tuple(
    step
    for step in phase49[
      "premise_steps"
    ]
    if (
      extract_toda_group_proof_step_literature_reference(
        step
      )
      is not None
      and (
        extract_toda_group_proof_step_literature_reference(
          step
        ).locator
        == "(5.1)"
      )
    )
  )
  fixed_51_conclusions = tuple(
    step.conclusion
    for step in fixed_51_steps
  )

  from low_dimensional_facts import (
    pi_2_1_zero_fact,
    pi_3_3_free_cyclic_fact,
  )

  assert (
    pi_2_1_zero_fact()
    in fixed_51_conclusions
  )
  assert (
    pi_3_3_free_cyclic_fact()
    in fixed_51_conclusions
  )
'''

  source = (
    source[:start]
    + replacement
    + source[end:]
  )

  TEST_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )


def main() -> int:
  patch_boundary_catalog()
  patch_focused_test()

  print(
    "Phase 159 pi_4^3 repair2g fix2 applied."
  )
  print(
    "Changed: toda_literature_statement_boundary.py"
  )
  print(
    "Changed: tests/"
    "test_phase159_pi4_3_repair2g_reference_policy.py"
  )
  print(
    "Production scope: complete missing (5.1) fixed-component catalog entry only."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
