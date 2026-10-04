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
from toda_proof_dependency import (
  TodaProofDependencyRole,
  classify_toda_proof_step_role,
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


def test_phase157_r11_r11_equation_53_reference_contains_fixed_hopf_value():
  reference, _ = _reference_and_body()

  assert "**[R2] (5.3).**" in reference
  assert (
    r"$H\left(\nu'\right) = \eta_{5}$."
    in reference
  )


def test_phase157_r11_r11_first_visible_argument_uses_mazu():
  _, body = _reference_and_body()

  assert (
    "まず, "
    r"$\nu'$ の位数を決定するために"
    in body
  )


def test_phase157_r11_r11_reference_reuse_is_explicit():
  _, body = _reference_and_body()

  assert (
    "[R2]より, "
    r"$\nu' \in \pi_{6}^{3}$."
    in body
  )


def test_phase157_r11_r11_hopf_derivation_precedes_surjectivity():
  _, body = _reference_and_body()

  fixed_hopf = (
    "[R2]より, "
    r"$H\left(\nu'\right)=\eta_{5}$."
  )
  target_group = (
    "[R4]より, "
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$."
  )
  surjectivity = (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である."
  )

  assert fixed_hopf in body
  assert target_group in body
  assert surjectivity in body

  assert body.index(
    fixed_hopf
  ) < body.index(
    target_group
  )
  assert body.index(
    target_group
  ) < body.index(
    surjectivity
  )


def test_phase157_r11_r11_generic_final_filler_is_absent():
  _, body = _reference_and_body()

  assert (
    "以上で得た群構造, 生成元, "
    "および写像に関する結果を合わせると,"
    not in body
  )


def test_phase157_r11_r11_display_math_lines_end_with_period():
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


def test_phase157_r11_r11_exact_sequence_ends_with_period():
  _, body = _reference_and_body()

  assert (
    r"$0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0$."
    in body
  )


def test_phase157_r11_r11_hopf_surjectivity_is_dependency_map_property():
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

  stack = [
    group_result.proof_step,
  ]
  visited = set()
  hopf_surjective_steps = []

  while stack:
    proof_step = stack.pop()
    proof_step_id = id(
      proof_step
    )

    if proof_step_id in visited:
      continue

    visited.add(
      proof_step_id
    )

    inference_rule = (
      proof_step.inference_rule
    )

    if (
      inference_rule is not None
      and inference_rule.name
      == "Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity"
    ):
      hopf_surjective_steps.append(
        proof_step
      )

    stack.extend(
      reversed(
        proof_step.premises
      )
    )

  assert hopf_surjective_steps

  for proof_step in hopf_surjective_steps:
    assert (
      classify_toda_proof_step_role(
        proof_step
      )
      is TodaProofDependencyRole.MAP_PROPERTY
    )


def test_phase157_r11_r11_reference_keeps_all_used_equation_53_components():
  reference, _ = _reference_and_body()

  assert "**[R2] (5.3).**" in reference
  assert (
    r"$2\nu' = \eta_{3}^{3}$."
    in reference
  )
  assert (
    r"$H\left(\nu'\right) = \eta_{5}$."
    in reference
  )


def test_phase157_r11_r11_reference_non_definition_lines_end_with_period():
  reference, _ = _reference_and_body()

  assert (
    r"$\nu' \in \pi_{6}^{3}$."
    in reference
  )
  assert (
    r"$2\nu' = \eta_{3}^{3}$."
    in reference
  )
  assert (
    r"$H\left(\nu'\right) = \eta_{5}$."
    in reference
  )


def test_phase157_r11_r14_eta3_cube_order_follows_injectivity():
  _, body = _reference_and_body()

  injectivity = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である."
  )
  eta_cube_order = (
    r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$."
  )

  assert injectivity in body
  assert eta_cube_order in body
  assert body.index(
    injectivity
  ) < body.index(
    eta_cube_order
  )



def test_phase157_r11_r14_surjectivity_precedes_short_exact_derivation():
  _, body = _reference_and_body()

  surjectivity = (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である."
  )
  short_exact_reason = (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
  )
  short_exact = (
    r"$0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0$."
  )

  assert surjectivity in body
  assert short_exact_reason in body
  assert short_exact in body
  assert body.index(
    surjectivity
  ) < body.index(
    short_exact_reason
  )
  assert body.index(
    surjectivity
  ) < body.index(
    short_exact
  )



def test_phase157_r11_r14_used_prop53_reference_is_public():
  reference, body = _reference_and_body()

  assert "**[R3] Proposition 5.3.**" in reference
  assert "[R3]" in body

