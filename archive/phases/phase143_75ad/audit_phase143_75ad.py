import runpy
from collections import Counter
from dataclasses import fields

import toda_proof_narrative_renderer as narrative
from toda_human_readable_renderer import (
  _render_scalar_latex,
  render_toda_expression_latex,
)
from toda_rules import (
  TodaLemma54DoubleSuspensionUpToSignStatement,
)
from test_phase60_toda36_specialization import (
  build_phase60_6_data,
)


TARGET_AUDIT = (
  "phase143_75u/"
  "audit_phase143_75u_remaining_fallbacks.py"
)


def render_value(value):
  try:
    return render_toda_expression_latex(value)
  except TypeError:
    try:
      return _render_scalar_latex(value)
    except TypeError:
      return repr(value)


def signature(statement):
  return tuple(
    (
      field.name,
      type(
        getattr(statement, field.name)
      ).__name__,
      render_value(
        getattr(statement, field.name)
      ),
    )
    for field in fields(statement)
  )


def equality_key(statement):
  try:
    hash(statement)
  except TypeError:
    return repr(statement)
  return statement


def main():
  canonical = (
    build_phase60_6_data()[
      "final_step"
    ].conclusion
  )

  print("=" * 78)
  print(
    "Phase 143-75AD DoubleSuspensionUpToSign "
    "20-occurrence cross-audit"
  )
  print("=" * 78)
  print("Canonical statement")
  print("-" * 78)
  print("type:", type(canonical).__name__)
  print(
    "fields:",
    tuple(
      field.name
      for field in fields(canonical)
    ),
  )

  for field in fields(canonical):
    value = getattr(
      canonical,
      field.name,
    )
    print(
      f"{field.name}: "
      f"{type(value).__name__}: "
      f"{render_value(value)}"
    )

  print(
    "current semantic rendering:",
    narrative.render_toda_proof_statement_latex(
      canonical
    ),
  )

  captured = []
  original = (
    narrative.render_toda_proof_statement_latex
  )

  def capturing_renderer(statement):
    if isinstance(
      statement,
      TodaLemma54DoubleSuspensionUpToSignStatement,
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
    signature(statement)
    for statement in captured
  )

  print("")
  print("=" * 78)
  print(
    "Captured DoubleSuspensionUpToSign "
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
    "unique field-value signatures:",
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
  print("Field-value signature distribution")
  print("-" * 78)
  for item, count in sorted(
    signature_counts.items(),
    key=lambda pair: (
      -pair[1],
      repr(pair[0]),
    ),
  ):
    print(f"{count} renderer call(s)")
    for name, type_name, rendered in item:
      print(
        f"  {name}: "
        f"{type_name}: {rendered}"
      )

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
  print("")
  print("No source files were changed.")
  print("No pytest was run.")


if __name__ == "__main__":
  main()
