from collections import Counter
from dataclasses import fields
import runpy

import toda_proof_narrative_renderer as narrative
from toda_rules import (
  TodaLemma514SigmaDoublePrimeStatement,
)

captured = []
original = narrative.render_toda_proof_statement_latex


def capturing_renderer(statement):
  if isinstance(
    statement,
    TodaLemma514SigmaDoublePrimeStatement,
  ):
    captured.append(statement)

  return original(statement)


def main():
  print("=" * 78)
  print(
    "Phase 143-75AK "
    "TodaLemma514SigmaDoublePrimeStatement semantic structure audit"
  )
  print("=" * 78)

  narrative.render_toda_proof_statement_latex = capturing_renderer

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
        TodaLemma514SigmaDoublePrimeStatement
      )
    ),
  )

  inventory = Counter()

  for index, statement in enumerate(unique, start=1):
    print("")
    print(f"Unique statement {index}")

    for field in fields(statement):
      value = getattr(statement, field.name)
      inventory[
        (field.name, type(value).__name__)
      ] += 1
      print(
        f"  {field.name} type:",
        type(value).__name__,
      )
      print(
        f"  {field.name}:",
        repr(value),
      )

    print(
      "  current narrative rendering:",
      repr(original(statement)),
    )

  print("")
  print("=" * 78)
  print("Cross-instance summary")
  print("=" * 78)

  for key, count in sorted(inventory.items()):
    print(f"{key[0]} / {key[1]}: {count}")

  print("")
  print("GitHub Phase 75 tests explicitly verify:")
  print("  sigma_double_prime is sigma-double-prime in pi_13^6")
  print(
    "  iterated_suspension_relation: "
    "E^3 sigma-double-prime = 4x E alpha*"
  )
  print(
    "  double_relation: "
    "2 sigma-double-prime = E sigma-triple-prime"
  )
  print(
    "  hopf_relation: "
    "H(sigma-double-prime) = eta_11^2"
  )
  print("")
  print(
    "Audit whether these relations are present as "
    "first-class fields in every runtime instance."
  )
  print("")
  print("No source files were changed.")
  print("No pytest was run.")


if __name__ == "__main__":
  main()
