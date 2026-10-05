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


def _render_pi6_3_repair14() -> str:
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


def test_phase157_r20_repair14_late_surjectivity_support_keeps_prop53():
  rendered = _render_pi6_3_repair14()

  reference, body = rendered.split(
    "---",
    1,
  )

  assert "**[R3] Proposition 5.3.**" in reference
  assert (
    r"$\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}^{2}\}$."
    in reference
  )

  prop53_support = (
    r"[R3]より, $\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}^{2}\}$"
  )
  surjective = (
    r"$H: \pi_{7}^{3} \to "
    r"\pi_{7}^{5}$ は全射である."
  )

  assert prop53_support in body
  assert surjective in body
  assert body.index(
    prop53_support
  ) < body.index(
    surjective
  )


def test_phase157_r20_repair14_removes_wrong_reference_from_map_property():
  rendered = _render_pi6_3_repair14()
  body = rendered.split(
    "---",
    1,
  )[1]

  assert (
    r"[R1]より, $H: \pi_{7}^{3} "
    r"\to \pi_{7}^{5}$ は全射である."
    not in body
  )
  assert (
    r"[R1]を用いて, $H: \pi_{7}^{3} "
    r"\to \pi_{7}^{5}$ は全射である."
    not in body
  )


def test_phase157_r20_repair14_public_reference_order_is_r1_through_r5():
  rendered = _render_pi6_3_repair14()
  reference = rendered.split(
    "---",
    1,
  )[0]

  headers = (
    "**[R1] Proposition 5.6.**",
    "**[R2] (5.3).**",
    "**[R3] Proposition 5.3.**",
    "**[R4] Proposition 5.1.**",
    "**[R5] Proposition 2.2.**",
  )

  for header in headers:
    assert header in reference
