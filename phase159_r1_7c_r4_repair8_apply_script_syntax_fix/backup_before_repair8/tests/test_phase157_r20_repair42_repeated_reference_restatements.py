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


def _body_pi6_3_repair42() -> str:
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


def test_phase157_r20_repair42_hopf_fixed_statement_is_not_repeated():
  body = _body_pi6_3_repair42()

  assert (
    body.count(
      r"H\left(\nu'\right) = \eta_{5}"
    )
    == 1
  )
  assert (
    "[R2]より, "
    r"$H\left(\nu'\right) = \eta_{5}$."
    in body
  )


def test_phase157_r20_repair42_double_nu_fixed_statement_is_not_repeated():
  body = _body_pi6_3_repair42()

  assert (
    body.count(
      "[R2]より, "
      r"$2\nu' = \eta_{3}^{3}"
    )
    == 1
  )
  assert (
    r"$\operatorname{ord}(\eta_{3}^{3})=2$ "
    r"かつ $2\nu'=\eta_{3}^{3}$ より, "
    r"$4\nu'=0$ かつ $2\nu'\neq0$ である."
    in body
  )


def test_phase157_r20_repair42_short_exact_order_remains_correct():
  body = _body_pi6_3_repair42()

  surjectivity = (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ "
    "は全射である."
  )
  reason = (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
  )

  assert body.index(
    surjectivity
  ) < body.index(
    reason
  )
