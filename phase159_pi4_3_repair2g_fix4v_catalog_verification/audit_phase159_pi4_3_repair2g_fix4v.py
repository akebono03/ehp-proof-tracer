from toda_literature_statement_boundary import (
  get_toda_fixed_statement_component,
  get_toda_fixed_statement_components,
)


def main() -> int:
  print(
    "=== Phase159 repair2g fix4v catalog verification ==="
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

  for index, component in enumerate(
    components,
    start=1,
  ):
    print(
      f"[{index}] "
      f"key={component.component_key} "
      f"role={component.statement_role.value} "
      f"order={component.order}"
    )

  matching = tuple(
    component
    for component in components
    if (
      component.component_key
      == "basic_sphere_group_relations"
    )
  )

  print(
    "basic_sphere_group_relations matches:",
    len(
      matching
    ),
  )

  if len(
    matching
  ) != 1:
    raise RuntimeError(
      "expected exactly one "
      "(5.1) / basic_sphere_group_relations component, "
      f"found {len(matching)}"
    )

  resolved = (
    get_toda_fixed_statement_component(
      "(5.1)",
      "basic_sphere_group_relations",
    )
  )

  print(
    "resolved component:",
    resolved.component_key,
  )
  print(
    "catalog verification: PASS"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
