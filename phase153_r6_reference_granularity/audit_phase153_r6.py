from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(
  REPO_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGETS = (
  ("pi4_2", 2, 2),
  ("pi5_2", 2, 3),
  ("pi6_2", 2, 4),
  ("pi7_2", 2, 5),
  ("pi8_2", 2, 6),
  ("pi9_2", 2, 7),
  ("pi10_6", 6, 4),
  ("pi12_7", 7, 5),
)


def build_presentation(
  n,
  k,
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


def main():
  failures = []

  print(
    "=" * 72
  )
  print(
    "Phase 153-R6 — Reference granularity audit"
  )
  print(
    "=" * 72
  )

  for label, n, k in TARGETS:
    presentation = build_presentation(
      n,
      k,
    )
    entries = (
      build_toda_group_proof_narrative_reference_entries(
        presentation
      )
    )
    lines_by_number = (
      _toda_group_proof_narrative_reference_statement_lines_by_number(
        presentation,
        entries,
      )
    )

    print()
    print(
      f"{label}: references={len(entries)}"
    )

    for entry in entries:
      locator = (
        entry.reference.locator
        or entry.reference.label
      )
      lines = lines_by_number.get(
        entry.number,
        (),
      )

      print(
        f"  [R{entry.number}] "
        f"{locator}: "
        f"statements={len(lines)}"
      )

      if (
        label == "pi6_2"
        and locator == "Proposition 5.6"
      ):
        if len(
          lines
        ) != 1:
          failures.append(
            (
              label,
              locator,
              (
                "expected exactly one "
                "boundary-frontier statement"
              ),
            )
          )
        elif (
          r"\pi_{6}^{3}"
          not in lines[0]
        ):
          failures.append(
            (
              label,
              locator,
              (
                "selected statement is not "
                "the pi_6^3 result"
              ),
            )
          )

  print()

  if failures:
    print(
      "FAIL"
    )

    for failure in failures:
      print(
        "  ",
        failure,
      )

    raise SystemExit(
      1
    )

  print(
    "PASS"
  )
  print(
    "Reference statement granularity follows "
    "the cross-reference proof boundary when available."
  )


if __name__ == "__main__":
  main()
