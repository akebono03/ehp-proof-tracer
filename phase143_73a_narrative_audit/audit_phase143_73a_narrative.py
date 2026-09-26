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


CASES = (
  (5, 2),
  (6, 2),
  (7, 2),
  (8, 2),
  (9, 2),
  (10, 2),
)

FORBIDDEN = (
  "ScalarGreaterEqualStatement",
  "TodaEtaFamilyDefinitionStatement",
)


def build_narrative(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
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


def main() -> None:
  failed = False
  combined = []

  for n, k in CASES:
    rendered = build_narrative(
      n=n,
      k=k,
    )
    combined.append(rendered)

    group_dimension = n + k

    print("=" * 78)
    print(
      f"pi_{group_dimension}^{n}"
    )

    for line in rendered.splitlines():
      if (
        "ScalarGreaterEqualStatement" in line
        or "TodaEtaFamilyDefinitionStatement" in line
        or r"\ge" in line
        or "family" in line
      ):
        print(line)

    for forbidden in FORBIDDEN:
      present = forbidden in rendered
      print(
        f"{forbidden}: "
        + (
          "FOUND"
          if present
          else "not found"
        )
      )
      if present:
        failed = True

  combined_text = "\n".join(
    combined
  )

  print("=" * 78)

  scalar_readable = (
    r"\ge" in combined_text
  )
  eta_readable = (
    "\u03b7-family \u306e\u5b9a\u7fa9"
    in combined_text
  )

  print(
    "human-readable scalar condition present: "
    + str(
      scalar_readable
    )
  )
  print(
    "human-readable eta-family definition present: "
    + str(
      eta_readable
    )
  )

  if not scalar_readable:
    failed = True

  if not eta_readable:
    failed = True

  if failed:
    raise SystemExit(
      "FAIL: Phase 143-73A Narrative audit failed."
    )

  print(
    "PASS: both internal statement names are hidden "
    "and both generic human-readable forms occur "
    "in the audited Narrative path."
  )


if __name__ == "__main__":
  main()
