from collections import Counter, defaultdict
from dataclasses import fields

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
  Toda54BracketUpToSignStatement,
)


def main():
  scanned_groups = 0
  scanned_nodes = 0
  target_occurrences = 0
  target_fallbacks = 0
  semantic_renderings = 0
  errors = []

  field_signatures = Counter()
  bracket_types = Counter()
  positive_value_types = Counter()
  rule_counts = Counter()
  rule_field_signatures = defaultdict(Counter)
  rule_bracket_types = defaultdict(Counter)
  rule_positive_types = defaultdict(Counter)
  rule_groups = defaultdict(set)
  rendered_brackets = Counter()
  rendered_positive_values = Counter()
  statement_renderer_results = Counter()
  sample_by_rule = {}

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
          Toda54BracketUpToSignStatement,
        ):
          continue

        target_occurrences += 1

        signature = tuple(
          field.name
          for field in fields(
            statement
          )
        )
        field_signatures[
          signature
        ] += 1

        bracket_type = type(
          statement.bracket
        ).__name__
        positive_type = type(
          statement.positive_value
        ).__name__

        bracket_types[
          bracket_type
        ] += 1
        positive_value_types[
          positive_type
        ] += 1

        rule_name = (
          step.inference_rule.name
          if step.inference_rule is not None
          else "<no inference rule>"
        )
        rule_counts[
          rule_name
        ] += 1
        rule_field_signatures[
          rule_name
        ][
          signature
        ] += 1
        rule_bracket_types[
          rule_name
        ][
          bracket_type
        ] += 1
        rule_positive_types[
          rule_name
        ][
          positive_type
        ] += 1
        rule_groups[
          rule_name
        ].add(
          (
            n,
            k,
          )
        )

        try:
          bracket_latex = (
            render_toda_expression_latex(
              statement.bracket
            )
          )
          positive_latex = (
            render_toda_expression_latex(
              statement.positive_value
            )
          )
          rendered_brackets[
            bracket_latex
          ] += 1
          rendered_positive_values[
            positive_latex
          ] += 1

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
          if semantic is not None:
            semantic_renderings += 1

          if rule_name not in sample_by_rule:
            sample_by_rule[
              rule_name
            ] = (
              bracket_latex,
              positive_latex,
              semantic,
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

  print("=" * 78)
  print(
    "Phase 143-75V "
    "Toda54BracketUpToSignStatement "
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
  print("Field signatures")
  print("-" * 78)
  for signature, count in (
    field_signatures.most_common()
  ):
    print(
      str(count)
      + " x "
      + repr(signature)
    )

  print()
  print("Bracket expression types")
  print("-" * 78)
  for name, count in (
    bracket_types.most_common()
  ):
    print(
      str(count)
      + " x "
      + name
    )

  print()
  print("Positive-value expression types")
  print("-" * 78)
  for name, count in (
    positive_value_types.most_common()
  ):
    print(
      str(count)
      + " x "
      + name
    )

  print()
  print("Per-rule semantic structure")
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
      "  fields: "
      + repr(
        dict(
          rule_field_signatures[
            rule_name
          ]
        )
      )
    )
    print(
      "  bracket types: "
      + repr(
        dict(
          rule_bracket_types[
            rule_name
          ]
        )
      )
    )
    print(
      "  positive types: "
      + repr(
        dict(
          rule_positive_types[
            rule_name
          ]
        )
      )
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
      "  sample bracket: "
      + sample[
        0
      ]
    )
    print(
      "  sample positive value: "
      + sample[
        1
      ]
    )
    print(
      "  current statement renderer: "
      + (
        "<None>"
        if sample[
          2
        ] is None
        else sample[
          2
        ]
      )
    )

  print()
  print("Distinct rendered bracket expressions")
  print("-" * 78)
  for value, count in (
    rendered_brackets.most_common()
  ):
    print(
      str(count)
      + " x "
      + value
    )

  print()
  print("Distinct rendered positive values")
  print("-" * 78)
  for value, count in (
    rendered_positive_values.most_common()
  ):
    print(
      str(count)
      + " x "
      + value
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

  if (
    scanned_groups == 112
    and scanned_nodes == 11033
    and target_occurrences == 40
    and target_fallbacks == 40
    and len(field_signatures) == 1
    and next(
      iter(
        field_signatures
      ),
      (),
    )
    == (
      "bracket",
      "positive_value",
    )
    and len(bracket_types) == 1
    and not errors
  ):
    print(
      "PASS: all 40 target statements "
      "share the same bracket/positive_value "
      "semantic field structure."
    )
  else:
    print(
      "MEASURED RESULT: inspect the structure "
      "before implementing Phase 143-75W."
    )


if __name__ == "__main__":
  main()
