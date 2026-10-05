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


def _assert_phase158_public_contract(
  rendered: str,
) -> None:
  target_index = rendered.index(
    "## 証明対象"
  )
  reference_index = rendered.index(
    "## 使用する結果"
  )
  separator_index = rendered.index(
    "---"
  )
  proof_index = rendered.index(
    "## 証明"
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


def test_phase158_r2_pi6_3_gets_public_contract():
  rendered = _render_group(
    3,
    3,
  )

  _assert_phase158_public_contract(
    rendered
  )

  assert (
    rendered.count(
      "## 証明対象"
    )
    == 1
  )


def test_phase158_r2_pi15_8_preserves_existing_target():
  rendered = _render_group(
    8,
    7,
  )

  _assert_phase158_public_contract(
    rendered
  )

  assert (
    rendered.count(
      "## 証明対象"
    )
    == 1
  )
  assert (
    "Toda Proposition 5.15 のうち,"
    in rendered
  )
  assert (
    "Toda Proposition 4.4 の分解同型"
    in rendered
  )


def test_phase158_r2_reference_free_group_still_has_shell():
  rendered = _render_group(
    2,
    0,
  )

  _assert_phase158_public_contract(
    rendered
  )

  reference_index = rendered.index(
    "## 使用する結果"
  )
  separator_index = rendered.index(
    "---"
  )

  assert (
    reference_index
    < separator_index
  )


def test_phase158_r2_depth_one_keeps_legacy_contract():
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
