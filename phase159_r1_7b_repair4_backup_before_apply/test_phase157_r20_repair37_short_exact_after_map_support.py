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


def _body_pi6_3_repair37() -> str:
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate.group_result
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


def test_phase157_r20_repair37_short_exact_follows_surjectivity():
  body = _body_pi6_3_repair37()

  surjectivity = (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ "
    "は全射である."
  )
  reason = (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
  )
  short_exact = (
    "\\[\n"
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    "\\longrightarrow 0.\n"
    "\\]"
  )

  assert surjectivity in body
  assert reason in body
  assert short_exact in body

  assert body.index(
    surjectivity
  ) < body.index(
    reason
  )
  assert body.index(
    reason
  ) < body.index(
    short_exact
  )


def test_phase157_r20_repair37_short_exact_follows_injectivity():
  body = _body_pi6_3_repair37()

  injectivity = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ "
    "は単射である."
  )
  short_exact = (
    "\\[\n"
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    "\\longrightarrow 0.\n"
    "\\]"
  )

  assert body.index(
    injectivity
  ) < body.index(
    short_exact
  )
