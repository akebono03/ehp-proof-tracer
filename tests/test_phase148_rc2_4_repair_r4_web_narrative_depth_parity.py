import web_group_proof as web_group_proof_module

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
from web_app import (
  create_app,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)


def _pi6_3_group_result():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  return (
    report.candidates[
      0
    ].source_candidate.group_result
  )


def _rendered_text(
  view,
):
  parts = []

  for line in view.rendered_lines:
    if line.segments:
      for segment in line.segments:
        if segment.kind in (
          "inline_math",
          "display_math",
        ):
          parts.append(
            "$"
            + segment.value
            + "$"
          )
        else:
          parts.append(
            segment.value
          )
      parts.append(
        "\n"
      )
      continue

    parts.append(
      line.prefix
    )
    if line.statement_latex is not None:
      parts.append(
        "$"
        + line.statement_latex
        + "$"
      )
    parts.append(
      line.suffix
    )
    parts.append(
      "\n"
    )

  return "".join(
    parts
  )


def test_phase148_rc2_4_repair_r4_web_depth2_narrative_uses_bounded_replay(
  monkeypatch,
):
  original = (
    web_group_proof_module
    .build_toda_group_result_proof_replay
  )
  calls = []

  def recording_replay(
    group_result,
    max_depth=1,
  ):
    calls.append(
      max_depth
    )
    return original(
      group_result,
      max_depth=max_depth,
    )

  monkeypatch.setattr(
    web_group_proof_module,
    "build_toda_group_result_proof_replay",
    recording_replay,
  )

  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )

  assert calls == [
    2,
  ]
  assert view.max_depth == 2
  assert len(
    view.steps
  ) == 18
  assert all(
    step.depth <= 2
    for step in view.steps
  )


def test_phase148_rc2_4_repair_r4_web_depth2_matches_public_depth2_renderer():
  group_result = (
    _pi6_3_group_result()
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  markdown = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  expected_lines = (
    web_group_proof_module
    ._build_group_proof_rendered_lines(
      markdown
    )
  )

  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )

  assert (
    view.rendered_lines
    == expected_lines
  )


def test_phase148_rc2_4_repair_r4_web_depth2_suppresses_recursive_raw_exactness():
  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )
  rendered = (
    _rendered_text(
      view
    )
  )

  assert (
    "は完全である"
    not in rendered
  )
  assert (
    r"\text{ is exact}"
    not in rendered
  )


def test_phase148_rc2_4_repair_r4_web_depth2_preserves_core_narrative_results():
  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )
  rendered = (
    _rendered_text(
      view
    )
  )

  assert (
    r"\operatorname{ord}\left(\nu'\right) = 4"
    in rendered
  )
  assert (
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
    in rendered
  )
  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    in rendered
  )
  assert (
    r"\xrightarrow{E} \pi_{6}^{3}"
    in rendered
  )
  assert (
    r"\xrightarrow{H} \pi_{6}^{5}"
    in rendered
  )
  assert (
    r"\longrightarrow 0"
    in rendered
  )


def test_phase148_rc2_4_repair_r4_web_depth2_preserves_numbered_equations():
  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )
  display_math = tuple(
    segment.value
    for line in view.rendered_lines
    for segment in line.segments
    if segment.kind == "display_math"
  )

  assert any(
    r"\tag{1}" in value
    for value in display_math
  )
  assert any(
    r"\tag{2}" in value
    for value in display_math
  )
  assert any(
    r"\tag{3}" in value
    for value in display_math
  )


def test_phase148_rc2_4_repair_r4_web_response_uses_repaired_depth2_narrative():
  app = create_app()
  app.config.update(
    TESTING=True,
  )
  client = app.test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group_proof",
      "n": "3",
      "k": "3",
      "group_proof_depth": "2",
      "group_proof_mode": "narrative",
    },
  )

  assert response.status_code == 200
  assert b"Selected depth:" in response.data
  assert (
    b"Selected depth:\n          2"
    in response.data
  )
  assert b"\\tag{1}" in response.data
  assert (
    "は完全である".encode(
      "utf-8"
    )
    not in response.data
  )
