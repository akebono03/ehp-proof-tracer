from __future__ import annotations

from pathlib import Path
import importlib
import sys


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


def patch_boundary_catalog() -> None:
  source = BOUNDARY_PATH.read_text(
    encoding="utf-8"
  )

  if "_EQUATION_51_COMPONENTS = (" not in source:
    anchor = "\n\n_PROPOSITION_22_COMPONENTS = (\n"
    addition = (
      "\n\n"
      "_EQUATION_51_COMPONENTS = (\n"
      "  TodaFixedStatementComponent(\n"
      "    reference_locator=\"(5.1)\",\n"
      "    component_key=\"basic_sphere_group_relations\",\n"
      "    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,\n"
      "    order=None,\n"
      "    range_text=None,\n"
      "    range_is_explicit_in_current_aggregate=True,\n"
      "  ),\n"
      ")\n"
    )
    source = replace_once(
      source,
      anchor,
      addition + anchor,
      "(5.1) fixed component definition",
    )

  registration = (
    "_FIXED_COMPONENTS_BY_REFERENCE[\n"
    "  \"(5.1)\"\n"
    "] = _EQUATION_51_COMPONENTS\n\n"
  )

  if registration not in source:
    anchor = "\n\n_FIXED_RULE_COMPONENT_KEYS = {\n"

    source = replace_once(
      source,
      anchor,
      "\n\n"
      + registration
      + "_FIXED_RULE_COMPONENT_KEYS = {\n",
      "(5.1) runtime catalog registration",
    )

  BOUNDARY_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )


def verify_runtime_catalog() -> None:
  sys.path.insert(
    0,
    str(
      ROOT
    ),
  )

  module = importlib.import_module(
    "toda_literature_statement_boundary"
  )

  component = (
    module.get_toda_fixed_statement_component(
      "(5.1)",
      "basic_sphere_group_relations",
    )
  )

  if component.reference_locator != "(5.1)":
    raise RuntimeError(
      "runtime self-check failed: unexpected reference locator"
    )

  if (
    component.component_key
    != "basic_sphere_group_relations"
  ):
    raise RuntimeError(
      "runtime self-check failed: unexpected component key"
    )

  if (
    "(5.1)"
    not in module._TRACKED_REFERENCE_LOCATORS
  ):
    raise RuntimeError(
      "runtime self-check failed: "
      "(5.1) missing from tracked reference locators"
    )


def main() -> int:
  patch_boundary_catalog()
  verify_runtime_catalog()

  print(
    "Phase 159 pi_4^3 repair2g fix3 applied."
  )
  print(
    "Changed: toda_literature_statement_boundary.py"
  )
  print(
    "Runtime self-check: "
    "(5.1) / basic_sphere_group_relations registered."
  )
  print(
    "Production scope: runtime catalog registration only."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
