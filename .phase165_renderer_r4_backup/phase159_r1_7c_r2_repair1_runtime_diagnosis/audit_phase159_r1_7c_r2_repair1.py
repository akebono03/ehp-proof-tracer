from __future__ import annotations

import inspect
from pathlib import Path

from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
  _phase158_normalize_public_narrative_contract,
  _phase159_r1_7c_step_line_indices,
  render_toda_group_proof_narrative_markdown,
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


ROOT = Path.cwd()
OUTPUT_DIR = (
  ROOT
  / "phase159_r1_7c_r2_repair1_runtime_diagnosis"
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
    .candidates[0]
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


def _body(
  rendered: str,
) -> list[str]:
  marker = "\n## 証明\n"
  if marker not in rendered:
    return rendered.splitlines()
  return rendered.split(
    marker,
    1,
  )[1].splitlines()


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  pi6 = _presentation(
    3,
    3,
  )
  pi11 = _presentation(
    4,
    7,
  )

  pi6_rendered = (
    render_toda_group_proof_narrative_markdown(
      pi6
    )
  )
  pi11_rendered = (
    render_toda_group_proof_narrative_markdown(
      pi11
    )
  )

  pi6_body = _body(
    pi6_rendered
  )
  pi11_body = _body(
    pi11_rendered
  )

  report = [
    "# Phase 159-R1-7c R2 repair1 runtime diagnosis",
    "",
    "Production code changes: none",
    "Test changes: none",
    "pytest: not run",
    "",
    "## Current public render function source",
    "",
    "```python",
    inspect.getsource(
      render_toda_group_proof_narrative_markdown
    ).rstrip(),
    "```",
    "",
    "## Phase 158 normalizer tail",
    "",
    "```python",
    inspect.getsource(
      _phase158_normalize_public_narrative_contract
    )[-5000:].rstrip(),
    "```",
    "",
    "## pi6_3 transitivity candidates",
    "",
  ]

  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      pi6
    )
  )

  for node in closure.nodes:
    step = node.proof_step
    rule = step.inference_rule
    conclusion = step.conclusion

    if (
      rule is None
      or rule.name
      != "equality transitivity"
      or not isinstance(
        conclusion,
        Relation,
      )
      or conclusion.relation_type
      is not RelationType.EQUALITY
    ):
      continue

    report.append(
      f"### step id={id(step)}"
    )
    report.append(
      "- conclusion rendered: "
      + repr(
        _render_generic_narrative_step(
          step
        )
      )
    )
    report.append(
      "- conclusion indices: "
      + repr(
        _phase159_r1_7c_step_line_indices(
          pi6_body,
          step,
        )
      )
    )

    for index, premise in enumerate(
      step.premises,
      start=1,
    ):
      report.append(
        f"- premise {index} rendered: "
        + repr(
          _render_generic_narrative_step(
            premise
          )
        )
      )
      report.append(
        f"- premise {index} indices: "
        + repr(
          _phase159_r1_7c_step_line_indices(
            pi6_body,
            premise,
          )
        )
      )

    report.append("")

  report.extend(
    (
      "## pi6_3 relevant body lines",
      "",
    )
  )

  for index, line in enumerate(
    pi6_body
  ):
    if (
      r"2\nu'" in line
      or r"\eta_{3}\eta_{4}\eta_{5}" in line
      or r"\eta_{3}^{3}" in line
      or "は単射" in line
      or "は全射" in line
    ):
      report.append(
        f"- {index}: `{line!r}`"
      )

  report.extend(
    (
      "",
      "## pi11_4 relevant body lines",
      "",
    )
  )

  for index, line in enumerate(
    pi11_body
  ):
    if (
      r"\Delta" in line
      or "Δ" in line
      or "は単射" in line
      or "は全射" in line
      or r"\xrightarrow{" in line
    ):
      report.append(
        f"- {index}: `{line!r}`"
      )

  report.extend(
    (
      "",
      "## pi6_3 rendered",
      "",
      "```text",
      pi6_rendered.rstrip(),
      "```",
      "",
      "## pi11_4 rendered",
      "",
      "```text",
      pi11_rendered.rstrip(),
      "```",
      "",
    )
  )

  text = "\n".join(
    report
  )

  (
    OUTPUT_DIR
    / "diagnosis.md"
  ).write_text(
    text,
    encoding="utf-8",
  )

  print(
    text
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
