from pathlib import Path
import inspect
import sys


ROOT = Path(__file__).resolve().parents[1]
ROOT_TEXT = str(
  ROOT
)

if ROOT_TEXT not in sys.path:
  sys.path.insert(
    0,
    ROOT_TEXT,
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
import toda_group_proof_narrative_contribution_renderer as contribution_renderer
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGET_FRAGMENT = (
  r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$"
)
TARGET_ISOMORPHISM = (
  TARGET_FRAGMENT
  + " は同型写像である."
)


def _rule_name(
  step,
) -> str:
  inference_rule = getattr(
    step,
    "inference_rule",
    None,
  )

  if inference_rule is None:
    return "<none>"

  return str(
    getattr(
      inference_rule,
      "name",
      "<unnamed>",
    )
  )


def _build_pi11_6_presentation():
  report = build_standard_toda_report(
    n=6,
    k=5,
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


def main() -> None:
  original = (
    contribution_renderer
    ._render_generic_narrative_step
  )
  trace_rows = []

  def traced(
    proof_step,
  ):
    rendered = original(
      proof_step
    )

    if (
      TARGET_FRAGMENT in rendered
      or "同型写像である." in rendered
    ):
      stack = inspect.stack()
      callers = tuple(
        frame.function
        for frame in stack[
          1:9
        ]
      )
      trace_rows.append(
        (
          type(
            proof_step.conclusion
          ).__name__,
          _rule_name(
            proof_step
          ),
          rendered,
          callers,
        )
      )

    return rendered

  contribution_renderer._render_generic_narrative_step = traced

  try:
    presentation = _build_pi11_6_presentation()
    rendered = render_toda_group_proof_narrative_markdown(
      presentation
    )
  finally:
    contribution_renderer._render_generic_narrative_step = original

  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 map-property numbered-reasoning audit4"
  )
  print(
    "=" * 78
  )
  print(
    "target: pi_11^6"
  )
  print()

  print(
    "[PUBLIC TARGET LINES]"
  )
  for line_number, line in enumerate(
    rendered.splitlines(),
    start=1,
  ):
    if TARGET_FRAGMENT in line:
      print(
        f"line {line_number}: {line}"
      )

  print()
  print(
    "[GENERIC-RENDER TRACE]"
  )

  if not trace_rows:
    print(
      "<no contribution-renderer generic trace matched>"
    )

  for index, (
    conclusion_type,
    rule_name,
    step_rendered,
    callers,
  ) in enumerate(
    trace_rows,
    start=1,
  ):
    print(
      f"TRACE {index}"
    )
    print(
      "conclusion_type:",
      conclusion_type,
    )
    print(
      "rule_name:",
      rule_name,
    )
    print(
      "rendered:",
      step_rendered,
    )
    print(
      "callers:",
      " -> ".join(
        callers
      ),
    )
    print()

  exact_iso_traces = tuple(
    row
    for row in trace_rows
    if row[2] == TARGET_ISOMORPHISM
  )

  print(
    "=" * 78
  )
  print(
    "SUMMARY"
  )
  print(
    "=" * 78
  )
  print(
    "trace rows:",
    len(
      trace_rows
    ),
  )
  print(
    "exact target isomorphism traces:",
    len(
      exact_iso_traces
    ),
  )

  if exact_iso_traces:
    print(
      "target isomorphism source route:"
    )
    for (
      conclusion_type,
      rule_name,
      _step_rendered,
      callers,
    ) in exact_iso_traces:
      print(
        "  conclusion_type:",
        conclusion_type,
      )
      print(
        "  rule_name:",
        rule_name,
      )
      print(
        "  callers:",
        " -> ".join(
          callers
        ),
      )

  print()
  print(
    "Production code changes: none"
  )
  print(
    "Test code changes: none"
  )
  print(
    "Full pytest: not run"
  )


if __name__ == "__main__":
  main()
