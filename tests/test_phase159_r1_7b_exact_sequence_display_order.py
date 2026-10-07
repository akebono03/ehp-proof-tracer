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


def _phase159_r1_7b_render(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[
      0
    ].source_candidate.group_result
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


def _normalized_latex(
  latex: str,
) -> str:
  return re.sub(
    r"\s+",
    "",
    latex,
  ).rstrip(
    "."
  )


def test_phase159_r1_7b_pi6_3_short_exact_sequence_is_display_math():
  rendered = _phase159_r1_7b_render(
    3,
    3,
  )
  expected = _normalized_latex(
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
  )

  assert expected in (
    _normalized_display_blocks(
      rendered
    )
  )
  assert (
    r"$0\longrightarrow \pi_{5}^{2}"
    not in rendered
  )


def test_phase159_r1_7b_pi11_4_delta_surjectivity_has_matching_exactness_before_it():
  rendered = _phase159_r1_7b_render(
    4,
    7,
  )
  expected = _normalized_latex(
    r"\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} "
    r"\xrightarrow{\Delta} \pi_{8}^{2}"
  )
  surjectivity = (
    r"$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$"
    " は全射."
  )

  assert expected in (
    _normalized_display_blocks(
      rendered
    )
  )
  assert surjectivity in rendered

  displays = list(
    re.finditer(
      r"\\\[\s*(.*?)\s*\\\]",
      rendered,
      flags=re.DOTALL,
    )
  )
  matching = next(
    match
    for match in displays
    if (
      _normalized_latex(
        match.group(
          1
        )
      )
      == expected
    )
  )
  surjectivity_index = rendered.index(
    surjectivity
  )
  reason_index = rendered.rfind(
    "完全性より,",
    matching.end(),
    surjectivity_index,
  )

  assert matching.start() < reason_index
  assert reason_index < surjectivity_index


def test_phase159_r1_7b_pi11_4_visible_exactness_windows_use_display_math():
  rendered = _phase159_r1_7b_render(
    4,
    7,
  )
  expected = _normalized_latex(
    r"\pi_{9}^{2} \xrightarrow{E} \pi_{10}^{3} "
    r"\xrightarrow{H} \pi_{10}^{5}"
  )

  assert expected in (
    _normalized_display_blocks(
      rendered
    )
  )
  assert (
    r"$\pi_{9}^{2} \xrightarrow{E} \pi_{10}^{3}"
    not in rendered
  )
