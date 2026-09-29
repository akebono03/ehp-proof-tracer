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


TARGET_NAMES = (
  "TodaProp53FiniteDimensionalStatement",
  "TodaProp58FiniteDimensionalStatement",
  "TodaProp59FiniteDimensionalStatement",
  "TodaProp511NuSquaredFiniteDimensionalStatement",
)

EXPECTED = {
  "TodaProp53FiniteDimensionalStatement": 76,
  "TodaProp58FiniteDimensionalStatement": 25,
  "TodaProp59FiniteDimensionalStatement": 20,
  "TodaProp511NuSquaredFiniteDimensionalStatement": 14,
}


def main():
  occurrences = Counter()
  fallback = Counter()
  errors = []

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

        for node in presentation.nodes:
          statement = (
            node.proof_step.conclusion
          )
          name = type(statement).__name__
          if name not in TARGET_NAMES:
            continue

          occurrences[name] += 1
          rendered = (
            _render_group_proof_narrative_fact(
              node.proof_step
            )
          )
          rule = node.proof_step.inference_rule
          rule_name = (
            rule.name
            if rule is not None
            else None
          )
          if (
            rule_name is not None
            and rendered == rule_name
          ):
            fallback[name] += 1
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
    "Phase 143-75M target fallback audit"
  )
  print("=" * 78)
  for name in TARGET_NAMES:
    print(
      name
      + ": "
      + str(occurrences[name])
      + " occurrences, "
      + str(fallback[name])
      + " rule-name fallback"
    )
  print(
    "total occurrences:",
    sum(occurrences.values()),
  )
  print(
    "total target fallback:",
    sum(fallback.values()),
  )
  print(
    "errors:",
    len(errors),
  )

  if (
    occurrences == Counter(EXPECTED)
    and not fallback
    and not errors
  ):
    print(
      "PASS: all 135 target occurrences "
      "use generic semantic rendering."
    )
  else:
    print("FAIL")
    for error in errors[:20]:
      print("  -", error)


if __name__ == "__main__":
  main()
