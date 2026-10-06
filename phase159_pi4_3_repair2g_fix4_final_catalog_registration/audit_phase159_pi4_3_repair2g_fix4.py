from pathlib import Path

from toda_literature_statement_boundary import (
  get_toda_fixed_statement_component,
  get_toda_fixed_statement_components,
)


ROOT = Path(__file__).resolve().parents[1]
BOUNDARY_PATH = ROOT / "toda_literature_statement_boundary.py"


def main() -> int:
  print(
    "=== Phase159 repair2g fix4 final catalog audit ==="
  )

  source = BOUNDARY_PATH.read_text(
    encoding="utf-8"
  )

  print(
    "final registration occurrences:",
    source.count(
      "_FIXED_COMPONENTS_BY_REFERENCE[\n"
      "  \"(5.1)\"\n"
      "] = _EQUATION_51_COMPONENTS"
    ),
  )

  components = (
    get_toda_fixed_statement_components(
      "(5.1)"
    )
  )

  print(
    "(5.1) component count:",
    len(
      components
    ),
  )

  for component in components:
    print(
      "  -",
      component.component_key,
      component.statement_role.value,
    )

  component = (
    get_toda_fixed_statement_component(
      "(5.1)",
      "basic_sphere_group_relations",
    )
  )

  print(
    "resolved component:",
    component.component_key,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
