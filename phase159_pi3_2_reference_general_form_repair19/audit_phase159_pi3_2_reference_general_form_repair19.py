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
    n=2,
    k=1,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  reference = (
    rendered.split(
      "## 使用する結果\n\n",
      1,
    )[1].split(
      "\n---\n",
      1,
    )[0]
  )

  expected_first = (
    r"$\pi_{i}^{1} = 0\ (i > 1),"
    r"\qquad "
    r"\pi_{i}^{n} = 0\ (i < n)$."
  )
  expected_second = (
    r"$\pi_{n}^{n} = "
    r"\mathbb{Z}\{\iota_{n}\}$."
  )

  assert "**[R1] (5.1).**" in reference
  assert expected_first in reference
  assert expected_second in reference

  assert r"\pi_{2}^{1} = 0" not in reference
  assert r"\pi_{3}^{3}" not in reference
  assert (
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$"
    not in reference
  )

  print(
    "=== Phase 159 pi3_2 Reference ==="
  )
  print(
    reference.strip()
  )
  print()
  print(
    "PASS: Toda (5.1) is rendered "
    "in general fixed-statement form."
  )


if __name__ == "__main__":
  main()
