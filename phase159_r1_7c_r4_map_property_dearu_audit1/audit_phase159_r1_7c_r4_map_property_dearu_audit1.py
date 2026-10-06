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
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


N_RANGE = range(
  2,
  16,
)
K_RANGE = range(
  0,
  8,
)
MAX_DEPTH = 2

TARGET_PHRASES = (
  "は単射である.",
  "は全射である.",
  "は同型である.",
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


def _render(
  n: int,
  k: int,
) -> str:
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
    max_depth=MAX_DEPTH,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def main() -> None:
  rendered_count = 0
  failed = []
  affected = []
  totals = {
    phrase: 0
    for phrase in TARGET_PHRASES
  }

  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 map-property 'である' audit1"
  )
  print(
    "=" * 78
  )
  print(
    "audit range: n=2..15, k=0..7"
  )
  print(
    "This range is an audit sample, not a permanent group-count contract."
  )
  print()

  for n in N_RANGE:
    for k in K_RANGE:
      label = _label(
        n,
        k,
      )

      try:
        rendered = _render(
          n,
          k,
        )
      except Exception as exc:
        failed.append(
          (
            label,
            type(
              exc
            ).__name__,
            str(
              exc
            ),
          )
        )
        continue

      rendered_count += 1
      lines = rendered.splitlines()
      findings = []

      for line_number, line in enumerate(
        lines,
        start=1,
      ):
        for phrase in TARGET_PHRASES:
          if phrase not in line:
            continue

          totals[
            phrase
          ] += line.count(
            phrase
          )
          findings.append(
            (
              line_number,
              phrase,
              line,
            )
          )

      if not findings:
        continue

      affected.append(
        (
          label,
          len(
            findings
          ),
        )
      )

      print(
        "-" * 78
      )
      print(
        label
      )

      for line_number, phrase, line in findings:
        print(
          f"[line {line_number}] {phrase}"
        )
        print(
          line
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
    "rendered:",
    rendered_count,
  )
  print(
    "failed:",
    len(
      failed
    ),
  )
  print(
    "affected outputs:",
    len(
      affected
    ),
  )

  for phrase in TARGET_PHRASES:
    print(
      phrase,
      totals[
        phrase
      ],
    )

  print(
    "total occurrences:",
    sum(
      totals.values()
    ),
  )

  if affected:
    print()
    print(
      "[AFFECTED LABELS]"
    )
    for label, count in affected:
      print(
        label,
        "occurrences=",
        count,
      )

  if failed:
    print()
    print(
      "[FAILURES]"
    )
    for label, error_type, message in failed:
      print(
        label,
        error_type,
        message,
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
