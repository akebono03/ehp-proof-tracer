import pytest

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
  _build_group_proof_rendered_lines,
  build_standard_web_group_proof_view,
)


def _rendered_group_proof(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
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

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def _assert_reference_proof_boundary(
  rendered: str,
) -> None:
  reference_marker = "## 使用する結果"
  proof_marker = "\n## 証明\n"

  reference_index = rendered.index(
    reference_marker
  )
  proof_index = rendered.index(
    proof_marker,
    reference_index,
  )
  separator_index = rendered.rfind(
    "\n---\n",
    reference_index,
    proof_index,
  )

  assert separator_index >= 0
  assert (
    reference_index
    < separator_index
    < proof_index
  )
  assert (
    rendered[
      separator_index:
      proof_index
    ].strip()
    == "---"
  )


@pytest.mark.parametrize(
  ("n", "k"),
  (
    (3, 3),
    (5, 3),
    (4, 6),
    (5, 7),
    (8, 7),
    (9, 7),
  ),
)
def test_phase157_r5_r10_public_reference_proof_boundary(
  n,
  k,
):
  rendered = _rendered_group_proof(
    n,
    k,
  )

  if "## 使用する結果" not in rendered:
    pytest.skip(
      "this proof has no reference section"
    )

  assert "\n## 証明\n" in rendered
  _assert_reference_proof_boundary(
    rendered
  )


def test_phase157_r5_r10_pi6_3_legacy_intro_is_normalized():
  rendered = _rendered_group_proof(
    3,
    3,
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
  _assert_reference_proof_boundary(
    rendered
  )


@pytest.mark.parametrize(
  ("n", "k"),
  (
    (3, 3),
    (5, 3),
    (4, 6),
    (5, 7),
    (8, 7),
    (9, 7),
  ),
)
def test_phase157_r5_r10_narrative_ends_with_qed(
  n,
  k,
):
  rendered = _rendered_group_proof(
    n,
    k,
  )

  assert rendered.rstrip().endswith(
    r"$\square$"
  )


def test_phase157_r5_r10_separator_parser_recognizes_horizontal_rule():
  rendered_lines = (
    _build_group_proof_rendered_lines(
      (
        "## 使用する結果\n"
        "reference\n"
        "\n"
        "---\n"
        "\n"
        "## 証明\n"
        "proof\n"
        "$\\square$\n"
      )
    )
  )

  assert any(
    line.kind == "separator"
    for line in rendered_lines
  )


def test_phase157_r5_r10_web_adapter_exposes_separator_and_qed():
  view = build_standard_web_group_proof_view(
    3,
    3,
    max_depth=2,
    mode="narrative",
  )

  kinds = tuple(
    line.kind
    for line in view.rendered_lines
  )

  assert "separator" in kinds
  assert any(
    line.kind == "heading"
    and line.prefix == "使用する結果"
    for line in view.rendered_lines
  )
  assert any(
    line.kind == "heading"
    and line.prefix == "証明"
    for line in view.rendered_lines
  )
  assert any(
    any(
      segment.kind == "inline_math"
      and segment.value == r"\square"
      for segment in line.segments
    )
    for line in view.rendered_lines
  )
