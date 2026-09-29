from collections import Counter, defaultdict
from dataclasses import fields, is_dataclass

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
)


TARGET_TYPES = (
  Toda45IsomorphismStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
)


def _value_shape(value):
  if value is None:
    return "None"

  value_type = type(value).__name__

  if is_dataclass(value):
    return (
      value_type
      + "("
      + ", ".join(
        field.name
        for field in fields(value)
      )
      + ")"
    )

  if isinstance(
    value,
    (
      tuple,
      list,
    ),
  ):
    item_types = sorted(
      {
        type(item).__name__
        for item in value
      }
    )
    return (
      value_type
      + "["
      + ", ".join(item_types)
      + "]"
    )

  return value_type


def main():
  scanned_groups = 0
  scanned_nodes = 0
  errors = []
  occurrences = Counter()
  field_shapes = defaultdict(Counter)
  sample_values = {}
  groups = defaultdict(set)

  for k in range(8):
    for n in range(2, 16):
      scanned_groups += 1

      try:
        report = build_standard_toda_report(
          n=n,
          k=k,
        )
        group_result = (
          report.candidates[
            0
          ].source_candidate.group_result
        )
        replay = build_toda_group_result_proof_replay(
          group_result,
          max_depth=7,
        )
        presentation = build_toda_group_proof_presentation(
          replay
        )
      except Exception as exc:
        errors.append(
          (
            n,
            k,
            type(exc).__name__,
            str(exc),
          )
        )
        continue

      for node in presentation.nodes:
        scanned_nodes += 1
        statement = node.proof_step.conclusion

        if not isinstance(
          statement,
          TARGET_TYPES,
        ):
          continue

        statement_type = type(
          statement
        ).__name__
        occurrences[
          statement_type
        ] += 1
        groups[
          statement_type
        ].add(
          (
            n,
            k,
          )
        )

        if not is_dataclass(
          statement
        ):
          field_shapes[
            statement_type
          ][
            "<not dataclass>"
          ] += 1
          continue

        shape = tuple(
          (
            field.name,
            _value_shape(
              getattr(
                statement,
                field.name,
              )
            ),
          )
          for field in fields(
            statement
          )
        )
        field_shapes[
          statement_type
        ][
          shape
        ] += 1

        sample_values.setdefault(
          (
            statement_type,
            shape,
          ),
          (
            n,
            k,
            repr(statement),
          ),
        )

  print("=" * 78)
  print(
    "Phase 143-75B top-three "
    "semantic-structure audit"
  )
  print(
    "range: n=2..15, k=0..7, depth=7"
  )
  print(
    f"scanned groups: {scanned_groups}"
  )
  print(
    f"scanned presentation nodes: "
    f"{scanned_nodes}"
  )
  print("=" * 78)

  for target_type in TARGET_TYPES:
    statement_type = target_type.__name__
    print()
    print(statement_type)
    print(
      "  occurrences: "
      f"{occurrences[statement_type]}"
    )
    print(
      "  groups: "
      f"{len(groups[statement_type])}"
    )

    for shape, count in (
      field_shapes[
        statement_type
      ].most_common()
    ):
      print(
        f"  shape ({count} occurrences):"
      )
      if isinstance(
        shape,
        tuple,
      ):
        for (
          field_name,
          value_shape,
        ) in shape:
          print(
            f"    {field_name}: "
            f"{value_shape}"
          )
      else:
        print(
          f"    {shape}"
        )

      sample = sample_values.get(
        (
          statement_type,
          shape,
        )
      )
      if sample is not None:
        n, k, value = sample
        print(
          f"    sample group: "
          f"pi_{n+k}^{n}"
        )
        print(
          f"    sample repr: {value}"
        )

  print()
  print(f"errors: {len(errors)}")
  for error in errors[:20]:
    print("  -", error)

  print()
  print("=" * 78)
  if errors:
    print(
      "AUDIT ERROR: inspect the errors "
      "before choosing a renderer."
    )
  else:
    print(
      "PASS: semantic field shapes for "
      "the three highest-frequency "
      "fallback statement types were "
      "collected."
    )
    print(
      "Use these shapes to decide whether "
      "existing map/group/expression "
      "renderers are sufficient for the "
      "smallest generic implementation."
    )


if __name__ == "__main__":
  main()
