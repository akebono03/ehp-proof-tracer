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


TARGET_NAME = "TodaProp44SuspensionInjectiveStatement"


def main():
  occurrences = 0
  fallback = 0
  semantic = 0
  rule_counts = Counter()
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
        replay = build_toda_group_result_proof_replay(
          group_result,
          max_depth=7,
        )
        presentation = build_toda_group_proof_presentation(
          replay
        )

        for node in presentation.nodes:
          step = node.proof_step
          if (
            type(step.conclusion).__name__
            != TARGET_NAME
          ):
            continue

          occurrences += 1
          rule_counts[step.inference_rule.name] += 1
          rendered = _render_group_proof_narrative_fact(
            step
          )

          if rendered == step.inference_rule.name:
            fallback += 1

          if (
            rendered.startswith("$E: ")
            and r" \hookrightarrow " in rendered
            and rendered.endswith("$")
          ):
            semantic += 1

      except Exception as exc:
        errors.append(
          (n, k, type(exc).__name__, str(exc))
        )

  print("=" * 78)
  print("Phase 143-75P target semantic rendering audit")
  print("=" * 78)
  print("target occurrences:", occurrences)
  print("semantic renderings:", semantic)
  print("rule-name fallback:", fallback)
  print("errors:", len(errors))
  print("rules:")
  for name, count in rule_counts.most_common():
    print("  " + str(count) + " x " + name)

  if errors:
    print("error details:")
    for error in errors:
      print("  " + repr(error))

  print("=" * 78)

  if (
    occurrences == 55
    and semantic == 55
    and fallback == 0
    and not errors
  ):
    print(
      "PASS: all 55 target occurrences use "
      "generic map-based injectivity rendering."
    )
  else:
    print("FAIL: inspect the measured result.")


if __name__ == "__main__":
  main()
