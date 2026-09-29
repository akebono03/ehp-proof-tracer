from collections import Counter, defaultdict
from dataclasses import fields, is_dataclass

import homotopy_groups
import toda_rules
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGET_NAMES = (
  "TodaProp53FiniteDimensionalStatement",
  "TodaProp58FiniteDimensionalStatement",
  "TodaProp59FiniteDimensionalStatement",
  "TodaProp511NuSquaredFiniteDimensionalStatement",
  "FiniteHomotopyGroupStatement",
)

EXPECTED_COUNTS = {
  "TodaProp53FiniteDimensionalStatement": 76,
  "TodaProp58FiniteDimensionalStatement": 25,
  "TodaProp59FiniteDimensionalStatement": 20,
  "TodaProp511NuSquaredFiniteDimensionalStatement": 14,
  "FiniteHomotopyGroupStatement": 3,
}


def _target_types():
  result = {}
  for name in TARGET_NAMES:
    owner = (
      homotopy_groups
      if name == "FiniteHomotopyGroupStatement"
      else toda_rules
    )
    result[name] = getattr(owner, name)
  return result


def _shape(value, depth=0):
  type_name = type(value).__name__

  if depth >= 2:
    return type_name

  if is_dataclass(value):
    parts = []
    for field in fields(value):
      field_value = getattr(
        value,
        field.name,
      )
      parts.append(
        field.name
        + ": "
        + _shape(
          field_value,
          depth + 1,
        )
      )
    return (
      type_name
      + "("
      + ", ".join(parts)
      + ")"
    )

  if isinstance(value, tuple):
    return (
      "tuple["
      + ", ".join(
        _shape(
          item,
          depth + 1,
        )
        for item in value
      )
      + "]"
    )

  return type_name


def _field_signature(statement):
  return tuple(
    (
      field.name,
      type(
        getattr(
          statement,
          field.name,
        )
      ).__name__,
    )
    for field in fields(statement)
  )


def _safe_rule_name(proof_step):
  rule = getattr(
    proof_step,
    "inference_rule",
    None,
  )
  return getattr(
    rule,
    "name",
    "<no rule name>",
  )


def main():
  target_types = _target_types()
  occurrences = Counter()
  groups = defaultdict(set)
  signatures = defaultdict(Counter)
  shapes = defaultdict(Counter)
  rule_names = defaultdict(Counter)
  samples = {}
  errors = []
  scanned_groups = 0
  scanned_nodes = 0

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
        scanned_groups += 1

        for node_index, node in enumerate(
          presentation.nodes
        ):
          scanned_nodes += 1
          proof_step = node.proof_step
          statement = proof_step.conclusion
          statement_name = (
            type(statement).__name__
          )
          if (
            statement_name
            not in target_types
          ):
            continue
          if not isinstance(
            statement,
            target_types[
              statement_name
            ],
          ):
            continue

          occurrences[
            statement_name
          ] += 1
          groups[
            statement_name
          ].add(group_label)
          signatures[
            statement_name
          ][
            _field_signature(
              statement
            )
          ] += 1
          shapes[
            statement_name
          ][
            _shape(statement)
          ] += 1
          rule_names[
            statement_name
          ][
            _safe_rule_name(
              proof_step
            )
          ] += 1

          samples.setdefault(
            statement_name,
            (
              group_label,
              node_index,
              repr(statement),
            ),
          )
      except Exception as exc:
        errors.append(
          (
            group_label,
            type(exc).__name__,
            str(exc),
          )
        )

  print("=" * 78)
  print(
    "Phase 143-75K finite-dimensional / "
    "group-result semantic-structure audit"
  )
  print(
    "range: n=2..15, k=0..7, depth=7"
  )
  print(
    "scanned groups:",
    scanned_groups,
  )
  print(
    "scanned presentation nodes:",
    scanned_nodes,
  )
  print("=" * 78)

  for name in TARGET_NAMES:
    print()
    print(name)
    print(
      "  occurrences:",
      occurrences[name],
    )
    print(
      "  groups:",
      len(groups[name]),
    )

    print("  field signatures:")
    for signature, count in (
      signatures[name].most_common()
    ):
      print(
        "   -",
        count,
        "x",
        signature,
      )

    print("  semantic shapes:")
    for shape, count in (
      shapes[name].most_common()
    ):
      print(
        "   -",
        count,
        "x",
        shape,
      )

    print("  rule names:")
    for rule_name, count in (
      rule_names[name].most_common()
    ):
      print(
        "   -",
        count,
        "x",
        rule_name,
      )

    if name in samples:
      group_label, node_index, sample = (
        samples[name]
      )
      print(
        "  sample group:",
        group_label,
      )
      print(
        "  sample node:",
        node_index,
      )
      print(
        "  sample statement:",
        sample,
      )

  print()
  print("errors:", len(errors))
  for error in errors[:20]:
    print("  -", error)

  count_mismatches = []
  for name, expected in (
    EXPECTED_COUNTS.items()
  ):
    actual = occurrences[name]
    if actual != expected:
      count_mismatches.append(
        (
          name,
          expected,
          actual,
        )
      )

  print()
  if (
    scanned_groups == 112
    and not errors
    and not count_mismatches
  ):
    print(
      "PASS: all five target statement "
      "types were audited with the "
      "expected Phase 143-75J counts."
    )
  else:
    print("AUDIT CHECK:")
    if scanned_groups != 112:
      print(
        "  scanned groups expected 112, got",
        scanned_groups,
      )
    for (
      name,
      expected,
      actual,
    ) in count_mismatches:
      print(
        "  count mismatch:",
        name,
        "expected",
        expected,
        "got",
        actual,
      )
    if errors:
      print(
        "  render/build errors were found."
      )


if __name__ == "__main__":
  main()
