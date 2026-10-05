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
  marker = "\n## 使用する結果\n"

  if marker not in rendered:
    return ""

  tail = rendered.split(
    marker,
    1,
  )[1]

  return tail.split(
    "\n## 証明\n",
    1,
  )[0]


def _proof_body(
  rendered: str,
) -> str:
  marker = "\n## 証明\n"

  if marker not in rendered:
    return rendered

  return rendered.split(
    marker,
    1,
  )[1]


def test_phase157_r20_repair53_r5_pi15_8_keeps_required_fixed_components():
  rendered = _render_group(
    8,
    7,
  )
  reference_section = _reference_section(
    rendered
  )

  assert "**[R1] Proposition 5.15.**" in reference_section
  assert (
    r"$\pi_{14}^{7} = \mathbb{Z}/8\{\sigma'\}$"
    in reference_section
  )
  assert (
    r"\pi_{15}^{8} \cong "
    not in reference_section
  )

  assert "**[R2] Proposition 4.4.**" in reference_section
  assert (
    r"$(α, \beta) \mapsto Eα + \sigma_{8}\beta: "
    r"\pi_{14}^{7} \oplus \pi_{15}^{15} "
    r"\to \pi_{15}^{8}$ は同型写像である."
    in reference_section
  )


def test_phase157_r20_repair53_r5_pi15_8_body_links_each_fixed_component():
  rendered = _render_group(
    8,
    7,
  )
  body = _proof_body(
    rendered
  )

  assert (
    "[R1] より,\n\n"
    "\\[\n"
    r"\pi_{14}^{7} = \mathbb{Z}/8\{\sigma'\}"
    "\n\\]"
    in body
  )
  assert (
    "[R2] より, これらの生成元はそれぞれ"
    in body
  )


def test_phase157_r20_repair53_r5_pi15_8_has_no_stale_reference_number():
  rendered = _render_group(
    8,
    7,
  )
  reference_section = _reference_section(
    rendered
  )
  body = _proof_body(
    rendered
  )

  assert "**[R3]" not in reference_section
  assert "[R3]" not in body
  assert "**[R1] Proposition 4.4.**" not in reference_section
  assert "**[R2] Proposition 5.15.**" not in reference_section
