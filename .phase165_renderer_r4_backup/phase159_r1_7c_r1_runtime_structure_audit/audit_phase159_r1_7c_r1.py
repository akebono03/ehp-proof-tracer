from __future__ import annotations

from pathlib import Path

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_references import (
  extract_toda_group_proof_step_literature_reference,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
)


ROOT = Path.cwd()
OUTPUT_DIR = (
  ROOT
  / "phase159_r1_7c_r1_runtime_structure_audit"
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


def _rule_name(
  proof_step,
) -> str | None:
  rule = getattr(
    proof_step,
    "inference_rule",
    None,
  )
  if rule is None:
    rule = getattr(
      proof_step,
      "rule",
      None,
    )
  return getattr(
    rule,
    "name",
    None,
  )


def _reference_text(
  proof_step,
) -> str | None:
  reference = (
    extract_toda_group_proof_step_literature_reference(
      proof_step
    )
  )
  if reference is None:
    return None

  for name in (
    "label",
    "locator",
    "reference",
    "title",
  ):
    value = getattr(
      reference,
      name,
      None,
    )
    if value:
      return str(
        value
      )

  return str(
    reference
  )


def _boundary_text(
  proof_step,
) -> str | None:
  boundary = (
    classify_toda_literature_statement_step(
      proof_step
    )
  )
  if boundary is None:
    return None

  classification = getattr(
    boundary,
    "classification",
    None,
  )
  component_key = getattr(
    boundary,
    "component_key",
    None,
  )
  locator = getattr(
    boundary,
    "reference_locator",
    None,
  )

  return (
    f"classification={classification!s}; "
    f"locator={locator!r}; "
    f"component={component_key!r}"
  )


def _step_summary(
  proof_step,
) -> str:
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )
  return (
    f"type={type(proof_step.conclusion).__name__}; "
    f"rule={_rule_name(proof_step)!r}; "
    f"reference={_reference_text(proof_step)!r}; "
    f"boundary={_boundary_text(proof_step)!r}; "
    f"rendered={rendered!r}; "
    f"premises={len(proof_step.premises)}"
  )


def _walk(
  root_step,
  max_depth: int = 4,
):
  rows = []
  seen = set()

  def visit(
    proof_step,
    depth: int,
    path: str,
  ) -> None:
    step_id = id(
      proof_step
    )
    repeated = step_id in seen
    rows.append(
      (
        depth,
        path,
        step_id,
        repeated,
        _step_summary(
          proof_step
        ),
      )
    )

    if repeated:
      return

    seen.add(
      step_id
    )

    if depth >= max_depth:
      return

    for index, premise in enumerate(
      proof_step.premises,
      start=1,
    ):
      visit(
        premise,
        depth + 1,
        f"{path}.{index}",
      )

  visit(
    root_step,
    0,
    "R",
  )
  return tuple(
    rows
  )


def _body(
  rendered: str,
) -> str:
  marker = "\n## 証明\n"
  if marker not in rendered:
    return rendered
  return rendered.split(
    marker,
    1,
  )[1]


def _interesting_pi6_lines(
  body: str,
):
  needles = (
    r"2\nu'",
    r"\eta_{3}\eta_{4}\eta_{5}",
    r"\eta_{3}^{3}",
    r"\tag{",
    "(1)",
    "(2)",
  )
  return tuple(
    (
      index,
      line,
    )
    for index, line in enumerate(
      body.splitlines()
    )
    if any(
      needle in line
      for needle in needles
    )
  )


def _visible_step_matches(
  presentation,
  body: str,
):
  rows = []

  for node in presentation.nodes:
    step = node.proof_step
    rendered = (
      _render_generic_narrative_step(
        step
      )
    )
    if not rendered:
      continue

    rows.append(
      (
        rendered in body,
        id(step),
        type(step.conclusion).__name__,
        _rule_name(step),
        _reference_text(step),
        _boundary_text(step),
        rendered,
      )
    )

  return tuple(
    rows
  )


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
    "# Phase 159-R1-7c R1 runtime structure audit",
    "",
    "Production code changes: none",
    "Test changes: none",
    "pytest: not run",
    "",
    "## pi6_3 equation-chain body lines",
    "",
  ]

  for index, line in _interesting_pi6_lines(
    pi6_body
  ):
    report.append(
      f"- line {index}: `{line!r}`"
    )

  report.extend(
    (
      "",
      "## pi6_3 root/direct ancestry",
      "",
    )
  )

  for (
    depth,
    path,
    step_id,
    repeated,
    summary,
  ) in _walk(
    pi6.root_step,
    max_depth=3,
  ):
    report.append(
      (
        f"- depth={depth} path={path} "
        f"id={step_id} repeated={repeated}: "
        f"{summary}"
      )
    )

  report.extend(
    (
      "",
      "## pi11_4 root/direct ancestry",
      "",
    )
  )

  for (
    depth,
    path,
    step_id,
    repeated,
    summary,
  ) in _walk(
    pi11.root_step,
    max_depth=4,
  ):
    report.append(
      (
        f"- depth={depth} path={path} "
        f"id={step_id} repeated={repeated}: "
        f"{summary}"
      )
    )

  report.extend(
    (
      "",
      "## pi11_4 presentation-node visibility",
      "",
    )
  )

  for (
    visible,
    step_id,
    conclusion_type,
    rule_name,
    reference,
    boundary,
    rendered,
  ) in _visible_step_matches(
    pi11,
    pi11_body,
  ):
    report.append(
      (
        f"- visible={visible} id={step_id} "
        f"type={conclusion_type}; "
        f"rule={rule_name!r}; "
        f"reference={reference!r}; "
        f"boundary={boundary!r}; "
        f"rendered={rendered!r}"
      )
    )

  report.extend(
    (
      "",
      "## pi11_4 rendered proof body",
      "",
      "```text",
      pi11_body.rstrip(),
      "```",
      "",
    )
  )

  text = "\n".join(
    report
  )

  (
    OUTPUT_DIR
    / "phase159_r1_7c_r1_structure_audit.md"
  ).write_text(
    text,
    encoding="utf-8",
  )
  (
    OUTPUT_DIR
    / "pi6_3.md"
  ).write_text(
    pi6_rendered,
    encoding="utf-8",
  )
  (
    OUTPUT_DIR
    / "pi11_4.md"
  ).write_text(
    pi11_rendered,
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
