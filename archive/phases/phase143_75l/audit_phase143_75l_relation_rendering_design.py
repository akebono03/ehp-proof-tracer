from collections import Counter, defaultdict
from dataclasses import fields

import toda_rules
import toda_group_proof_narrative_renderer as group_renderer
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
  render_toda_raw_group_structure_latex,
)


TARGET_NAMES = (
  "TodaProp53FiniteDimensionalStatement",
  "TodaProp58FiniteDimensionalStatement",
  "TodaProp59FiniteDimensionalStatement",
  "TodaProp511NuSquaredFiniteDimensionalStatement",
)

EXPECTED_COUNTS = {
  "TodaProp53FiniteDimensionalStatement": 76,
  "TodaProp58FiniteDimensionalStatement": 25,
  "TodaProp59FiniteDimensionalStatement": 20,
  "TodaProp511NuSquaredFiniteDimensionalStatement": 14,
}


def _target_types():
  return {
    name: getattr(toda_rules, name)
    for name in TARGET_NAMES
  }


def _relation_operator(relation):
  relation_type = getattr(
    relation,
    "relation_type",
    None,
  )
  value = getattr(
    relation_type,
    "value",
    str(relation_type),
  )
  if value == "equality":
    return "="
  if value == "membership":
    return r"\in"
  return "<UNSUPPORTED:" + str(value) + ">"


def _render_relation_candidate(relation):
  return (
    render_toda_primary_group_latex(
      relation.lhs
    )
    + " "
    + _relation_operator(relation)
    + " "
    + render_toda_raw_group_structure_latex(
      relation.rhs
    )
  )


def _render_zero_candidate(statement):
  group = getattr(
    statement,
    "group",
    None,
  )
  if group is None:
    return None
  return (
    render_toda_primary_group_latex(group)
    + " = 0"
  )


def _render_range_candidate(statement):
  render_scalar = getattr(
    group_renderer,
    "_render_scalar_latex",
    None,
  )
  if render_scalar is None:
    return None
  return (
    render_scalar(statement.left)
    + r" \ge "
    + render_scalar(statement.right)
  )


def _semantic_fields(statement):
  relation_fields = []
  zero_fields = []
  range_fields = []
  ignored_fields = []
  for field in fields(statement):
    value = getattr(
      statement,
      field.name,
    )
    type_name = type(value).__name__
    if type_name == "Relation":
      relation_fields.append(
        (field.name, value)
      )
    elif (
      type_name
      == "TodaPrimaryGroupZeroStatement"
    ):
      zero_fields.append(
        (field.name, value)
      )
    elif (
      type_name
      == "ScalarGreaterEqualStatement"
    ):
      range_fields.append(
        (field.name, value)
      )
    elif field.name == "literature_statements":
      ignored_fields.append(
        (
          field.name,
          "metadata",
        )
      )
    else:
      ignored_fields.append(
        (
          field.name,
          type_name,
        )
      )
  return (
    relation_fields,
    zero_fields,
    range_fields,
    ignored_fields,
  )


