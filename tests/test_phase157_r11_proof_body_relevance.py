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


def _render_pi6_3(
  max_depth: int = 2,
) -> str:
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
    max_depth=max_depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _proof_body(
  rendered: str,
) -> str:
  return rendered.split(
    "\n## 証明\n",
    1,
  )[1]


def test_phase157_r11_pi6_3_body_excludes_unconsumed_suspension_isomorphism():
  body = _proof_body(
    _render_pi6_3()
  )

  assert (
    r"$E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である."
    not in body
  )


def test_phase157_r11_pi6_3_body_keeps_consumed_pi6_5_group():
  body = _proof_body(
    _render_pi6_3()
  )

  assert (
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$"
    in body
  )


def test_phase157_r11_pi6_5_group_precedes_its_order_consumer():
  body = _proof_body(
    _render_pi6_3()
  )
  pi6_5 = (
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$"
  )
  consumer = (
    "この短完全列と両端の群の位数より, "
    "中央の群の位数は"
  )

  assert pi6_5 in body
  assert consumer in body
  assert body.index(
    pi6_5
  ) < body.index(
    consumer
  )
