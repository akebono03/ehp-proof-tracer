from collections import Counter, defaultdict
from dataclasses import fields

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGET_NAME = "TodaProp44SuspensionInjectiveStatement"
EXPECTED_OCCURRENCES = 55


def _value_signature(value):
  value_type = type(value).__name__

  if hasattr(value, "__dataclass_fields__"):
    return (
      value_type,
      tuple(
        field.name
        for field in fields(value)
      ),
    )

  return (
    value_type,
    (),
  )


def main():
  occurrences = 0
  groups = set()
  statement_field_signatures = Counter()
  map_type_counts = Counter()
  map_field_signatures = Counter()
  source_group_type_counts = Counter()
  target_group_type_counts = Counter()
  rule_counts = Counter()
  rule_to_shape_counts = defaultdict(Counter)
  semantic_failures = []
  samples = {}

  scanned_groups = 0
  presentation_nodes = 0
  build_errors = []

  for n in range(2, 16):
    for k in range(0, 8):
      group_label = (
        "pi_"
        + str(n + k)
        + "^"
        + str(n)
      )

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
        replay = (
          build_toda_group_result_proof_replay(
            group_result,
            max_depth=7,
          )
        )
        presentation = (
          build_toda_group_proof_presentation(
            replay
          )
        )
      except Exception as exc:
        build_errors.append(
          (
            group_label,
            type(exc).__name__,
            str(exc),
          )
        )
        continue

      scanned_groups += 1
      presentation_nodes += len(
        presentation.nodes
      )

      for node in presentation.nodes:
        step = node.proof_step
        statement = step.conclusion

        if (
          type(statement).__name__
          != TARGET_NAME
        ):
          continue

        occurrences += 1
        groups.add(group_label)

        statement_fields = tuple(
          field.name
          for field in fields(statement)
        )
        statement_field_signatures[
          statement_fields
        ] += 1

        rule_name = (
          step.inference_rule.name
          if step.inference_rule is not None
          else "<no rule>"
        )
        rule_counts[rule_name] += 1

        map_value = getattr(
          statement,
          "map",
          None,
        )
        map_type = type(
          map_value
        ).__name__
        map_type_counts[
          map_type
        ] += 1

        if map_value is None:
          semantic_failures.append(
            (
              group_label,
              rule_name,
              "statement.map is missing",
            )
          )
          continue

        map_signature = _value_signature(
          map_value
        )
        map_field_signatures[
          map_signature
        ] += 1

        source_group = getattr(
          map_value,
          "source_group",
          None,
        )
        target_group = getattr(
          map_value,
          "target_group",
          None,
        )

        source_type = type(
          source_group
        ).__name__
        target_type = type(
          target_group
        ).__name__

        source_group_type_counts[
          source_type
        ] += 1
        target_group_type_counts[
          target_type
        ] += 1

        shape = (
          statement_fields,
          map_signature,
          source_type,
          target_type,
        )
        rule_to_shape_counts[
          rule_name
        ][
          shape
        ] += 1

        if (
          source_group is None
          or target_group is None
        ):
          semantic_failures.append(
            (
              group_label,
              rule_name,
              "map lacks source_group or target_group",
            )
          )

        if rule_name not in samples:
          samples[rule_name] = repr(
            statement
          )

  print("=" * 78)
  print(
    "Phase 143-75O "
    "TodaProp44SuspensionInjectiveStatement "
    "semantic structure audit"
  )
  print("=" * 78)
  print(
    "scanned groups:",
    scanned_groups,
  )
  print(
    "scanned presentation nodes:",
    presentation_nodes,
  )
  print(
    "target occurrences:",
    occurrences,
  )
  print(
    "groups containing target:",
    len(groups),
  )
  print(
    "build errors:",
    len(build_errors),
  )
  print(
    "semantic failures:",
    len(semantic_failures),
  )

  print()
  print("Statement field signatures")
  print("-" * 78)
  for signature, count in (
    statement_field_signatures.most_common()
  ):
    print(
      str(count)
      + " x "
      + repr(signature)
    )

  print()
  print("Map types")
  print("-" * 78)
  for name, count in (
    map_type_counts.most_common()
  ):
    print(
      str(count)
      + " x "
      + name
    )

  print()
  print("Map field signatures")
  print("-" * 78)
  for signature, count in (
    map_field_signatures.most_common()
  ):
    print(
      str(count)
      + " x "
      + repr(signature)
    )

  print()
  print("Source group types")
  print("-" * 78)
  for name, count in (
    source_group_type_counts.most_common()
  ):
    print(
      str(count)
      + " x "
      + name
    )

  print()
  print("Target group types")
  print("-" * 78)
  for name, count in (
    target_group_type_counts.most_common()
  ):
    print(
      str(count)
      + " x "
      + name
    )

  print()
  print("Inference rules")
  print("-" * 78)
  for name, count in (
    rule_counts.most_common()
  ):
    print(
      str(count)
      + " x "
      + name
    )

  print()
  print("Rule -> semantic shape count")
  print("-" * 78)
  for rule_name in sorted(
    rule_to_shape_counts
  ):
    shapes = rule_to_shape_counts[
      rule_name
    ]
    print(rule_name)
    print(
      "  distinct semantic shapes:",
      len(shapes),
    )
    for shape, count in (
      shapes.most_common()
    ):
      print(
        "  "
        + str(count)
        + " x "
        + repr(shape)
      )

  print()
  print("Representative statements")
  print("-" * 78)
  for rule_name in sorted(samples):
    print(rule_name)
    print(
      "  "
      + samples[rule_name]
    )

  if semantic_failures:
    print()
    print("Semantic failures")
    print("-" * 78)
    for failure in semantic_failures:
      print(
        "  - "
        + repr(failure)
      )

  if build_errors:
    print()
    print("Build errors")
    print("-" * 78)
    for error in build_errors:
      print(
        "  - "
        + repr(error)
      )

  print()
  print("=" * 78)

  if (
    occurrences == EXPECTED_OCCURRENCES
    and not build_errors
    and not semantic_failures
    and statement_field_signatures
    == Counter(
      {
        ("map",): 55,
      }
    )
    and map_type_counts
    == Counter(
      {
        "TodaSuspensionMap": 55,
      }
    )
    and len(
      map_field_signatures
    ) == 1
    and len(
      rule_counts
    ) == 2
  ):
    print(
      "PASS: all 55 occurrences carry the same "
      "map-based semantic structure; "
      "rule-name parsing is unnecessary."
    )
  else:
    print(
      "MEASURED RESULT: inspect the inventory above "
      "before designing Phase 143-75P."
    )


if __name__ == "__main__":
  main()
