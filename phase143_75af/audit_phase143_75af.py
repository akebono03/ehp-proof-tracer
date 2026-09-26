from collections import Counter
from dataclasses import fields
import runpy

import toda_proof_narrative_renderer as narrative
from toda_rules import (
  TodaProp44FirstSummandRestrictionStatement,
)

captured = []
original = narrative.render_toda_proof_statement_latex


def signature(statement):
  decomposition = statement.decomposition_map
  suspension = statement.suspension_map

  source = decomposition.source_group
  summands = getattr(source, "summands", ())

  return (
    repr(decomposition.target_group),
    repr(summands[0]) if summands else None,
    repr(suspension.source_group),
    repr(suspension.target_group),
    repr(decomposition.formula),
  )


def capturing_renderer(statement):
  if isinstance(
    statement,
    TodaProp44FirstSummandRestrictionStatement,
  ):
    captured.append(statement)

  return original(statement)


def main():
  print("=" * 78)
  print(
    "Phase 143-75AF "
    "TodaProp44FirstSummandRestrictionStatement audit"
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
        TodaProp44FirstSummandRestrictionStatement
      )
    ),
  )

  relation_counts = Counter()
  formula_counts = Counter()

  for index, statement in enumerate(
    unique,
    start=1,
  ):
    decomposition = statement.decomposition_map
    suspension = statement.suspension_map
    summands = getattr(
      decomposition.source_group,
      "summands",
      (),
    )

    first_summand = (
      summands[0]
      if summands
      else None
    )

    relation = (
      first_summand
      == suspension.source_group,
      decomposition.target_group
      == suspension.target_group,
    )
    relation_counts[relation] += 1
    formula_counts[
      type(decomposition.formula).__name__
    ] += 1

    print("")
    print(f"Unique statement {index}")
    print(
      "  decomposition map type:",
      type(decomposition).__name__,
    )
    print(
      "  source summand count:",
      len(summands),
    )
    print(
      "  first summand:",
      repr(first_summand),
    )
    print(
      "  suspension source:",
      repr(suspension.source_group),
    )
    print(
      "  target:",
      repr(decomposition.target_group),
    )
    print(
      "  suspension target:",
      repr(suspension.target_group),
    )
    print(
      "  formula type:",
      type(decomposition.formula).__name__,
    )
    print(
      "  formula:",
      repr(decomposition.formula),
    )
    print(
      "  first summand == E source:",
      first_summand
      == suspension.source_group,
    )
    print(
      "  decomposition target == E target:",
      decomposition.target_group
      == suspension.target_group,
    )
    print(
      "  current semantic rendering:",
      original(statement),
    )

  print("")
  print("=" * 78)
  print("Cross-instance summary")
  print("=" * 78)
  print(
    "relation distribution:",
    dict(relation_counts),
  )
  print(
    "formula-type distribution:",
    dict(formula_counts),
  )
  print("")
  print(
    "Interpretation to verify:"
  )
  print(
    "the Proposition 4.4 decomposition map, "
    "restricted to its first direct summand, "
    "is the recorded suspension map E."
  )
  print("")
  print(
    "Do NOT interpret this statement itself "
    "as injectivity or isomorphism."
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
