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
  depth: int,
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
    max_depth=depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _body(
  rendered: str,
) -> str:
  marker = (
    "次に, $\\nu'$ の位数を決定するために"
  )
  index = rendered.find(
    marker
  )
  assert index >= 0
  return rendered[
    index:
  ]


def test_phase156_r5_repair9_depth2_public_body_starts_after_53_boundary():
  rendered = _render_pi6_3(
    2
  )
  body = _body(
    rendered
  )

  assert rendered.startswith(
    "# Group proof narrative"
  )
  assert "## 使用する結果" in rendered
  assert "\n## 証明\n" in rendered
  assert (
    "使用する結果を先にまとめる."
    not in rendered
  )
  assert "(5.3)" in rendered
  assert "Lemma 5.2" not in rendered
  assert "$\\nu'$ を定める." not in rendered
  assert (
    "\\nu' \\in "
    "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"
    not in rendered
  )
  assert body.startswith(
    "次に, $\\nu'$ の位数を決定するために"
  )


def test_phase156_r5_repair9_depth3_public_body_starts_after_53_boundary():
  rendered = _render_pi6_3(
    3
  )
  body = _body(
    rendered
  )

  assert "(5.3)" in rendered
  assert "Lemma 5.2" not in rendered
  assert "$\\nu'$ を定める." not in rendered
  assert (
    "\\nu' \\in "
    "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"
    not in rendered
  )
  assert body.startswith(
    "次に, $\\nu'$ の位数を決定するために"
  )
