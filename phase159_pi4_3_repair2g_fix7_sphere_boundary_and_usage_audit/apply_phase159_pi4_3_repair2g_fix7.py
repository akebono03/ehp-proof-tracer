
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOUNDARY_PATH = ROOT / "toda_literature_statement_boundary.py"


def replace_once(
  source: str,
  old: str,
  new: str,
  description: str,
) -> str:
  count = source.count(old)

  if count != 1:
    raise RuntimeError(
      f"{description}: expected exactly one match, found {count}"
    )

  return source.replace(
    old,
    new,
    1,
  )


def main() -> int:
  source = BOUNDARY_PATH.read_text(
    encoding="utf-8"
  )

  rule_name = (
    "Toda (5.1) sphere connectivity zero"
  )

  component_assignment = (
    '_FIXED_RULE_COMPONENT_KEYS[\n'
    '  "Toda (5.1) sphere connectivity zero"\n'
    '] = "sphere_connectivity_zero"\n\n'
  )
  locator_assignment = (
    '_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME[\n'
    '  "Toda (5.1) sphere connectivity zero"\n'
    '] = "(5.1)"\n\n'
  )

  tracked_marker = (
    "_TRACKED_REFERENCE_LOCATORS = frozenset(\n"
    "  _FIXED_COMPONENTS_BY_REFERENCE\n"
    ")\n"
  )

  if component_assignment not in source:
    if tracked_marker not in source:
      raise RuntimeError(
        "_TRACKED_REFERENCE_LOCATORS marker not found"
      )

    source = replace_once(
      source,
      tracked_marker,
      component_assignment
      + locator_assignment
      + tracked_marker,
      "sphere connectivity fixed mapping",
    )
  elif locator_assignment not in source:
    raise RuntimeError(
      "component mapping exists without locator mapping"
    )

  if (
    "basic_sphere_group_relations"
    in source
  ):
    raise RuntimeError(
      "obsolete basic_sphere_group_relations "
      "still present in boundary source"
    )

  BOUNDARY_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159 pi_4^3 repair2g fix7 applied."
  )
  print(
    "Changed: toda_literature_statement_boundary.py"
  )
  print(
    "Added fixed mapping: "
    "Toda (5.1) sphere connectivity zero "
    "-> sphere_connectivity_zero"
  )
  print(
    "No Reference usage filter changed."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
