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

FORBIDDEN = (
  "は単射である.",
  "は全射である.",
)

EXPECTED_CONCISE = (
  "は単射.",
  "は全射.",
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
  forbidden_findings = []
  concise_findings = []

  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 map-property dearu repair1 closure audit"
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

      proof_parts = rendered.split(
        "## 証明\n\n",
        1,
      )

      proof_body = (
        proof_parts[1]
        if len(
          proof_parts
        ) == 2
        else rendered
      )

      for phrase in FORBIDDEN:
        count = proof_body.count(
          phrase
        )

        if count:
          forbidden_findings.append(
            (
              label,
              phrase,
              count,
            )
          )

      concise_count = sum(
        proof_body.count(
          phrase
        )
        for phrase in EXPECTED_CONCISE
      )

      if concise_count:
        concise_findings.append(
          (
            label,
            concise_count,
          )
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
    "forbidden affected outputs:",
    len(
      forbidden_findings
    ),
  )
  print(
    "forbidden occurrences:",
    sum(
      count
      for _, _, count in forbidden_findings
    ),
  )
  print(
    "outputs with concise map-property prose:",
    len(
      concise_findings
    ),
  )
  print(
    "concise occurrences:",
    sum(
      count
      for _, count in concise_findings
    ),
  )

  if forbidden_findings:
    print()
    print(
      "[FORBIDDEN FINDINGS]"
    )
    for label, phrase, count in forbidden_findings:
      print(
        label,
        phrase,
        count,
      )

  if concise_findings:
    print()
    print(
      "[CONCISE OUTPUTS]"
    )
    for label, count in concise_findings:
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
