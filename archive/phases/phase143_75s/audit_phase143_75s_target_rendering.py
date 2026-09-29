from collections import Counter

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def main():
  occurrences = 0
  rendered_count = 0
  none_count = 0
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

      for node in presentation.nodes:
        statement = node.proof_step.conclusion

        if (
          type(statement).__name__
          != "Toda58EquationStatement"
        ):
          continue

        target = (
          statement.whitehead_nu_relation
        )
        occurrences += 1

        try:
          rendered = (
            render_toda_proof_statement_latex(
              target
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

        if rendered is None:
          none_count += 1
        else:
          rendered_count += 1
          output_counts[
            rendered
          ] += 1

  print("=" * 78)
  print(
    "Phase 143-75S target semantic "
    "rendering audit"
  )
  print("=" * 78)
  print(
    "target aggregate components:",
    occurrences,
  )
  print(
    "semantic renderings:",
    rendered_count,
  )
  print(
    "None renderings:",
    none_count,
  )
  print(
    "errors:",
    len(errors),
  )

  print()
  print("Rendered outputs")
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
    occurrences == 45
    and rendered_count == 45
    and none_count == 0
    and not errors
  ):
    print(
      "PASS: all 45 "
      "Toda58WhiteheadSquareUpToSignStatement "
      "aggregate components render semantically."
    )
  else:
    print(
      "FAIL: inspect the measured values above."
    )


if __name__ == "__main__":
  main()
