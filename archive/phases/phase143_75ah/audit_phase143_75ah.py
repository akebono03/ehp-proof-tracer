from collections import Counter
from dataclasses import fields
import runpy

import toda_proof_narrative_renderer as narrative
from toda_rules import (
  TodaLemma57TwoIota5ImageMembershipStatement,
)

captured = []
original = narrative.render_toda_proof_statement_latex


def capturing_renderer(statement):
  if isinstance(
    statement,
    TodaLemma57TwoIota5ImageMembershipStatement,
  ):
    captured.append(statement)

  return original(statement)


def main():
  print("=" * 78)
  print(
    "Phase 143-75AH "
    "TodaLemma57TwoIota5ImageMembershipStatement audit"
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
        TodaLemma57TwoIota5ImageMembershipStatement
      )
    ),
  )

  element_types = Counter()
  group_types = Counter()
  group_signatures = Counter()

  for index, statement in enumerate(
    unique,
    start=1,
  ):
    element_types[
      type(statement.element).__name__
    ] += 1
    group_types[
      type(statement.source_group).__name__
    ] += 1

    signature = (
      repr(
        statement.source_group.group_dimension
      ),
      repr(
        statement.source_group.sphere_dimension
      ),
    )
    group_signatures[signature] += 1

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
      "  source group type:",
      type(statement.source_group).__name__,
    )
    print(
      "  source group:",
      repr(statement.source_group),
    )
    print(
      "  source group dimension:",
      repr(
        statement.source_group.group_dimension
      ),
    )
    print(
      "  source sphere dimension:",
      repr(
        statement.source_group.sphere_dimension
      ),
    )
    print(
      "  current narrative rendering:",
      repr(original(statement)),
    )

  print("")
  print("=" * 78)
  print("Cross-instance summary")
  print("=" * 78)
  print(
    "element types:",
    dict(element_types),
  )
  print(
    "source group types:",
    dict(group_types),
  )
  print(
    "source group signatures:",
    dict(group_signatures),
  )
  print("")
  print(
    "Existing operation-query renderer semantics:"
  )
  print(
    "element in 2 iota_5 composed with source_group"
  )
  print(
    "Verify whether all current Narrative "
    "occurrences support reusing that semantic form."
  )
  print(
    "Do not introduce a generic image witness, "
    "map field, or left_factor field."
  )
  print("")
  print("No source files were changed.")
  print("No pytest was run.")


if __name__ == "__main__":
  main()
