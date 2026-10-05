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
from web_group_proof import (
  build_standard_web_group_proof_view,
)


def _presentation(n, k, max_depth=2):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=max_depth,
  )
  return build_toda_group_proof_presentation(
    replay
  )


def _web_text(n, k, max_depth=2):
  view = build_standard_web_group_proof_view(
    n,
    k,
    max_depth=max_depth,
    mode="narrative",
  )
  parts = []
  for line in view.rendered_lines:
    if line.segments:
      parts.append(
        "".join(
          segment.value
          for segment in line.segments
        )
      )
    else:
      parts.append(
        line.prefix
        + (
          ""
          if line.statement_latex is None
          else line.statement_latex
        )
        + line.suffix
      )
  return "\n".join(parts)


def test_phase150_rc4_7d_3_pi10_public_and_web_use_generic_reason_route():
  markdown = render_toda_group_proof_narrative_markdown(
    _presentation(
      4,
      6,
    )
  )
  web_text = _web_text(
    4,
    6,
  )

  assert "以上で得た群構造" in markdown
  assert "結果を合わせると" in markdown
  assert "以上で得た群構造" in web_text
  assert "結果を合わせると" in web_text


def test_phase150_rc4_7d_3_pi12_public_and_web_use_generic_reason_route():
  markdown = render_toda_group_proof_narrative_markdown(
    _presentation(
      5,
      7,
    )
  )
  web_text = _web_text(
    5,
    7,
  )

  assert "この完全性" in markdown
  assert "結果を合わせると" in markdown
  assert "この完全性" in web_text
  assert "結果を合わせると" in web_text


def test_phase150_rc4_7d_3_pi16_public_and_web_use_generic_reason_route():
  markdown = render_toda_group_proof_narrative_markdown(
    _presentation(9, 7)
  )
  web_text = _web_text(9, 7)
  phrase = (
    "群構造に関する結果と写像による移送の結果を合わせると"
  )
  assert phrase in markdown
  assert phrase in web_text


def test_phase150_rc4_7d_3_pi8_dedicated_route_is_preserved():
  markdown = render_toda_group_proof_narrative_markdown(
    _presentation(5, 3)
  )
  assert "# Group proof narrative" in markdown
  assert "Toda Proposition 5.6 のうち," in markdown


def test_phase150_rc4_7d_3_pi15_dedicated_route_is_preserved():
  markdown = render_toda_group_proof_narrative_markdown(
    _presentation(8, 7)
  )
  assert "Toda Proposition 5.15 のうち," in markdown
  assert "直和因子の順序を入れ替えると," in markdown


def test_phase150_rc4_7d_3_depth1_rc4_target_keeps_existing_route():
  markdown = render_toda_group_proof_narrative_markdown(
    _presentation(
      4,
      6,
      max_depth=1,
    )
  )
  assert "# Group proof narrative" in markdown
  assert (
    "以上で得た群構造、生成元、および写像に関する"
    "結果を合わせると"
    not in markdown
  )
