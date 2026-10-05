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


def _render_pi6_3() -> str:
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


def _reference_and_body() -> tuple[
  str,
  str,
]:
  rendered = _render_pi6_3()
  reference, body = rendered.split(
    "\n## 証明\n",
    1,
  )

  return (
    reference,
    body,
  )


def test_phase157_r11_r7_equation_53_reference_contains_hopf_value():
  reference, _ = _reference_and_body()

  assert (
    r"$H\left(\nu'\right) = \eta_{5}$."
    in reference
  )


def test_phase157_r11_r7_first_visible_argument_uses_mazu():
  _, body = _reference_and_body()

  assert (
    "まず, "
    r"$\nu'$ の位数を決定するために"
    in body
  )


def test_phase157_r11_r7_reference_reuse_is_explicit():
  _, body = _reference_and_body()

  assert (
    "[R1]より, "
    r"$\nu' \in \pi_{6}^{3}$."
    in body
  )


def test_phase157_r11_r7_hopf_support_precedes_surjectivity():
  _, body = _reference_and_body()

  hopf_value = (
    "[R1]より, "
    r"$H\left(\nu'\right) = \eta_{5}$."
  )
  target_group = (
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$."
  )
  surjectivity = (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である."
  )

  assert hopf_value in body
  assert target_group in body
  assert surjectivity in body

  assert body.index(
    target_group
  ) < body.index(
    surjectivity
  )
  assert body.index(
    hopf_value
  ) < body.index(
    surjectivity
  )


def test_phase157_r11_r7_generic_final_filler_is_absent():
  _, body = _reference_and_body()

  assert (
    "以上で得た群構造, 生成元, "
    "および写像に関する結果を合わせると,"
    not in body
  )


def test_phase157_r11_r7_display_math_lines_end_with_period():
  rendered = _render_pi6_3()

  for line in rendered.splitlines():
    stripped = line.strip()

    if (
      stripped.startswith(
        "$"
      )
      and stripped.endswith(
        "$"
      )
      and stripped != r"$\square$"
    ):
      raise AssertionError(
        "display-math line lacks ASCII period: "
        + stripped
      )


def test_phase157_r11_r7_exact_sequence_ends_with_period():
  _, body = _reference_and_body()

  assert (
    r"$0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0$."
    in body
  )
