from __future__ import annotations

from pathlib import Path

from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _phase159_r1_7c_inline_math_content,
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
from toda_human_readable_renderer import (
  render_toda_expression_latex,
)


ROOT = Path.cwd()
OUTPUT_DIR = (
  ROOT
  / "phase159_r1_7c_r2_repair4_projected_match_diagnosis"
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


def _body_lines(
  rendered: str,
) -> list[str]:
  marker = "\n## 証明\n"
  return (
    rendered.split(
      marker,
      1,
    )[1].splitlines()
    if marker in rendered
    else rendered.splitlines()
  )


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  presentation = _presentation(
    3,
    3,
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  body = _body_lines(
    rendered
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  report = [
    "# Phase 159-R1-7c R2 repair4 projected-match diagnosis",
    "",
    "Production code changes: none",
    "Test changes: none",
    "pytest: not run",
    "",
  ]

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
      or len(
        step.premises
      )
      != 2
    ):
      continue

    first = step.premises[0].conclusion
    second = step.premises[1].conclusion

    report.append(
      f"## transitivity step id={id(step)}"
    )
    report.append(
      f"- conclusion: {conclusion!r}"
    )
    report.append(
      f"- first: {first!r}"
    )
    report.append(
      f"- second: {second!r}"
    )

    try:
      lhs_latex = render_toda_expression_latex(
        conclusion.lhs
      )
      rhs_latex = render_toda_expression_latex(
        conclusion.rhs
      )
    except Exception as exc:
      report.append(
        f"- conclusion latex error: {exc!r}"
      )
      report.append("")
      continue

    if (
      isinstance(
        first,
        Relation,
      )
      and isinstance(
        second,
        Relation,
      )
      and first.lhs == conclusion.lhs
      and first.rhs == second.lhs
      and second.rhs == conclusion.rhs
    ):
      middle = first.rhs
    elif (
      isinstance(
        first,
        Relation,
      )
      and isinstance(
        second,
        Relation,
      )
      and second.lhs == conclusion.lhs
      and second.rhs == first.lhs
      and first.rhs == conclusion.rhs
    ):
      middle = second.rhs
    else:
      report.append(
        "- graph order: no supported chain"
      )
      report.append("")
      continue

    middle_latex = render_toda_expression_latex(
      middle
    )

    report.append(
      f"- lhs_latex={lhs_latex!r}"
    )
    report.append(
      f"- middle_latex={middle_latex!r}"
    )
    report.append(
      f"- rhs_latex={rhs_latex!r}"
    )

    for index, line in enumerate(
      body
    ):
      content = (
        _phase159_r1_7c_inline_math_content(
          line
        )
      )

      if content is None:
        continue

      if (
        "nu" in content.lower()
        or r"\nu" in content
        or r"\eta_{3}" in content
      ):
        report.append(
          (
            f"- body[{index}] content={content!r}; "
            f"starts_lhs={content.startswith(lhs_latex + ' = ')}; "
            f"ends_middle={content.endswith(' = ' + middle_latex)}; "
            f"equals_lhs_middle={content == lhs_latex + ' = ' + middle_latex}; "
            f"ends_rhs={content.endswith(' = ' + rhs_latex)}"
          )
        )

    report.append("")

  report.extend(
    (
      "## full pi6_3 proof body",
      "",
      "```text",
      "\n".join(
        body
      ).rstrip(),
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
