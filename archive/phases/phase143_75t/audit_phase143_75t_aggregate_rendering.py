from collections import Counter

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
  render_toda_proof_statement_latex,
)


TARGET_NAME = "Toda58EquationStatement"


def main():
  scanned_groups = 0
  scanned_nodes = 0
  target_occurrences = 0
  semantic_renderings = 0
  target_rule_name_fallback = 0
  all_rule_name_fallback = 0
  fallback_statement_types = Counter()
  output_counts = Counter()
  errors = []

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

        try:
          fact = (
            _render_group_proof_narrative_fact(
              step
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

        rule_name = (
          step.inference_rule.name
          if step.inference_rule is not None
          else None
        )

        if (
          rule_name is not None
          and fact == rule_name
        ):
          all_rule_name_fallback += 1
          fallback_statement_types[
            type(statement).__name__
          ] += 1

        if (
          type(statement).__name__
          != TARGET_NAME
        ):
          continue

        target_occurrences += 1

        rendered = (
          render_toda_proof_statement_latex(
            statement
          )
        )

        if rendered is not None:
          semantic_renderings += 1
          output_counts[
            rendered
          ] += 1

        if (
          rule_name is not None
          and fact == rule_name
        ):
          target_rule_name_fallback += 1

  print("=" * 78)
  print(
    "Phase 143-75T aggregate semantic "
    "rendering audit"
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
    "target semantic renderings:",
    semantic_renderings,
  )
  print(
    "target rule-name fallback:",
    target_rule_name_fallback,
  )
  print(
    "all rule-name fallback:",
    all_rule_name_fallback,
  )
  print(
    "remaining fallback statement types:",
    len(fallback_statement_types),
  )
  print(
    "errors:",
    len(errors),
  )

  print()
  print("Target rendered outputs")
  print("-" * 78)
  for value, count in (
    output_counts.most_common()
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
    and target_occurrences == 45
    and semantic_renderings == 45
    and target_rule_name_fallback == 0
    and all_rule_name_fallback == 365
    and len(
      fallback_statement_types
    ) == 31
    and not errors
  ):
    print(
      "PASS: Phase 143-75T removed all 45 "
      "Toda58EquationStatement fallbacks; "
      "365 remain across 31 statement types."
    )
  else:
    print(
      "MEASURED RESULT: inspect the values "
      "above before continuing."
    )


if __name__ == "__main__":
  main()
