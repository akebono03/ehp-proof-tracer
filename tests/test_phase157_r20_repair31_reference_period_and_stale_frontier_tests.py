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


def _render_pi6_3_repair31() -> str:
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase157_r20_repair31_reference_prefixed_math_lines_end_with_period():
  rendered = _render_pi6_3_repair31()
  body = rendered.split(
    "---",
    1,
  )[1]

  expected = (
    "[R3]より, "
    r"$\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}^{2}\}$."
  )

  assert expected in body


def test_phase157_r20_repair31_r2_hopf_reference_line_ends_with_period():
  rendered = _render_pi6_3_repair31()
  body = rendered.split(
    "---",
    1,
  )[1]

  expected = (
    "[R2]より, "
    r"$H\left(\nu'\right) = \eta_{5}$."
  )

  assert expected in body


def test_phase157_r20_repair31_all_math_terminated_lines_have_period():
  rendered = _render_pi6_3_repair31()

  for line in rendered.splitlines():
    stripped = line.strip()

    if (
      stripped.endswith(
        "$"
      )
      and "$" in stripped
      and stripped != r"$\square$"
    ):
      raise AssertionError(
        "math-terminated line lacks ASCII period: "
        + stripped
      )
