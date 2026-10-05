from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
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


INTRO = "使用する結果を先にまとめる."


def _presentation(
  n: int,
  k: int,
):
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
      max_depth=2,
    )
  )

  return (
    build_toda_group_proof_presentation(
      replay
    )
  )


def _render_group(
  n: int,
  k: int,
) -> str:
  return (
    render_toda_group_proof_narrative_markdown(
      _presentation(
        n,
        k,
      )
    )
  )


def _reference_body(
  rendered: str,
) -> list[str]:
  lines = rendered.splitlines()
  reference_index = lines.index(
    "## 使用する結果"
  )
  separator_index = lines.index(
    "---"
  )

  return [
    line
    for line in lines[
      reference_index + 1:
      separator_index
    ]
    if line.strip()
  ]


def test_phase158_r3_reference_renderer_starts_with_r1():
  presentation = _presentation(
    8,
    7,
  )
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  rendered = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      entries
    )
  )

  assert INTRO not in rendered
  assert (
    rendered.splitlines()[
      0
    ].startswith(
      "**[R1] "
    )
  )


def test_phase158_r3_pi6_3_has_no_reference_intro():
  rendered = _render_group(
    3,
    3,
  )

  assert INTRO not in rendered

  body = _reference_body(
    rendered
  )

  assert body[
    0
  ].startswith(
    "**[R1] "
  )
  assert "Proposition 5.6" in body[
    0
  ]


def test_phase158_r3_pi15_8_has_no_reference_intro():
  rendered = _render_group(
    8,
    7,
  )

  assert INTRO not in rendered

  body = _reference_body(
    rendered
  )

  assert body[
    0
  ].startswith(
    "**[R1] "
  )
  assert "Proposition 5.15" in body[
    0
  ]


def test_phase158_r3_pi15_8_keeps_reference_content():
  rendered = _render_group(
    8,
    7,
  )

  assert "Proposition 5.15" in rendered
  assert "Proposition 4.4" in rendered
  assert (
    r"(α, \beta) \mapsto "
    r"Eα + \sigma_{8}\beta"
    in rendered
  )


def test_phase158_r3_keeps_public_contract_and_qed():
  rendered = _render_group(
    3,
    3,
  )
  lines = rendered.splitlines()
  nonempty = [
    line.strip()
    for line in lines
    if line.strip()
  ]

  assert (
    lines.index(
      "## 証明対象"
    )
    < lines.index(
      "## 使用する結果"
    )
    < lines.index(
      "---"
    )
    < lines.index(
      "## 証明"
    )
  )
  assert nonempty[
    -1
  ] == "□"
