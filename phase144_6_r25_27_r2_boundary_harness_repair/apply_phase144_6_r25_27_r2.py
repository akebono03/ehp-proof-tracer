from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = (
  ROOT
  / "phase144_6_r25_27_proof_edge_ownership_boundary_audit"
  / "audit_phase144_6_r25_27.py"
)


def main() -> int:
  source = AUDIT.read_text(
    encoding="utf-8",
  )

  old = """def _closure_from_block(
  dependencies,
  start_index,
  boundary_indices,
):
  visited = set()
  active = set()

  def visit(
    block_index,
  ):
    if block_index in boundary_indices:
      return

    if block_index in visited:
      return

    if block_index in active:
      return

    active.add(
      block_index
    )

    for dependency_index in dependencies[
      block_index
    ]:
      visit(
        dependency_index
      )

    active.remove(
      block_index
    )
    visited.add(
      block_index
    )

  visit(
    start_index
  )

  return frozenset(
    visited
  )
"""

  new = """def _closure_from_block(
  dependencies,
  start_index,
  boundary_indices,
):
  visited = set()
  active = set()

  def visit(
    block_index,
  ):
    if block_index in boundary_indices:
      return

    if block_index in visited:
      return

    if block_index in active:
      return

    active.add(
      block_index
    )

    for dependency_index in dependencies[
      block_index
    ]:
      visit(
        dependency_index
      )

    active.remove(
      block_index
    )
    visited.add(
      block_index
    )

  if start_index not in boundary_indices:
    visit(
      start_index
    )

  return frozenset(
    visited
  )
"""

  if new in source:
    print(
      "R25-27-R2 audit harness repair is already applied."
    )
    return 0

  if old not in source:
    raise RuntimeError(
      "Expected R25-27 _closure_from_block implementation "
      "was not found."
    )

  AUDIT.write_text(
    source.replace(
      old,
      new,
      1,
    ),
    encoding="utf-8",
  )

  print(
    "R25-27-R2 audit harness repair applied."
  )
  print(
    "Production code changes: none."
  )
  print(
    "Existing test changes: none."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
