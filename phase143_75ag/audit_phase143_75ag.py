from collections import Counter
from dataclasses import fields
import runpy

import toda_proof_narrative_renderer as narrative
from toda_rules import (
  TodaLemma510BracketModuloStatement,
)

captured = []
original = narrative.render_toda_proof_statement_latex


def capturing_renderer(statement):
  if isinstance(
    statement,
    TodaLemma510BracketModuloStatement,
  ):
    captured.append(statement)

  return original(statement)


def main():
  print("=" * 78)
  print(
    "Phase 143-75AG "
    "TodaLemma510BracketModuloStatement audit"
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
    narrative.render_toda_proof_statement_latex = (
      original
    )

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
        TodaLemma510BracketModuloStatement
      )
    ),
  )

  modulus_counts = Counter()
  bracket_type_counts = Counter()
  element_type_counts = Counter()
  ambient_type_counts = Counter()
  rendering_counts = Counter()

  for index, statement in enumerate(
    unique,
    start=1,
  ):
    modulus_counts[
      repr(statement.modulus)
    ] += 1
    bracket_type_counts[
      type(statement.bracket).__name__
    ] += 1
    element_type_counts[
      type(statement.element).__name__
    ] += 1
    ambient_type_counts[
      type(statement.ambient_group).__name__
    ] += 1

    rendered = original(statement)
    rendering_counts[
      repr(rendered)
    ] += 1

    print("")
    print(f"Unique statement {index}")
    print(
      "  element type:",
      type(statement.element).__name__,
    )
    print(
      "  element:",
      repr(statement.element),
    )
    print(
      "  bracket type:",
      type(statement.bracket).__name__,
    )
    print(
      "  bracket:",
      repr(statement.bracket),
    )
    print(
      "  bracket index:",
      repr(
        getattr(
          statement.bracket,
          "index",
          None,
        )
      ),
    )
    print(
      "  ambient group type:",
      type(statement.ambient_group).__name__,
    )
    print(
      "  ambient group:",
      repr(statement.ambient_group),
    )
    print(
      "  modulus type:",
      type(statement.modulus).__name__,
    )
    print(
      "  modulus:",
      repr(statement.modulus),
    )
    print(
      "  current semantic rendering:",
      repr(rendered),
    )

  print("")
  print("=" * 78)
  print("Cross-instance summary")
  print("=" * 78)
  print(
    "modulus distribution:",
    dict(modulus_counts),
  )
  print(
    "element-type distribution:",
    dict(element_type_counts),
  )
  print(
    "bracket-type distribution:",
    dict(bracket_type_counts),
  )
  print(
    "ambient-type distribution:",
    dict(ambient_type_counts),
  )
  print(
    "current-rendering distribution:",
    dict(rendering_counts),
  )

  print("")
  print("Semantic interpretation to verify:")
  print(
    "element belongs to bracket modulo "
    "modulus times ambient_group."
  )
  print(
    "Do not replace this with ordinary "
    "Toda-bracket membership."
  )
  print(
    "Do not introduce generic coset algebra."
  )
  print("")
  print(
    "The Phase 143-75U inventory remains "
    "authoritative for occurrence/group counts."
  )
  print("No source files were changed.")
  print("No pytest was run.")


if __name__ == "__main__":
  main()
