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


def presentation(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    result,
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
    "Phase 153-R6 aggregate component granularity repair audit"
  )
  print(
    "=" * 72
  )

  for label, n, k in TARGETS:
    p = presentation(
      n,
      k,
    )
    entries = (
      build_toda_group_proof_narrative_reference_entries(
        p
      )
    )
    lines_by_number = (
      _toda_group_proof_narrative_reference_statement_lines_by_number(
        p,
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
        f"  [R{entry.number}] {locator}: statements={len(lines)}"
      )

      if (
        label == "pi6_2"
        and locator == "Proposition 5.6"
      ):
        if len(
          lines
        ) != 1:
          failures.append(
            "pi6_2 Proposition 5.6 did not render exactly one statement"
          )
          continue

        line = lines[
          0
        ]

        if (
          r"\pi_{6}^{3}"
          not in line
        ):
          failures.append(
            "pi6_2 Proposition 5.6 did not retain pi_6^3"
          )

        for forbidden in (
          r"\pi_{5}^{2}",
          r"\pi_{7}^{4}",
          r"\pi_{8}^{5}",
          r"\pi_{n + 3}^{n}",
        ):
          if forbidden in line:
            failures.append(
              (
                "pi6_2 Proposition 5.6 retained unrelated "
                + forbidden
              )
            )

  print()

  if failures:
    print(
      "FAIL"
    )

    for failure in failures:
      print(
        "  "
        + failure
      )

    raise SystemExit(
      1
    )

  print(
    "PASS"
  )
  print(
    "Aggregate Reference statements are reduced to a uniquely consumed "
    "group-relation component when structural evidence is available."
  )


if __name__ == "__main__":
  main()
