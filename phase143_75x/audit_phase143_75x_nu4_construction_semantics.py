from collections import Counter, defaultdict
from dataclasses import fields, is_dataclass

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_fact,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_narrative_renderer import (
  render_toda_expression_latex,
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaLemma54Nu4ConstructionStatement,
)


def _field_signature(value):
  if not is_dataclass(value):
    return ()

  return tuple(
    field.name
    for field in fields(value)
  )


def _safe_expression_latex(value):
  try:
    return render_toda_expression_latex(
      value
    )
  except Exception:
    return (
      "<unrendered:"
      + type(value).__name__
      + ">"
    )


def main():
  scanned_groups = 0
  scanned_nodes = 0
  target_occurrences = 0
  target_fallbacks = 0
  semantic_renderings = 0
  errors = []

  statement_signatures = Counter()
  field_types = defaultdict(Counter)
  branch_signatures = {
    "positive_branch": Counter(),
    "negative_branch": Counter(),
  }
  branch_value_tuples = {
    "positive_branch": Counter(),
    "negative_branch": Counter(),
  }
  rule_counts = Counter()
  rule_groups = defaultdict(set)
  rendered_fields = defaultdict(Counter)
  statement_renderer_results = Counter()
  sample_by_rule = {}

  target_fields = (
    "alpha_star",
    "nu4",
    "parameter",
    "whitehead_data",
    "double_suspension_value",
    "positive_branch",
    "negative_branch",
  )

  for n in range(2, 16):
    for k in range(0, 8):
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
        errors.append(
          (
            n,
            k,
            type(exc).__name__,
            str(exc),
          )
        )
        continue

      scanned_groups += 1
      scanned_nodes += len(
        presentation.nodes
      )

      for node in presentation.nodes:
        step = node.proof_step
        statement = step.conclusion

        if not isinstance(
          statement,
          TodaLemma54Nu4ConstructionStatement,
        ):
          continue

        target_occurrences += 1

        signature = _field_signature(
          statement
        )
        statement_signatures[
          signature
        ] += 1

        rule_name = (
          step.inference_rule.name
          if step.inference_rule is not None
          else "<no inference rule>"
        )
        rule_counts[
          rule_name
        ] += 1
        rule_groups[
          rule_name
        ].add(
          (
            n,
            k,
          )
        )

        for field_name in target_fields:
          value = getattr(
            statement,
            field_name,
          )
          field_types[
            field_name
          ][
            type(value).__name__
          ] += 1

          if field_name in (
            "alpha_star",
            "nu4",
            "parameter",
            "double_suspension_value",
          ):
            rendered_fields[
              field_name
            ][
              _safe_expression_latex(
                value
              )
            ] += 1

        for branch_name in (
          "positive_branch",
          "negative_branch",
        ):
          branch = getattr(
            statement,
            branch_name,
          )
          branch_signature = (
            _field_signature(
              branch
            )
          )
          branch_signatures[
            branch_name
          ][
            branch_signature
          ] += 1

          if branch_signature:
            branch_value_tuples[
              branch_name
            ][
              tuple(
                getattr(
                  branch,
                  name,
                )
                for name in branch_signature
              )
            ] += 1

        try:
          semantic = (
            render_toda_proof_statement_latex(
              statement
            )
          )
          statement_renderer_results[
            (
              "<None>"
              if semantic is None
              else semantic
            )
          ] += 1
          if semantic is not None:
            semantic_renderings += 1

          fact = (
            _render_group_proof_narrative_fact(
              step
            )
          )
          if (
            step.inference_rule is not None
            and fact
            == step.inference_rule.name
          ):
            target_fallbacks += 1
        except Exception as exc:
          errors.append(
            (
              n,
              k,
              type(exc).__name__,
              str(exc),
            )
          )

        if rule_name not in sample_by_rule:
          sample_by_rule[
            rule_name
          ] = statement

  print("=" * 78)
  print(
    "Phase 143-75X "
    "TodaLemma54Nu4ConstructionStatement "
    "semantic structure audit"
  )
  print("=" * 78)
  print(
    "scanned groups:",
    scanned_groups,
  )
  print(
    "scanned presentation nodes:",
    scanned_nodes,
  )
  print(
    "target occurrences:",
    target_occurrences,
  )
  print(
    "target rule-name fallbacks:",
    target_fallbacks,
  )
  print(
    "existing statement semantic renderings:",
    semantic_renderings,
  )
  print(
    "errors:",
    len(errors),
  )

  print()
  print("Statement field signatures")
  print("-" * 78)
  for signature, count in (
    statement_signatures.most_common()
  ):
    print(
      str(count)
      + " x "
      + repr(signature)
    )

  print()
  print("Field type inventory")
  print("-" * 78)
  for field_name in target_fields:
    print(
      field_name
      + ": "
      + repr(
        dict(
          field_types[
            field_name
          ]
        )
      )
    )

  print()
  print("Branch field signatures")
  print("-" * 78)
  for branch_name in (
    "positive_branch",
    "negative_branch",
  ):
    print(
      branch_name
    )
    for signature, count in (
      branch_signatures[
        branch_name
      ].most_common()
    ):
      print(
        "  "
        + str(count)
        + " x "
        + repr(signature)
      )

  print()
  print("Branch value tuples")
  print("-" * 78)
  for branch_name in (
    "positive_branch",
    "negative_branch",
  ):
    print(
      branch_name
    )
    for values, count in (
      branch_value_tuples[
        branch_name
      ].most_common()
    ):
      print(
        "  "
        + str(count)
        + " x "
        + repr(values)
      )

  print()
  print("Rendered first-class expression fields")
  print("-" * 78)
  for field_name in (
    "alpha_star",
    "nu4",
    "parameter",
    "double_suspension_value",
  ):
    print(
      field_name
    )
    for value, count in (
      rendered_fields[
        field_name
      ].most_common()
    ):
      print(
        "  "
        + str(count)
        + " x "
        + value
      )

  print()
  print("Per-rule occurrence structure")
  print("-" * 78)
  for rule_name, count in (
    rule_counts.most_common()
  ):
    print(
      str(count)
      + " x "
      + rule_name
    )
    print(
      "  groups: "
      + str(
        len(
          rule_groups[
            rule_name
          ]
        )
      )
    )

    sample = sample_by_rule[
      rule_name
    ]
    print(
      "  alpha_star: "
      + _safe_expression_latex(
        sample.alpha_star
      )
    )
    print(
      "  nu4: "
      + _safe_expression_latex(
        sample.nu4
      )
    )
    print(
      "  parameter: "
      + _safe_expression_latex(
        sample.parameter
      )
    )
    print(
      "  double_suspension_value: "
      + _safe_expression_latex(
        sample.double_suspension_value
      )
    )
    print(
      "  whitehead_data type: "
      + type(
        sample.whitehead_data
      ).__name__
    )

  print()
  print("Current statement-renderer results")
  print("-" * 78)
  for value, count in (
    statement_renderer_results.most_common()
  ):
    print(
      str(count)
      + " x "
      + value
    )

  print()
  print("=" * 78)

  expected_signature = (
    "alpha_star",
    "nu4",
    "parameter",
    "whitehead_data",
    "double_suspension_value",
    "positive_branch",
    "negative_branch",
  )

  if (
    scanned_groups == 112
    and scanned_nodes == 11033
    and target_occurrences == 37
    and target_fallbacks == 37
    and semantic_renderings == 0
    and statement_signatures[
      expected_signature
    ] == 37
    and len(
      statement_signatures
    ) == 1
    and len(
      rule_counts
    ) == 1
    and not errors
  ):
    print(
      "PASS: all 37 target statements "
      "share one seven-field piecewise "
      "nu_4 construction structure."
    )
  else:
    print(
      "MEASURED RESULT: inspect the aggregate "
      "and branch structure before implementation."
    )


if __name__ == "__main__":
  main()
