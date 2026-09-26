from collections import Counter
from dataclasses import fields
import runpy

import toda_proof_narrative_renderer as narrative
from toda_rules import (
  TodaProp59DeltaKernelStatement,
)

captured = []
original = narrative.render_toda_proof_statement_latex


def capturing_renderer(statement):
  if isinstance(
    statement,
    TodaProp59DeltaKernelStatement,
  ):
    captured.append(statement)

  return original(statement)


def main():
  print("=" * 78)
  print(
    "Phase 143-75AI "
    "TodaProp59DeltaKernelStatement semantic structure audit"
  )
  print("=" * 78)

  narrative.render_toda_proof_statement_latex = (
    capturing_renderer
  )

  try:
    runpy.run_path(
      "phase143_75u/"
      "audit_phase143_75u_remaining_fallbacks.py",
      run_name="__main__",
    )
  finally:
    narrative.render_toda_proof_statement_latex = original

  unique = []
  for statement in captured:
    if statement not in unique:
      unique.append(statement)

  print("")
  print("=" * 78)
  print("Target semantic structure")
  print("=" * 78)
  print("raw renderer calls:", len(captured))
  print(
    "unique object identities:",
    len({id(x) for x in captured}),
  )
  print("unique statement equalities:", len(unique))
  print(
    "field names:",
    tuple(
      field.name
      for field in fields(
        TodaProp59DeltaKernelStatement
      )
    ),
  )

  map_types = Counter()
  kernel_types = Counter()
  signatures = Counter()

  for index, statement in enumerate(
    unique,
    start=1,
  ):
    map_types[type(statement.map).__name__] += 1
    kernel_types[
      type(statement.kernel_group).__name__
    ] += 1

    signature = (
      repr(statement.map),
      repr(statement.kernel_group),
    )
    signatures[signature] += 1

    print("")
    print(f"Unique statement {index}")
    print(
      "  map type:",
      type(statement.map).__name__,
    )
    print("  map:", repr(statement.map))
    print(
      "  map source:",
      repr(statement.map.source_group),
    )
    print(
      "  map target:",
      repr(statement.map.target_group),
    )
    print(
      "  kernel group type:",
      type(statement.kernel_group).__name__,
    )
    print(
      "  kernel group:",
      repr(statement.kernel_group),
    )
    print(
      "  current narrative rendering:",
      repr(original(statement)),
    )

  print("")
  print("=" * 78)
  print("Cross-instance summary")
  print("=" * 78)
  print("map types:", dict(map_types))
  print("kernel group types:", dict(kernel_types))
  print(
    "unique map/kernel signatures:",
    len(signatures),
  )
  print("")
  print("GitHub Phase 70 canonical expectation:")
  print(
    "  TodaProp59DeltaKernelStatement("
    "map=Delta: pi_8^5 -> pi_6^2, "
    "kernel_group=Z/2{4 nu_5})"
  )
  print("")
  print(
    "Candidate semantics to verify from runtime:"
  )
  print(
    "  Ker(Delta: source -> target) = kernel_group"
  )
  print("")
  print("No source files were changed.")
  print("No pytest was run.")


if __name__ == "__main__":
  main()
