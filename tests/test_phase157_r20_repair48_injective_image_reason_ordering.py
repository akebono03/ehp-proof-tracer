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


def _body_pi6_3_repair48() -> str:
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
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  return rendered.split(
    "\n## 証明\n",
    1,
  )[1]


def test_phase157_r20_repair48_injective_image_reason_follows_both_visible_premises():
  body = _body_pi6_3_repair48()

  group_structure = (
    "[R1]より, "
    r"$\pi_{5}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}^{3}\}$."
  )
  injective = (
    r"$E: \pi_{5}^{2} \to "
    r"\pi_{6}^{3}$ は単射である."
  )
  reason = (
    "この群構造と $E$ の単射性より, "
    r"$E(\eta_{2}^{3})="
    r"\eta_{3}^{3}\neq0$ であり, "
    "単射写像は元の位数を保つ."
  )
  conclusion = (
    r"$\operatorname{ord}"
    r"\left(\eta_{3}^{3}\right) = 2$."
  )

  assert body.index(
    group_structure
  ) < body.index(
    reason
  )
  assert body.index(
    injective
  ) < body.index(
    reason
  )
  assert body.index(
    reason
  ) < body.index(
    conclusion
  )


def test_phase157_r20_repair48_reason_is_immediately_before_eta_order():
  body = _body_pi6_3_repair48()

  reason = (
    "この群構造と $E$ の単射性より, "
    r"$E(\eta_{2}^{3})="
    r"\eta_{3}^{3}\neq0$ であり, "
    "単射写像は元の位数を保つ."
  )
  conclusion = (
    r"$\operatorname{ord}"
    r"\left(\eta_{3}^{3}\right) = 2$."
  )

  paragraphs = tuple(
    paragraph.strip()
    for paragraph in body.split(
      "\n\n"
    )
    if paragraph.strip()
  )

  reason_index = paragraphs.index(
    reason
  )
  conclusion_index = paragraphs.index(
    conclusion
  )

  assert (
    conclusion_index
    == reason_index + 1
  )


def test_phase157_r20_repair48_prop22_dependency_order_remains_correct():
  body = _body_pi6_3_repair48()

  fixed_reference = (
    "[R5]より, "
    r"$H(\alpha\circ E\beta) = "
    r"H(\alpha)\circ E\beta$."
  )
  specialization = (
    r"$H\left(\nu'\eta_{6}\right) = "
    r"H\left(\nu'\right)\eta_{6}\tag{7}$."
  )
  value = (
    r"$H\left(\nu'\eta_{6}\right) = "
    r"\eta_{5}^{2}\tag{8}$."
  )

  assert body.index(
    fixed_reference
  ) < body.index(
    specialization
  ) < body.index(
    value
  )
