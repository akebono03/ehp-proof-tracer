from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_contribution_renderer import (
  _is_toda_group_proof_narrative_reference_statement_candidate,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  select_toda_group_proof_narrative_reference_statement_steps,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
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


def candidate_steps(
  entry,
):
  result = []
  seen_rendered = set()

  for proof_step in entry.proof_steps:
    rendered = _render_generic_narrative_step(
      proof_step
    )

    if not (
      _is_toda_group_proof_narrative_reference_statement_candidate(
        proof_step,
        rendered,
      )
    ):
      continue

    if rendered in seen_rendered:
      continue

    seen_rendered.add(
      rendered
    )
    result.append(
      proof_step
    )

  return tuple(
    result
  )


def main():
  failures = []

  print("=" * 72)
  print(
    "Phase 153-R5 — "
    "root exclusion + used external ancestry audit"
  )
  print("=" * 72)

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

    root_selected = False
    used_external_entries = 0

    print()
    print(
      f"{label}: references={len(entries)}"
    )

    for entry in entries:
      candidates = candidate_steps(
        entry
      )
      selected = (
        select_toda_group_proof_narrative_reference_statement_steps(
          entry,
          candidates,
          presentation.edges,
          root_step=presentation.root_step,
        )
      )

      if any(
        step is presentation.root_step
        for step in selected
      ):
        root_selected = True

      premise_ids = {
        id(
          edge.premise_step
        )
        for edge in presentation.edges
      }

      external_used = tuple(
        step
        for step in candidates
        if (
          step is not presentation.root_step
          and id(
            step
          ) in premise_ids
        )
      )

      if external_used:
        used_external_entries += 1

        if selected != external_used:
          failures.append(
            (
              label,
              (
                entry.reference.locator
                or entry.reference.label
              ),
              (
                "used external candidates "
                "were not preferred"
              ),
            )
          )

    print(
      "  root selected: "
      + (
        "YES"
        if root_selected
        else "NO"
      )
    )
    print(
      "  entries with used external candidates: "
      + str(
        used_external_entries
      )
    )

    if root_selected:
      failures.append(
        (
          label,
          None,
          (
            "root was selected as an "
            "external reference statement"
          ),
        )
      )

  print()

  if failures:
    print("FAIL")

    for failure in failures:
      print(
        "  ",
        failure,
      )

    raise SystemExit(
      1
    )

  print("PASS")
  print(
    "No audited group selected "
    "presentation.root_step as an "
    "external Reference statement."
  )


if __name__ == "__main__":
  main()
