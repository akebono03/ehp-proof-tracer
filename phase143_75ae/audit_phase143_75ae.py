import runpy
from collections import Counter
from dataclasses import fields

import toda_proof_narrative_renderer as narrative
from toda_rules import (
  TodaSuspensionZeroStatement,
)
from test_phase73_pi9_3_zero import (
  build_phase73_4_data,
)


TARGET_AUDIT = (
  "phase143_75u/"
  "audit_phase143_75u_remaining_fallbacks.py"
)


def group_signature(group):
  return (
    type(group).__name__,
    getattr(group, "group_dimension", None),
    getattr(group, "sphere_dimension", None),
  )


def statement_signature(statement):
  suspension_map = statement.map
  return (
    type(suspension_map).__name__,
    group_signature(
      suspension_map.source_group
    ),
    group_signature(
      suspension_map.target_group
    ),
  )


def equality_key(statement):
  try:
    hash(statement)
  except TypeError:
    return repr(statement)
  return statement


def print_statement(label, statement):
  print(label)
  print("  type:", type(statement).__name__)
  print(
    "  fields:",
    tuple(
      field.name
      for field in fields(statement)
    ),
  )
  print(
    "  map type:",
    type(statement.map).__name__,
  )
  print(
    "  source:",
    group_signature(
      statement.map.source_group
    ),
  )
  print(
    "  target:",
    group_signature(
      statement.map.target_group
    ),
  )
  print(
    "  current semantic rendering:",
    narrative.render_toda_proof_statement_latex(
      statement
    ),
  )


def main():
  data = build_phase73_4_data()

  print("=" * 78)
  print(
    "Phase 143-75AE TodaSuspensionZeroStatement "
    "25-occurrence cross-audit"
  )
  print("=" * 78)

  print_statement(
    "Canonical pi8^2 suspension-zero statement",
    data["pi8_zero_step"].conclusion,
  )
  print("")
  print_statement(
    "Canonical pi7^2 suspension-zero statement",
    data["pi7_zero_step"].conclusion,
  )

  captured = []
  original = (
    narrative.render_toda_proof_statement_latex
  )

  def capturing_renderer(statement):
    if isinstance(
      statement,
      TodaSuspensionZeroStatement,
    ):
      captured.append(statement)
    return original(statement)

  narrative.render_toda_proof_statement_latex = (
    capturing_renderer
  )

  try:
    print("")
    print(
      "Established Phase 143-75U inventory"
    )
    print("-" * 78)
    runpy.run_path(
      TARGET_AUDIT,
      run_name="__main__",
    )
  finally:
    narrative.render_toda_proof_statement_latex = (
      original
    )

  identity_counts = Counter(
    id(statement)
    for statement in captured
  )
  equality_counts = Counter(
    equality_key(statement)
    for statement in captured
  )
  signature_counts = Counter(
    statement_signature(statement)
    for statement in captured
  )

  print("")
  print("=" * 78)
  print(
    "Captured TodaSuspensionZeroStatement "
    "dedup/value distribution"
  )
  print("=" * 78)
  print(
    "raw renderer calls:",
    len(captured),
  )
  print(
    "unique object identities:",
    len(identity_counts),
  )
  print(
    "unique statement equalities:",
    len(equality_counts),
  )
  print(
    "unique map signatures:",
    len(signature_counts),
  )

  print("")
  print("Object identity call-count distribution")
  print("-" * 78)
  for call_count, object_count in sorted(
    Counter(
      identity_counts.values()
    ).items()
  ):
    print(
      f"{object_count} object(s) x "
      f"{call_count} renderer call(s)"
    )

  print("")
  print("Map signature distribution")
  print("-" * 78)
  for item, count in sorted(
    signature_counts.items(),
    key=lambda pair: (
      -pair[1],
      repr(pair[0]),
    ),
  ):
    map_type, source, target = item
    print(f"{count} renderer call(s)")
    print(f"  map: {map_type}")
    print(f"  source: {source}")
    print(f"  target: {target}")

  print("")
  print("Audit interpretation")
  print("-" * 78)
  print(
    "The Phase 143-75U inventory is authoritative "
    "for fallback occurrences/groups."
  )
  print(
    "Raw renderer calls are diagnostic only and "
    "must not be treated as occurrence counts."
  )
  print(
    "TodaSuspensionZeroStatement describes a zero "
    "suspension map, not an element-level equation."
  )
  print("")
  print("No source files were changed.")
  print("No pytest was run.")


if __name__ == "__main__":
  main()
