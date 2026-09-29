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
from toda_rules import (
  Toda54BracketUpToSignStatement,
)


def main():
  scanned_groups = 0
  scanned_nodes = 0
  target_occurrences = 0
  target_semantic_renderings = 0
  target_rule_name_fallbacks = 0
  all_rule_name_fallbacks = 0
  fallback_statement_types = Counter()
  outputs = Counter()
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
          all_rule_name_fallbacks += 1
          fallback_statement_types[
            type(statement).__name__
          ] += 1

        if not isinstance(
          statement,
          Toda54BracketUpToSignStatement,
        ):
          continue

        target_occurrences += 1

        rendered = (
          render_toda_proof_statement_latex(
            statement
          )
        )

        if rendered is not None:
          target_semantic_renderings += 1
          outputs[
            rendered
          ] += 1

        if (
          rule_name is not None
          and fact == rule_name
        ):
          target_rule_name_fallbacks += 1

  print("=" * 78)
  print(
    "Phase 143-75W "
    "Toda54BracketUpToSignStatement "
    "semantic rendering audit"
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
    target_semantic_renderings,
  )
  print(
    "target rule-name fallbacks:",
    target_rule_name_fallbacks,
  )
  print(
    "all rule-name fallbacks:",
    all_rule_name_fallbacks,
  )
  print(
    "remaining fallback statement types:",
    len(
      fallback_statement_types
    ),
  )
  print(
    "errors:",
    len(errors),
  )

  print()
  print("Rendered target outputs")
  print("-" * 78)
  for value, count in (
    outputs.most_common()
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
    and target_semantic_renderings == 40
    and target_rule_name_fallbacks == 0
    and all_rule_name_fallbacks == 325
    and len(
      fallback_statement_types
    ) == 30
    and not errors
  ):
    print(
      "PASS: all 40 "
      "Toda54BracketUpToSignStatement "
      "fallbacks were replaced by value-set "
      "semantic rendering; 325 remain across "
      "30 statement types."
    )
  else:
    print(
      "MEASURED RESULT: inspect values before "
      "continuing."
    )


if __name__ == "__main__":
  main()
