from collections import Counter

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _group_proof_narrative_statement_label,
  _render_group_proof_narrative_latex,
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


def main():
  occurrences = Counter()
  fallbacks = Counter()
  errors = []

  for k in range(8):
    for n in range(2, 16):
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

        latex = _render_group_proof_narrative_latex(
          proof_step
        )
        label = _group_proof_narrative_statement_label(
          statement
        )

        if (
          latex is None
          and label is None
          and proof_step.inference_rule
          is not None
        ):
          fallbacks[name] += 1

  print("=" * 78)
  print(
    "Phase 143-75I Whitehead-square / "
    "Hopf-invariant semantic rendering audit"
  )
  print(
    "range: n=2..15, k=0..7, depth=7"
  )
  print("=" * 78)

  for target_type in TARGET_TYPES:
    name = target_type.__name__
    print(
      f"{name}: "
      f"{occurrences[name]} occurrences, "
      f"{fallbacks[name]} "
      "inference-rule-name fallbacks"
    )

  print(
    f"errors: {len(errors)}"
  )
  print("=" * 78)

  if (
    not errors
    and sum(
      fallbacks.values()
    ) == 0
  ):
    print(
      "PASS: all three Phase 143-75I "
      "statement types render semantically."
    )
  else:
    print(
      "FAIL: target fallback remains."
    )


if __name__ == "__main__":
  main()
