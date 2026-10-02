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
  marker = "## 使用する結果\n\n"

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


def test_phase153_r12_pi11_4_excludes_root_proposition_515_reference():
  rendered = _render_group(
    4,
    7,
  )
  reference_section = _reference_section(
    rendered
  )

  assert "Proposition 5.15" not in reference_section
  assert "**[R1] Proposition 5.8.**" in reference_section
  assert "**[R2] Proposition 4.4.**" in reference_section


def test_phase153_r12_pi11_4_body_uses_renumbered_external_references():
  rendered = _render_group(
    4,
    7,
  )
  marker = "## 証明\n\n"
  body = rendered.split(
    marker,
    1,
  )[1]

  assert "[R1]を用いる." in body
  assert (
    r"[R2]より, $\nu_{4}$ の分解写像は同型写像である."
    in body
  )
  assert "[R3]" not in body
  assert "Proposition 5.15" not in body



def test_phase153_r12_pi6_2_r10_reference_filtering_remains_stable():
  rendered = _render_group(
    2,
    4,
  )
  reference_section = _reference_section(
    rendered
  )

  assert "**[R1] Proposition 5.6.**" in reference_section
  assert "**[R2] (5.2).**" in reference_section
  assert "Proposition 5.8" not in reference_section


def test_phase153_r12_pi6_3_r11_generic_root_exclusion_remains_stable():
  rendered = _render_group(
    3,
    3,
  )
  reference_part = rendered.split(
    "まず",
    1,
  )[0]

  assert "Proposition 5.6" not in reference_part
  assert "(5.3)" in reference_part
  assert "Proposition 5.3" in reference_part
