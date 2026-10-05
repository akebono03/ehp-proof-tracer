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


def _section_index(
  rendered: str,
  marker: str,
) -> int:
  return (
    rendered.splitlines().index(
      marker
    )
  )


def _assert_phase158_public_contract(
  rendered: str,
) -> None:
  target_index = _section_index(
    rendered,
    "## 証明対象",
  )
  reference_index = _section_index(
    rendered,
    "## 使用する結果",
  )
  separator_index = _section_index(
    rendered,
    "---",
  )
  proof_index = _section_index(
    rendered,
    "## 証明",
  )

  assert (
    target_index
    < reference_index
    < separator_index
    < proof_index
  )

  nonempty_lines = [
    line.strip()
    for line in rendered.splitlines()
    if line.strip()
  ]

  assert (
    nonempty_lines[-1]
    == "□"
  )


def test_phase158_r2_repair1_pi6_3_contract_uses_exact_headers():
  rendered = _render_group(
    3,
    3,
  )

  _assert_phase158_public_contract(
    rendered
  )

  assert (
    rendered.splitlines().count(
      "## 証明対象"
    )
    == 1
  )
  assert (
    rendered.splitlines().count(
      "## 証明"
    )
    == 1
  )


def test_phase158_r2_repair1_pi15_8_preserves_prop44_map_formula():
  rendered = _render_group(
    8,
    7,
  )

  _assert_phase158_public_contract(
    rendered
  )

  assert (
    r"\left(α, \beta\right) \mapsto "
    r"Eα + \sigma_{8}\beta"
    in rendered
  )


def test_phase158_r2_repair1_pi15_8_keeps_single_reference_header():
  rendered = _render_group(
    8,
    7,
  )

  assert (
    rendered.splitlines().count(
      "## 使用する結果"
    )
    == 1
  )
  assert (
    rendered.splitlines().count(
      "## 証明"
    )
    == 1
  )


def test_phase158_r2_repair1_reference_free_group_has_empty_reference_section():
  rendered = _render_group(
    2,
    0,
  )

  _assert_phase158_public_contract(
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


def test_phase158_r2_repair1_depth_one_is_unchanged():
  rendered = _render_group(
    8,
    7,
    max_depth=1,
  )

  assert (
    "## 使用する結果"
    not in rendered
  )
  assert (
    "---"
    not in rendered
  )
  assert (
    "□"
    not in rendered
  )
