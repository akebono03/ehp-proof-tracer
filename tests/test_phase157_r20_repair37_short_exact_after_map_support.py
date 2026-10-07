import re

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


def _normalized_display_blocks(
  markdown: str,
) -> tuple[
  str,
  ...,
]:
  blocks = re.findall(
    r"\\\[\s*(.*?)\s*\\\]",
    markdown,
    flags=re.DOTALL,
  )

  return tuple(
    re.sub(
      r"\s+",
      "",
      block,
    ).rstrip(
      "."
    )
    for block in blocks
  )


def test_phase157_r20_repair37_short_exact_follows_surjectivity():
  body = _body_pi6_3_repair37()

  surjectivity = (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ "
    "は全射."
  )
  reason = (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
  )
  normalized_short_exact = re.sub(
    r"\s+",
    "",
    (
      r"0\longrightarrow \pi_{5}^{2}"
      r"\xrightarrow{E} \pi_{6}^{3}"
      r"\xrightarrow{H} \pi_{6}^{5}"
      r"\longrightarrow 0"
    ),
  )

  assert surjectivity in body
  assert reason in body
  assert normalized_short_exact in (
    _normalized_display_blocks(
      body
    )
  )

  short_exact_start = body.index(
    r"\[",
    body.index(
      reason
    ),
  )

  assert body.index(
    surjectivity
  ) < body.index(
    reason
  )
  assert body.index(
    reason
  ) < short_exact_start


def test_phase157_r20_repair37_short_exact_follows_injectivity():
  body = _body_pi6_3_repair37()

  injectivity = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ "
    "は単射."
  )
  normalized_short_exact = re.sub(
    r"\s+",
    "",
    (
      r"0\longrightarrow \pi_{5}^{2}"
      r"\xrightarrow{E} \pi_{6}^{3}"
      r"\xrightarrow{H} \pi_{6}^{5}"
      r"\longrightarrow 0"
    ),
  )

  assert injectivity in body
  assert normalized_short_exact in (
    _normalized_display_blocks(
      body
    )
  )

  short_exact_start = body.index(
    r"\[",
    body.index(
      injectivity
    ),
  )

  assert body.index(
    injectivity
  ) < short_exact_start
