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

  final_registration = (
    "_FIXED_COMPONENTS_BY_REFERENCE[\n"
    "  \"(5.1)\"\n"
    "] = _EQUATION_51_COMPONENTS\n\n"
  )

  tracked_marker = (
    "_TRACKED_REFERENCE_LOCATORS = frozenset(\n"
    "  _FIXED_COMPONENTS_BY_REFERENCE\n"
    ")\n"
  )

  final_block = (
    final_registration
    + tracked_marker
  )

  if final_block not in source:
    if tracked_marker not in source:
      raise RuntimeError(
        "tracked reference locator marker not found"
      )

    source = replace_once(
      source,
      tracked_marker,
      final_block,
      "final (5.1) runtime catalog registration",
    )

  BOUNDARY_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )


def verify_source_layout() -> None:
  source = BOUNDARY_PATH.read_text(
    encoding="utf-8"
  )

  registration = (
    "_FIXED_COMPONENTS_BY_REFERENCE[\n"
    "  \"(5.1)\"\n"
    "] = _EQUATION_51_COMPONENTS\n\n"
  )
  tracked = (
    "_TRACKED_REFERENCE_LOCATORS = frozenset(\n"
    "  _FIXED_COMPONENTS_BY_REFERENCE\n"
    ")"
  )

  registration_index = source.rfind(
    registration
  )
  tracked_index = source.find(
    tracked
  )

  if registration_index < 0:
    raise RuntimeError(
      "source self-check failed: final registration missing"
    )

  if tracked_index < 0:
    raise RuntimeError(
      "source self-check failed: tracked locator construction missing"
    )

  if registration_index > tracked_index:
    raise RuntimeError(
      "source self-check failed: registration occurs after tracked locators"
    )


def verify_runtime_catalog() -> None:
  sys.path.insert(
    0,
    str(
      ROOT
    ),
  )

  sys.modules.pop(
    "toda_literature_statement_boundary",
    None,
  )

  module = importlib.import_module(
    "toda_literature_statement_boundary"
  )

  components = (
    module.get_toda_fixed_statement_components(
      "(5.1)"
    )
  )

  if len(
    components
  ) != 1:
    raise RuntimeError(
      "runtime self-check failed: expected one (5.1) component, "
      f"found {len(components)}"
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
  verify_source_layout()
  verify_runtime_catalog()

  print(
    "Phase 159 pi_4^3 repair2g fix4 applied."
  )
  print(
    "Changed: toda_literature_statement_boundary.py"
  )
  print(
    "Source self-check: final registration is immediately before "
    "_TRACKED_REFERENCE_LOCATORS."
  )
  print(
    "Runtime self-check: "
    "(5.1) / basic_sphere_group_relations registered."
  )
  print(
    "Production scope: final active catalog registration only."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
