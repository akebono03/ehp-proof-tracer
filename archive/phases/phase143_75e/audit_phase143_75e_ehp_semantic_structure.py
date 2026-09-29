from collections import defaultdict
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
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaKernelFreeCyclicStatement,
  TodaDeltaSurjectiveStatement,
  TodaSuspensionKernelFreeCyclicStatement,
)


TARGET_TYPES = (
  TodaDeltaSurjectiveStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaKernelFreeCyclicStatement,
)


def _value_shape(value):
  if is_dataclass(value):
    names = ", ".join(
      field.name
      for field in fields(value)
    )
    return (
      type(value).__name__
      + "("
      + names
      + ")"
    )

  if isinstance(
    value,
    tuple,
  ):
    return (
      "tuple["
      + ", ".join(
        type(item).__name__
        for item in value
      )
      + "]"
    )

  return type(value).__name__


def main():
  occurrences = defaultdict(int)
  groups = defaultdict(set)
  shapes = defaultdict(
    lambda: defaultdict(int)
  )
  samples = defaultdict(list)
  rule_names = defaultdict(set)
  errors = []

  scanned_groups = 0
  scanned_nodes = 0

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

      scanned_nodes += len(
        presentation.nodes
      )

      for node in presentation.nodes:
        proof_step = node.proof_step
        statement = proof_step.conclusion

        if not isinstance(
          statement,
          TARGET_TYPES,
        ):
          continue

        name = type(
          statement
        ).__name__

        occurrences[name] += 1
        groups[name].add(
          f"pi_{n + k}^{n}"
        )

        field_shape = tuple(
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

        shapes[name][
          field_shape
        ] += 1

        if (
          proof_step.inference_rule
          is not None
        ):
          rule_names[name].add(
            proof_step.inference_rule.name
          )

        if len(
          samples[name]
        ) < 4:
          samples[name].append(
            (
              f"pi_{n + k}^{n}",
              repr(
                statement
              ),
            )
          )

  print("=" * 78)
  print(
    "Phase 143-75E EHP map/image/kernel "
    "semantic-structure audit"
  )
  print(
    "range: n=2..15, k=0..7, depth=7"
  )
  print(
    f"scanned groups: {scanned_groups}"
  )
  print(
    "scanned presentation nodes: "
    f"{scanned_nodes}"
  )
  print("=" * 78)

  for target_type in TARGET_TYPES:
    name = target_type.__name__
    print()
    print(name)
    print(
      f"  occurrences: {occurrences[name]}"
    )
    print(
      f"  groups: {len(groups[name])}"
    )

    for (
      field_shape,
      count,
    ) in sorted(
      shapes[name].items(),
      key=lambda item: (
        -item[1],
        repr(
          item[0]
        ),
      ),
    ):
      print(
        f"  shape ({count} occurrences):"
      )
      for (
        field_name,
        value_shape,
      ) in field_shape:
        print(
          f"    {field_name}: "
          f"{value_shape}"
        )

    print(
      "  rule names:"
    )
    for rule_name in sorted(
      rule_names[name]
    ):
      print(
        f"    - {rule_name}"
      )

    print(
      "  samples:"
    )
    for (
      group,
      statement_repr,
    ) in samples[name]:
      print(
        f"    - {group}"
      )
      print(
        f"      {statement_repr}"
      )

  print()
  print(
    f"errors: {len(errors)}"
  )
  for error in errors[:20]:
    print(
      "  -",
      error,
    )

  print()
  print("=" * 78)
  if not errors:
    print(
      "PASS: semantic field shapes for the "
      "EHP map/image/kernel statement family "
      "were collected."
    )
  else:
    print(
      "FAIL: audit encountered render/replay "
      "errors."
    )


if __name__ == "__main__":
  main()
