from collections import Counter, defaultdict
from dataclasses import fields, is_dataclass
import runpy

import toda_proof_narrative_renderer as narrative

TARGET_NAMES = {
  "TodaLemma510OrdinaryBracketPlusSuspensionImageStatement",
  "TodaLemma510OrdinaryIndeterminacyDoubleStatement",
  "TodaLemma510OrdinarySuspensionImageInDoubleStatement",
  "TodaLemma510HopfBracketContainsStatement",
  "Toda211OrdinaryEHPExactnessStatement",
  "TodaLemma510Nu6OrdinaryCompositionZeroStatement",
  "TodaLemma510OrdinarySuspensionImageFiniteStatement",
  "TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement",
  "FiniteHomotopyGroupStatement",
  "TodaLemma510IndexedHopfBracketContainsStatement",
  "TodaLemma510Split115Statement",
  "Toda211OrdinaryEHPApplicabilityStatement",
  "TodaLemma510Nu6OrdinaryCompositionReductionStatement",
  "Toda515Sigma8TransportedDecompositionStatement",
  "Toda515Sigma8Prop44SpecializationStatement",
}

captured = defaultdict(list)
original = narrative.render_toda_proof_statement_latex


def capturing_renderer(statement):
  name = type(statement).__name__

  if name in TARGET_NAMES:
    captured[name].append(statement)

  return original(statement)


def unique_equal(values):
  result = []

  for value in values:
    if value not in result:
      result.append(value)

  return result


def main():
  print("=" * 78)
  print("Phase 143-75AO bulk semantic structure audit")
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

  print("")
  print("=" * 78)
  print("All remaining target statement structures")
  print("=" * 78)

  missing = sorted(
    TARGET_NAMES - set(captured)
  )
  print("target types expected:", len(TARGET_NAMES))
  print("target types captured:", len(captured))
  print("missing target types:", missing)

  for name in sorted(captured):
    values = captured[name]
    unique = unique_equal(values)

    print("")
    print("-" * 78)
    print(name)
    print("-" * 78)
    print("raw renderer calls:", len(values))
    print(
      "unique object identities:",
      len({id(value) for value in values}),
    )
    print("unique equal values:", len(unique))

    first = unique[0]

    if is_dataclass(first):
      print(
        "field names:",
        tuple(
          field.name
          for field in fields(first)
        ),
      )

    signatures = Counter()

    for value in unique:
      if is_dataclass(value):
        signature = tuple(
          (
            field.name,
            type(
              getattr(
                value,
                field.name,
              )
            ).__name__,
          )
          for field in fields(value)
        )
        signatures[signature] += 1

    print("field type signatures:")
    for signature, count in signatures.items():
      print(" ", count, "x", signature)

    for index, value in enumerate(
      unique,
      start=1,
    ):
      print("")
      print(f"unique value {index}:")

      if not is_dataclass(value):
        print("  repr:", repr(value))
        continue

      for field in fields(value):
        field_value = getattr(
          value,
          field.name,
        )
        print(
          f"  {field.name} "
          f"[{type(field_value).__name__}]: "
          f"{field_value!r}"
        )

      try:
        rendered = original(value)
      except Exception as exc:
        rendered = (
          f"<ERROR {type(exc).__name__}: "
          f"{exc}>"
        )

      print(
        "  current semantic rendering:",
        repr(rendered),
      )

  print("")
  print("=" * 78)
  print("Bulk audit complete")
  print("=" * 78)
  print("No source files were changed.")
  print("No pytest was run.")
  print(
    "Use these exact runtime fields to group "
    "safe semantic renderer branches."
  )


if __name__ == "__main__":
  main()
