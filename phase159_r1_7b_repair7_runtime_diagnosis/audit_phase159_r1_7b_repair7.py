from __future__ import annotations

from pathlib import Path

from homotopy_groups import (
  TodaEHPExactnessWindow,
)
from proof import (
  ProofStep,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _phase158_baseline_render_toda_group_proof_narrative_markdown,
  _phase159_r1_7b_exactness_step_latex,
  _phase159_r1_7b_inline_exactness_latex,
  _phase159_r1_7b_normalize_public_exact_sequences,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)


ROOT = Path.cwd()
OUTPUT_DIR = (
  ROOT
  / "phase159_r1_7b_repair7_runtime_diagnosis"
  / "audit_output"
)


def _presentation(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[
      0
    ]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  return build_toda_group_proof_presentation(
    replay
  )


def _ancestry(
  root_step: ProofStep,
) -> tuple[
  ProofStep,
  ...,
]:
  result = []
  seen = set()

  def visit(
    step: ProofStep,
  ) -> None:
    step_id = id(
      step
    )

    if step_id in seen:
      return

    seen.add(
      step_id
    )

    for premise in step.premises:
      visit(
        premise
      )

    result.append(
      step
    )

  visit(
    root_step
  )

  return tuple(
    result
  )


def _rule_name(
  step: ProofStep,
) -> str:
  rule_name = getattr(
    step,
    "rule_name",
    None,
  )

  if isinstance(
    rule_name,
    str,
  ):
    return rule_name

  source = getattr(
    step,
    "source",
    None,
  )

  if isinstance(
    source,
    str,
  ):
    return source

  return ""


def _exactness_rows(
  label: str,
  steps,
) -> list[
  str
]:
  rows = [
    f"## {label}",
    "",
  ]

  found = 0

  for index, step in enumerate(
    steps
  ):
    statement = step.conclusion

    if not isinstance(
      statement,
      (
        TodaProp42ExactnessStatement,
        TodaEHPExactnessWindow,
      ),
    ):
      continue

    found += 1
    rows.append(
      f"### exactness {found}"
    )
    rows.append(
      f"- index: {index}"
    )
    rows.append(
      "- type: "
      + type(
        statement
      ).__name__
    )
    rows.append(
      "- rule_name: "
      + repr(
        _rule_name(
          step
        )
      )
    )

    if isinstance(
      statement,
      TodaProp42ExactnessStatement,
    ):
      try:
        latex = (
          _phase159_r1_7b_exactness_step_latex(
            step
          )
        )
      except Exception as exc:
        latex = (
          "ERROR: "
          + repr(
            exc
          )
        )

      rows.append(
        "- r1_7b_latex: "
        + repr(
          latex
        )
      )

    rows.append("")

  rows.append(
    f"count: {found}"
  )
  rows.append("")

  return rows


def _extract_proof_body(
  rendered: str,
) -> list[
  str
]:
  marker = "## 証明"

  lines = rendered.rstrip().splitlines()

  try:
    index = lines.index(
      marker
    )
  except ValueError:
    return []

  body = lines[
    index + 1:
  ]

  while (
    body
    and not body[
      0
    ].strip()
  ):
    body.pop(
      0
    )

  while (
    body
    and body[
      -1
    ].strip()
    in (
      "□",
      r"$\square$",
    )
  ):
    body.pop()

  return body


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  presentation = _presentation(
    4,
    7,
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  report_lines = [
    "# Phase 159-R1-7b repair7 runtime diagnosis",
    "",
    "## presentation counts",
    "",
    (
      "- original nodes: "
      + str(
        len(
          presentation.nodes
        )
      )
    ),
    (
      "- original root ancestry: "
      + str(
        len(
          _ancestry(
            presentation.root_step
          )
        )
      )
    ),
    (
      "- closure nodes: "
      + str(
        len(
          closure.nodes
        )
      )
    ),
    (
      "- closure root ancestry: "
      + str(
        len(
          _ancestry(
            closure.root_step
          )
        )
      )
    ),
    "",
  ]

  report_lines.extend(
    _exactness_rows(
      "original nodes",
      tuple(
        node.proof_step
        for node in presentation.nodes
      ),
    )
  )
  report_lines.extend(
    _exactness_rows(
      "original root ancestry",
      _ancestry(
        presentation.root_step
      ),
    )
  )
  report_lines.extend(
    _exactness_rows(
      "closure nodes",
      tuple(
        node.proof_step
        for node in closure.nodes
      ),
    )
  )
  report_lines.extend(
    _exactness_rows(
      "closure root ancestry",
      _ancestry(
        closure.root_step
      ),
    )
  )

  baseline = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  proof_body = (
    _extract_proof_body(
      baseline
    )
  )

  report_lines.extend(
    (
      "## baseline proof-body exactness-like lines",
      "",
    )
  )

  for index, line in enumerate(
    proof_body
  ):
    if (
      "完全性より" not in line
      and "完全である" not in line
      and r"\xrightarrow{" not in line
    ):
      continue

    parsed = None

    try:
      parsed = (
        _phase159_r1_7b_inline_exactness_latex(
          line
        )
      )
    except Exception as exc:
      parsed = (
        "ERROR: "
        + repr(
          exc
        )
      )

    report_lines.append(
      f"- index {index}"
    )
    report_lines.append(
      "  - repr: "
      + repr(
        line
      )
    )
    report_lines.append(
      "  - inline parser: "
      + repr(
        parsed
      )
    )

  report_lines.append("")

  normalized_original = (
    _phase159_r1_7b_normalize_public_exact_sequences(
      presentation,
      proof_body,
    )
  )
  normalized_closure = (
    _phase159_r1_7b_normalize_public_exact_sequences(
      closure,
      proof_body,
    )
  )

  (
    OUTPUT_DIR
    / "baseline_pi11_4.md"
  ).write_text(
    baseline,
    encoding="utf-8",
  )

  (
    OUTPUT_DIR
    / "normalized_with_original_presentation.txt"
  ).write_text(
    "\n".join(
      normalized_original
    ),
    encoding="utf-8",
  )

  (
    OUTPUT_DIR
    / "normalized_with_closure_presentation.txt"
  ).write_text(
    "\n".join(
      normalized_closure
    ),
    encoding="utf-8",
  )

  report = "\n".join(
    report_lines
  )

  (
    OUTPUT_DIR
    / "diagnosis.md"
  ).write_text(
    report,
    encoding="utf-8",
  )

  print(
    report
  )
  print("")
  print(
    "Wrote:"
  )
  print(
    "  phase159_r1_7b_repair7_runtime_diagnosis/"
    "audit_output/diagnosis.md"
  )
  print(
    "  phase159_r1_7b_repair7_runtime_diagnosis/"
    "audit_output/baseline_pi11_4.md"
  )
  print(
    "  phase159_r1_7b_repair7_runtime_diagnosis/"
    "audit_output/normalized_with_original_presentation.txt"
  )
  print(
    "  phase159_r1_7b_repair7_runtime_diagnosis/"
    "audit_output/normalized_with_closure_presentation.txt"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
