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


AUDIT_CASES = (
  ("pi_7^5", 5, 2),
  ("pi_8^6", 6, 2),
  ("pi_9^7", 7, 2),
  ("pi_10^8", 8, 2),
  ("pi_11^9", 9, 2),
  ("pi_12^10", 10, 2),
)

FORBIDDEN_FRAGMENTS = (
  "+ -1\\,",
  "+ -1 ",
)


def _build_narrative(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  if not report.candidates:
    raise RuntimeError(
      f"no group candidate for n={n}, k={k}"
    )

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=3,
    )
  )

  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def _audit_case(
  label: str,
  n: int,
  k: int,
) -> bool:
  narrative = _build_narrative(
    n,
    k,
  )

  forbidden_hits = tuple(
    fragment
    for fragment in FORBIDDEN_FRAGMENTS
    if fragment in narrative
  )

  has_subtraction = " - " in narrative

  print(
    "=" * 78
  )
  print(
    f"{label}: n={n}, k={k}"
  )
  print(
    "-" * 78
  )
  print(
    narrative.rstrip()
  )
  print(
    "-" * 78
  )
  print(
    "forbidden scalar form: "
    + (
      "FOUND "
      + repr(
        forbidden_hits
      )
      if forbidden_hits
      else "not found"
    )
  )
  print(
    "subtraction form present: "
    + str(
      has_subtraction
    )
  )

  return not forbidden_hits


def main() -> None:
  print(
    "Phase 143-72A Narrative scalar-expression re-audit"
  )
  print(
    "Actual path:"
  )
  print(
    "  build_standard_toda_report"
  )
  print(
    "  -> build_toda_group_result_proof_replay"
  )
  print(
    "  -> build_toda_group_proof_presentation"
  )
  print(
    "  -> render_toda_group_proof_narrative_markdown"
  )
  print()

  results = tuple(
    (
      label,
      _audit_case(
        label,
        n,
        k,
      ),
    )
    for label, n, k in AUDIT_CASES
  )

  failed = tuple(
    label
    for label, passed in results
    if not passed
  )

  print()
  print(
    "=" * 78
  )
  print(
    "Phase 143-72A summary"
  )
  print(
    "=" * 78
  )

  if failed:
    print(
      "FAIL: malformed scalar display remains in "
      + ", ".join(
        failed
      )
    )
    raise SystemExit(
      1
    )

  print(
    "PASS: no '+ -1\\,' / '+ -1 ' scalar display "
    "was found in the six Narrative cases."
  )


if __name__ == "__main__":
  main()
