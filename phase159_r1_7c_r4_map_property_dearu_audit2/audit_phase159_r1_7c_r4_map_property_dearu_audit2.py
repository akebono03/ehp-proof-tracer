from pathlib import Path
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
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
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


TARGETS = (
  (
    6,
    5,
  ),
  (
    6,
    6,
  ),
  (
    7,
    6,
  ),
  (
    9,
    7,
  ),
)

TARGET_PHRASES = (
  "は単射である.",
  "は全射である.",
)


def _label(
  n: int,
  k: int,
) -> str:
  return (
    "pi_"
    + str(
      n + k
    )
    + "^"
    + str(
      n
    )
  )


def _build(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  if not report.candidates:
    raise RuntimeError(
      "no report candidate"
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
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  return (
    presentation,
    rendered,
  )


def _rule_name(
  proof_step,
) -> str:
  rule = getattr(
    proof_step,
    "rule",
    None,
  )

  if rule is None:
    return "<none>"

  return str(
    getattr(
      rule,
      "name",
      type(
        rule
      ).__name__,
    )
  )


def main() -> None:
  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 map-property 'である' source-route audit2"
  )
  print(
    "=" * 78
  )

  total_public = 0
  total_generic_matches = 0

  for n, k in TARGETS:
    label = _label(
      n,
      k,
    )
    presentation, rendered = _build(
      n,
      k,
    )

    public_lines = tuple(
      (
        line_number,
        line,
      )
      for line_number, line in enumerate(
        rendered.splitlines(),
        start=1,
      )
      if any(
        phrase in line
        for phrase in TARGET_PHRASES
      )
    )

    print()
    print(
      "-" * 78
    )
    print(
      label
    )
    print(
      "-" * 78
    )

    for line_number, line in public_lines:
      total_public += 1

      print(
        f"[PUBLIC line {line_number}]"
      )
      print(
        line
      )

      candidates = []

      for node_index, node in enumerate(
        presentation.nodes,
        start=1,
      ):
        step = node.proof_step

        try:
          generic = _render_generic_narrative_step(
            step
          )
        except Exception as exc:
          generic = (
            "<render error: "
            + type(
              exc
            ).__name__
            + ": "
            + str(
              exc
            )
            + ">"
          )

        if not any(
          phrase in generic
          for phrase in TARGET_PHRASES
        ):
          continue

        statement_type = type(
          step.conclusion
        ).__name__

        candidates.append(
          (
            node_index,
            statement_type,
            _rule_name(
              step
            ),
            generic,
          )
        )

      if not candidates:
        print(
          "[GENERIC SOURCE] none"
        )
      else:
        for (
          node_index,
          statement_type,
          rule_name,
          generic,
        ) in candidates:
          total_generic_matches += 1
          print(
            "[GENERIC SOURCE]"
          )
          print(
            "node_index:",
            node_index,
          )
          print(
            "statement_type:",
            statement_type,
          )
          print(
            "rule_name:",
            rule_name,
          )
          print(
            "rendered:",
            generic,
          )

      print()

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
    "public occurrences:",
    total_public,
  )
  print(
    "generic-source matches:",
    total_generic_matches,
  )
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
