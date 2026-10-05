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
  max_depth: int = 2,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=max_depth,
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


def _assert_contract(
  rendered: str,
) -> None:
  lines = rendered.splitlines()

  target_index = lines.index(
    "## 証明対象"
  )
  reference_index = lines.index(
    "## 使用する結果"
  )
  separator_index = lines.index(
    "---"
  )
  proof_index = lines.index(
    "## 証明"
  )

  assert (
    target_index
    < reference_index
    < separator_index
    < proof_index
  )

  nonempty = [
    line.strip()
    for line in lines
    if line.strip()
  ]

  assert (
    nonempty[-1]
    == "□"
  )


def test_phase158_r2_repair3_pi6_3_contract():
  rendered = _render_group(
    3,
    3,
  )

  _assert_contract(
    rendered
  )

  assert (
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
    in rendered
  )


def test_phase158_r2_repair3_target_uses_single_tex_delimiters():
  rendered = _render_group(
    2,
    0,
  )

  assert r"\[" in rendered
  assert r"\]" in rendered
  assert r"\\[" not in rendered
  assert r"\\]" not in rendered


def test_phase158_r2_repair3_pi15_8_preserves_canonical_formula():
  rendered = _render_group(
    8,
    7,
  )

  _assert_contract(
    rendered
  )

  assert (
    r"\left(α, \beta\right) \mapsto "
    r"Eα + \sigma_{8}\beta"
    in rendered
  )


def test_phase158_r2_repair3_pi15_8_preserves_transport():
  rendered = _render_group(
    8,
    7,
  )

  assert (
    r"\sigma' \longmapsto E\sigma'"
    in rendered
  )
  assert (
    r"\iota_{15} \longmapsto \sigma_{8}"
    in rendered
  )


def test_phase158_r2_repair3_reference_free_group_has_empty_reference_body():
  rendered = _render_group(
    2,
    0,
  )

  _assert_contract(
    rendered
  )

  lines = rendered.splitlines()
  reference_index = lines.index(
    "## 使用する結果"
  )
  separator_index = lines.index(
    "---"
  )

  between = [
    line
    for line in lines[
      reference_index + 1:
      separator_index
    ]
    if line.strip()
  ]

  assert between == []


def test_phase158_r2_repair3_depth_one_keeps_legacy_output():
  rendered = _render_group(
    8,
    7,
    max_depth=1,
  )

  assert (
    "## 使用する結果"
    not in rendered
  )
  assert "---" not in rendered
  assert "□" not in rendered
