from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def main() -> None:
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )
  reference_part = rendered.split(
    "まず",
    1,
  )[0]

  print(
    "=" * 72
  )
  print(
    "Phase 153-R11 Test Replacement R5 audit"
  )
  print(
    "=" * 72
  )
  print(
    reference_part
  )

  failures = []

  if "使用する結果を先にまとめる." not in reference_part:
    failures.append(
      "Reference section missing"
    )

  if "(5.3)" not in reference_part:
    failures.append(
      "(5.3) missing"
    )

  if "Proposition 5.3" not in reference_part:
    failures.append(
      "Proposition 5.3 missing"
    )

  if "Proposition 5.6" in reference_part:
    failures.append(
      "root self-reference Proposition 5.6 remains"
    )

  print()

  if failures:
    print(
      "FAIL"
    )
    for failure in failures:
      print(
        "  ",
        failure,
      )
    raise SystemExit(
      1
    )

  print(
    "PASS"
  )
  print(
    "Depth-2 pi6_3 Reference section is self-reference-free "
    "and keeps used external References."
  )


if __name__ == "__main__":
  main()
