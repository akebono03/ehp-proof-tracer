from collections import (
  Counter,
  defaultdict,
)
from dataclasses import (
  fields,
  is_dataclass,
)

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
  Toda58WhiteheadSquareUpToSignStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  TodaProp27HopfInvariantUpToSignStatement,
)


TARGET_TYPES = (
  TodaPi32WhiteheadSquareUpToSignStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  Toda58WhiteheadSquareUpToSignStatement,
)


def _shape(value):
  if is_dataclass(value):
    names = ", ".join(
      field.name
      for field in fields(value)
    )
    return (
      f"{type(value).__name__}"
      f"({names})"
    )

  if isinstance(
    value,
    tuple,
  ):
    return (
      "tuple("
      + ", ".join(
        _shape(item)
        for item in value
      )
      + ")"
    )

  if isinstance(
    value,
    list,
  ):
    return (
      "list("
      + ", ".join(
        _shape(item)
        for item in value
      )
      + ")"
    )

  return type(
    value
  ).__name__


def _statement_shape(statement):
  if not is_dataclass(
    statement
  ):
    return (
      type(statement).__name__
    )

  return tuple(
    (
      field.name,
      _shape(
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


def main():
  occurrences = Counter()
  groups = defaultdict(
    set
  )
  shapes = defaultdict(
    Counter
  )
  rule_names = defaultdict(
    Counter
  )
  samples = defaultdict(
    list
  )
  errors = []
  scanned_nodes = 0

  for k in range(8):
    for n in range(2, 16):
      group_name = (
        f"pi_{n + k}^{n}"
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
          group_name
        )
        shapes[name][
          _statement_shape(
            statement
          )
        ] += 1

        if (
          proof_step.inference_rule
          is not None
        ):
          rule_names[name][
            proof_step.inference_rule.name
          ] += 1

        if len(
          samples[name]
        ) < 6:
          samples[name].append(
            (
              group_name,
              repr(
                statement
              ),
            )
          )

  print("=" * 78)
  print(
    "Phase 143-75H Whitehead-square / "
    "Hopf-invariant semantic-structure audit"
  )
  print(
    "range: n=2..15, k=0..7, depth=7"
  )
  print(
    "scanned groups: 112"
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
      f"  occurrences: "
      f"{occurrences[name]}"
    )
    print(
      f"  groups: "
      f"{len(groups[name])}"
    )

    for shape, count in (
      shapes[name]
      .most_common()
    ):
      print(
        f"  shape "
        f"({count} occurrences):"
      )
      for (
        field_name,
        field_shape,
      ) in shape:
        print(
          f"    {field_name}: "
          f"{field_shape}"
        )

    print(
      "  rule names:"
    )
    for (
      rule_name,
      count,
    ) in (
      rule_names[name]
      .most_common()
    ):
      print(
        f"    - {count} x "
        f"{rule_name}"
      )

    print(
      "  samples:"
    )
    for (
      group_name,
      statement_repr,
    ) in samples[name]:
      print(
        f"    - {group_name}"
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

  expected = {
    "TodaPi32WhiteheadSquareUpToSignStatement": 60,
    "TodaProp27HopfInvariantUpToSignStatement": 53,
    "Toda58WhiteheadSquareUpToSignStatement": 33,
  }

  if (
    not errors
    and all(
      occurrences[name]
      == count
      for name, count
      in expected.items()
    )
  ):
    print(
      "PASS: semantic field shapes for the "
      "Whitehead-square / Hopf-invariant "
      "statement family were collected."
    )
  else:
    print(
      "CHECK: occurrence counts differ from "
      "the Phase 143-75G inventory or "
      "render errors occurred."
    )


if __name__ == "__main__":
  main()
