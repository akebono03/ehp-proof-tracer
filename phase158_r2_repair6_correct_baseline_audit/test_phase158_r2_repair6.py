from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _phase158_baseline_render_toda_group_proof_narrative_markdown,
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _presentation(
  n: int,
  k: int,
  max_depth: int = 2,
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
      max_depth=max_depth,
    )
  )

  return (
    build_toda_group_proof_presentation(
      replay
    )
  )


def _trim(
  lines: list[str],
) -> list[str]:
  result = lines[:]

  while (
    result
    and not result[
      0
    ].strip()
  ):
    result.pop(
      0
    )

  while (
    result
    and not result[
      -1
    ].strip()
  ):
    result.pop()

  return result


def _strip_terminal_qed(
  lines: list[str],
) -> list[str]:
  result = _trim(
    lines
  )

  if (
    result
    and result[
      -1
    ].strip()
    in {
      "□",
      r"$\square$",
      r"\(\square\)",
      r"\square",
    }
  ):
    result.pop()

  return _trim(
    result
  )


def _strip_reference_separator(
  lines: list[str],
) -> list[str]:
  result = _trim(
    lines
  )

  if (
    result
    and result[
      -1
    ].strip()
    == "---"
  ):
    result.pop()

  return _trim(
    result
  )


def _reference_and_proof_payloads(
  rendered: str,
) -> tuple[
  list[str],
  list[str],
]:
  lines = (
    rendered.splitlines()
  )

  if (
    "## 使用する結果" in lines
    and "## 証明" in lines
  ):
    reference_index = lines.index(
      "## 使用する結果"
    )
    proof_index = lines.index(
      "## 証明"
    )

    reference_payload = (
      _strip_reference_separator(
        lines[
          reference_index + 1:
          proof_index
        ]
      )
    )
    proof_payload = (
      _strip_terminal_qed(
        lines[
          proof_index + 1:
        ]
      )
    )

    return (
      reference_payload,
      proof_payload,
    )

  body = lines[:]

  if (
    body
    and body[
      0
    ]
    == "# Group proof narrative"
  ):
    body = body[
      1:
    ]

  return (
    [],
    _strip_terminal_qed(
      body
    ),
  )


def test_phase158_r2_repair6_pi15_8_preserves_baseline_payloads():
  presentation = (
    _presentation(
      8,
      7,
    )
  )

  baseline = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  normalized = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  baseline_reference, baseline_proof = (
    _reference_and_proof_payloads(
      baseline
    )
  )
  normalized_reference, normalized_proof = (
    _reference_and_proof_payloads(
      normalized
    )
  )

  assert (
    normalized_reference
    == baseline_reference
  )
  assert (
    normalized_proof
    == baseline_proof
  )


def test_phase158_r2_repair6_pi11_4_preserves_local_pre_r2_reference_numbers():
  presentation = (
    _presentation(
      4,
      7,
    )
  )

  baseline = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  normalized = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert (
    r"[R3]より, $\nu_{4}$ の分解写像は同型写像である."
    in baseline
  )
  assert (
    r"[R3]より, $\nu_{4}$ の分解写像は同型写像である."
    in normalized
  )


def test_phase158_r2_repair6_terminal_qed_is_single_square():
  presentation = (
    _presentation(
      8,
      7,
    )
  )

  normalized = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  nonempty = [
    line.strip()
    for line in normalized.splitlines()
    if line.strip()
  ]

  assert nonempty[
    -1
  ] == "□"
  assert r"$\square$" not in nonempty[
    -2:
  ]


def test_phase158_r2_repair6_contract_is_exactly_ordered():
  presentation = (
    _presentation(
      3,
      3,
    )
  )

  normalized = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  lines = (
    normalized.splitlines()
  )

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


def test_phase158_r2_repair6_depth_one_is_identical_to_baseline():
  presentation = (
    _presentation(
      8,
      7,
      max_depth=1,
    )
  )

  baseline = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  normalized = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert normalized == baseline
