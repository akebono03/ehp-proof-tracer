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
    and not result[0].strip()
  ):
    result.pop(0)

  while (
    result
    and not result[-1].strip()
  ):
    result.pop()

  return result


def _strip_qed(
  lines: list[str],
) -> list[str]:
  result = _trim(
    lines
  )

  if (
    result
    and result[-1].strip()
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


def _sections(
  rendered: str,
):
  lines = rendered.splitlines()

  target = (
    lines.index(
      "## 証明対象"
    )
    if "## 証明対象" in lines
    else None
  )
  reference = (
    lines.index(
      "## 使用する結果"
    )
    if "## 使用する結果" in lines
    else None
  )
  proof = (
    lines.index(
      "## 証明"
    )
    if "## 証明" in lines
    else None
  )

  return (
    lines,
    target,
    reference,
    proof,
  )


def test_phase158_r2_repair4_pi15_8_preserves_baseline_reference_and_proof():
  presentation = _presentation(
    8,
    7,
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

  (
    baseline_lines,
    baseline_target,
    baseline_reference,
    baseline_proof,
  ) = _sections(
    baseline
  )
  (
    normalized_lines,
    normalized_target,
    normalized_reference,
    normalized_proof,
  ) = _sections(
    normalized
  )

  assert baseline_target is not None
  assert baseline_reference is not None
  assert baseline_proof is not None
  assert normalized_target is not None
  assert normalized_reference is not None
  assert normalized_proof is not None

  baseline_reference_body = _trim(
    baseline_lines[
      baseline_reference + 1:
      baseline_proof
    ]
  )
  normalized_separator = (
    normalized_lines.index(
      "---"
    )
  )
  normalized_reference_body = _trim(
    normalized_lines[
      normalized_reference + 1:
      normalized_separator
    ]
  )

  assert (
    normalized_reference_body
    == baseline_reference_body
  )

  baseline_proof_body = _strip_qed(
    baseline_lines[
      baseline_proof + 1:
    ]
  )
  normalized_proof_body = _strip_qed(
    normalized_lines[
      normalized_proof + 1:
    ]
  )

  assert (
    normalized_proof_body
    == baseline_proof_body
  )


def test_phase158_r2_repair4_pi11_4_preserves_current_baseline_proof():
  presentation = _presentation(
    4,
    7,
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

  assert "[R1]を用いる." in baseline
  assert "[R1]を用いる." in normalized
  assert "[R2]を用いる." in baseline
  assert "[R2]を用いる." in normalized


def test_phase158_r2_repair4_has_single_terminal_qed():
  presentation = _presentation(
    8,
    7,
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

  assert nonempty[-1] == "□"
  assert r"$\square$" not in nonempty[-2:]


def test_phase158_r2_repair4_contract_headers_are_exact():
  presentation = _presentation(
    3,
    3,
  )
  normalized = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  lines = normalized.splitlines()

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


def test_phase158_r2_repair4_depth_one_is_identical_to_baseline():
  presentation = _presentation(
    8,
    7,
    max_depth=1,
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