def main():
  target_types = _target_types()
  occurrences = Counter()
  relation_field_sets = defaultdict(Counter)
  zero_field_sets = defaultdict(Counter)
  range_field_sets = defaultdict(Counter)
  ignored_field_sets = defaultdict(Counter)
  candidate_outputs = defaultdict(dict)
  unsupported_relation_types = Counter()
  render_failures = []
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
          statement = (
            node.proof_step.conclusion
          )
          name = type(statement).__name__
          if name not in target_types:
            continue
          if not isinstance(
            statement,
            target_types[name],
          ):
            continue

          occurrences[name] += 1
          (
            relation_fields,
            zero_fields,
            range_fields,
            ignored_fields,
          ) = _semantic_fields(statement)

          relation_field_sets[name][
            tuple(
              field_name
              for field_name, _value
              in relation_fields
            )
          ] += 1
          zero_field_sets[name][
            tuple(
              field_name
              for field_name, _value
              in zero_fields
            )
          ] += 1
          range_field_sets[name][
            tuple(
              field_name
              for field_name, _value
              in range_fields
            )
          ] += 1
          ignored_field_sets[name][
            tuple(ignored_fields)
          ] += 1

          if name not in candidate_outputs:
            continue

          if not candidate_outputs[name]:
            try:
              rendered_relations = []
              for (
                field_name,
                relation,
              ) in relation_fields:
                operator = _relation_operator(
                  relation
                )
                if operator.startswith(
                  "<UNSUPPORTED:"
                ):
                  unsupported_relation_types[
                    operator
                  ] += 1
                rendered_relations.append(
                  (
                    field_name,
                    _render_relation_candidate(
                      relation
                    ),
                  )
                )

              rendered_zeros = [
                (
                  field_name,
                  _render_zero_candidate(
                    value
                  ),
                )
                for field_name, value
                in zero_fields
              ]
              rendered_ranges = [
                (
                  field_name,
                  _render_range_candidate(
                    value
                  ),
                )
                for field_name, value
                in range_fields
              ]

              candidate_outputs[name] = {
                "group": group_label,
                "node": node_index,
                "relations": rendered_relations,
                "zeros": rendered_zeros,
                "ranges": rendered_ranges,
                "ignored": ignored_fields,
              }
            except Exception as exc:
              render_failures.append(
                (
                  name,
                  group_label,
                  node_index,
                  type(exc).__name__,
                  str(exc),
                )
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
    "Phase 143-75L finite-dimensional "
    "relation-rendering design audit"
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
    print("  relation field sets:")
    for value, count in (
      relation_field_sets[name].most_common()
    ):
      print(
        "   -",
        count,
        "x",
        value,
      )
    print("  zero field sets:")
    for value, count in (
      zero_field_sets[name].most_common()
    ):
      print(
        "   -",
        count,
        "x",
        value,
      )
    print("  range field sets:")
    for value, count in (
      range_field_sets[name].most_common()
    ):
      print(
        "   -",
        count,
        "x",
        value,
      )
    print("  non-semantic/metadata fields:")
    for value, count in (
      ignored_field_sets[name].most_common()
    ):
      print(
        "   -",
        count,
        "x",
        value,
      )

    sample = candidate_outputs.get(
      name,
      {},
    )
    if sample:
      print(
        "  sample group:",
        sample["group"],
      )
      print(
        "  sample node:",
        sample["node"],
      )
      print("  candidate relation rendering:")
      for field_name, latex in (
        sample["relations"]
      ):
        print(
          "   -",
          field_name + ":",
          latex,
        )
      print("  candidate zero rendering:")
      for field_name, latex in (
        sample["zeros"]
      ):
        print(
          "   -",
          field_name + ":",
          latex,
        )
      print("  candidate range rendering:")
      for field_name, latex in (
        sample["ranges"]
      ):
        print(
          "   -",
          field_name + ":",
          latex,
        )

  print()
  print(
    "unsupported relation types:",
    sum(
      unsupported_relation_types.values()
    ),
  )
  for key, count in (
    unsupported_relation_types.most_common()
  ):
    print(
      "  -",
      count,
      "x",
      key,
    )

  print(
    "candidate render failures:",
    len(render_failures),
  )
  for failure in render_failures[:20]:
    print(
      "  -",
      failure,
    )

  print(
    "build errors:",
    len(errors),
  )
  for error in errors[:20]:
    print(
      "  -",
      error,
    )

  mismatches = []
  for name, expected in (
    EXPECTED_COUNTS.items()
  ):
    actual = occurrences[name]
    if actual != expected:
      mismatches.append(
        (
          name,
          expected,
          actual,
        )
      )

  print()
  if (
    scanned_groups == 112
    and not unsupported_relation_types
    and not render_failures
    and not errors
    and not mismatches
  ):
    print(
      "PASS: all four finite-dimensional "
      "statement types can be decomposed "
      "into existing semantic rendering "
      "components for relation/group/zero/"
      "range fields."
    )
    print(
      "DESIGN: keep the four statement "
      "types distinct, but use one generic "
      "field-composition helper rather than "
      "rule-name parsing or proposition-"
      "specific prose."
    )
  else:
    print("AUDIT CHECK:")
    for mismatch in mismatches:
      print(
        "  count mismatch:",
        mismatch,
      )
    if unsupported_relation_types:
      print(
        "  unsupported relation type found."
      )
    if render_failures:
      print(
        "  candidate rendering failed."
      )
    if errors:
      print(
        "  build errors were found."
      )


if __name__ == "__main__":
  main()
