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


def _render_group(
  n,
  k,
):
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


def _reference_section(
  rendered: str,
) -> str:
  marker = "## 使用する結果\n"

  if marker not in rendered:
    return ""

  after_header = rendered.split(
    marker,
    1,
  )[1]

  return after_header.split(
    "## 証明",
    1,
  )[0]


def _header_numbers(
  rendered: str,
) -> tuple[
  int,
  ...,
]:
  return tuple(
    int(
      value
    )
    for value in re.findall(
      r"\*\*\[R([0-9]+)\]",
      _reference_section(
        rendered
      ),
    )
  )


def _body_numbers(
  rendered: str,
) -> tuple[
  int,
  ...,
]:
  if "## 証明" not in rendered:
    return ()

  body = rendered.split(
    "## 証明",
    1,
  )[1]

  return tuple(
    int(
      value
    )
    for value in re.findall(
      r"\[R([0-9]+)\]",
      body,
    )
  )


def test_phase153_r13_pi4_2_excludes_root_equation_by_locator_identity():
  rendered = _render_group(
    2,
    2,
  )
  section = _reference_section(
    rendered
  )

  assert "(5.2)" not in section


def test_phase153_r13_pi8_5_specialized_connector_keeps_only_used_references():
  rendered = _render_group(
    5,
    3,
  )
  section = _reference_section(
    rendered
  )

  assert "Proposition 5.6" not in section

  header_numbers = set(
    _header_numbers(
      rendered
    )
  )
  body_numbers = set(
    _body_numbers(
      rendered
    )
  )

  assert header_numbers
  assert header_numbers == body_numbers


def test_phase153_r13_pi15_8_specialized_reference_fallback_stays_external():
  rendered = _render_group(
    8,
    7,
  )
  section = _reference_section(
    rendered
  )

  assert "Proposition 5.15" not in section
  assert "Proposition 4.4" in section
  assert _header_numbers(
    rendered
  ) == (
    1,
  )
  assert set(
    _body_numbers(
      rendered
    )
  ) == {
    1,
  }


def test_phase153_r13_reference_numbers_are_contiguous_for_repaired_groups():
  for n, k in (
    (2, 2),
    (5, 3),
    (8, 7),
  ):
    rendered = _render_group(
      n,
      k,
    )
    numbers = _header_numbers(
      rendered
    )

    assert numbers == tuple(
      range(
        1,
        len(
          numbers
        )
        + 1,
      )
    )
